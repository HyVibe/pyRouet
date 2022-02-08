"""
┌────────────────────────┐
│ Base classes for steps │
└────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from abc import (
    ABC,
    abstractmethod
)

from ..objects.results import (
    Result_Action,
    Result_Measure,
    Result_Container
)

from ..objects.constraints import (
    Constraint_Object
)

from ..constraints import (
    Constraint_None
)

from ..errors import (
    Procedure_Error,
    Procedure_Abort_Error
)

import traceback
import time
import logging


# ┌────────────────────────────────────────┐
# │ Base step class                        │
# └────────────────────────────────────────┘

class Step_Base(ABC):
    def __init__(self, **kwargs):
        """
        Available kwargs:
        - phony:   bool → Execute even if already done
        - critcal: bool → Stop procedure execution if error
        """

        super().__init_()

        # Process kwargs
        self.phony           = kwargs.get("phony"          , False)
        self.critical        = kwargs.get("critical"       , False)
        self.break_if_error  = kwargs.get("break_if_error" , False)
        self.store_timestamp = kwargs.get("store_timestamp", False)
        self.store_duration  = kwargs.get("store_duration" , False)

    def options_get(self):
        dd = {
            "phony":          self.phony,
            "critical":       self.cricital,
            "break_if_error": self.break_if_error
        }

        return dd

    @abstractmethod
    def run(self, ctx, path_stack, errlist, values):
        pass

    def clean(self):
        pass

    def abort(self):
        pass

    @classmethod
    def path_str(cls, path_stack):
        return ".".join(path_stack)

# ┌────────────────────────────────────────┐
# │ Base class for Action step             │
# └────────────────────────────────────────┘

class Step_Action(Step_Base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # user-implemented
    def _impl(self, ctx, path_stack):
        pass

    def run(self, ctx, path_stack, errlist, values):
        log     = logging.getLogger(self.path_str(path_stack))

        id_     = path_stack[-1]            # ID of action is tail of stack
        r       = Result_Action(id_, False) # Default result is False

        t_start = time.time()

        try:
            self._impl(ctx, path_stack)     # Run action implementation
            r.result = True                 # No exception, action did go sucessfully

        except Exception as e:
            r.err = e                       # Store error
            errlist.register(path_stack, e) # Register in errlist

            # Print traceback if unknown error
            if not isinstance(e, Procedure_Error):
                log.error(traceback.format_exc())
        finally:
            t_end = time.time()

            # Store timing information
            if self.store_timestamp:
                r.timestamp = int(t_start*1000)

            if self.store_duration:
                r.duration  = int((t_end-t_start)*1000)

        return r

    def clean(self):
        pass
