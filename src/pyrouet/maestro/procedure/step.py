"""
┌────────────────────────┐
│ Base classes for steps │
└────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022

 Copyright (C) 2022, the Pyrouet project core team.
 
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License along
 with this program; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import traceback
import time
import logging

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
    Constraint_Object,
    Constraint_Description
)

from ..constraints import (
    Constraint_None
)

from ..errors import (
    Procedure_Error,
    Procedure_Constraint_Error,
    Procedure_Abort_Error,
)


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

        super().__init__()

        # Process kwargs
        self.phony           = kwargs.get("phony"          , False)
        self.critical        = kwargs.get("critical"       , False)
        self.break_if_error  = kwargs.get("break_if_error" , False)
        self.store_timestamp = kwargs.get("store_timestamp", False)
        self.store_duration  = kwargs.get("store_duration" , False)

    def options_get(self):
        dd = {
            "phony":          self.phony,
            "critical":       self.critical,
            "break_if_error": self.break_if_error,
            "store_timestamp": self.store_timestamp,
            "store_duration": self.store_duration
        }

        return dd

    @abstractmethod
    def run(self, ctx, path_stack, errlist, values):
        pass # pragma: no cover

    def clean(self):
        pass # pragma: no cover

    def abort(self):
        pass # pragma: no cover

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
        pass # pragma: no cover

    def run(self, ctx, path_stack, errlist, values):
        log     = logging.getLogger(self.path_str(path_stack))

        id_     = path_stack[-1]              # ID of action is tail of stack
        r       = Result_Action(result=False) # Default result is False

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
        pass # pragma: no cover


# ┌────────────────────────────────────────┐
# │ Base class for Measure step            │
# └────────────────────────────────────────┘

class Step_Measure(Step_Base):
    def __init__(self,
        constraint: Constraint_Object = None,
        unit: str                     = "",
        **kwargs
    ):
        super().__init__(**kwargs)

        # Kwargs options
        self.save_value = kwargs.get("save_value", False)

        # Other parameters
        self.constraint = constraint or Constraint_None()
        self.unit       = unit

    def _measure(self, ctx, path_stack, values):
        pass # pragma: no cover

    def run(self, ctx, path_stack, errlist, values):
        log = logging.getLogger(self.path_str(path_stack))
        id_ = path_stack[-1] # ID of action is tail of stack

        # Construct result object
        r   = Result_Measure(
            constraint = Constraint_Description.from_constraint(self.constraint),
            unit       = self.unit,
        )

        # Start timestamp
        t_start = time.time()

        try:
            # Get and store value
            value   = self._measure(ctx, path_stack, values) # Measure value
            r.value = value                                  # Store in result

            # Store in saved values if needed
            if self.save_value:
                values.set(path_stack, r.value)

            # Compare against constraint
            if not self.constraint.validate(r.value):
                raise Procedure_Constraint_Error(r.constraint, r.value, path_stack)

            # Measure and constraint validated without error, result is True
            r.result = True

        except Exception as e:
            r.result = False
            r.err    = e # Store error
            errlist.register(path_stack, e) # Register exception in error list

            # Print traceback if uknown error
            if not isinstance(e, Procedure_Error):
                log.debug(traceback.format_exc())
        finally:
            t_end = time.time()

            # Store timing information
            if self.store_timestamp:
                r.timestamp = int(t_start*1000)
            if self.store_duration:
                r.duration  = int((t_end-t_start)*1000)

        return r

    def clean(self):
        pass # pragma: no cover


# ┌────────────────────────────────────────┐
# │ Class for Measure transforms           │
# └────────────────────────────────────────┘

class Step_Measure_Transform(Step_Measure):
    def __init__(self,
        value_from: str,
        constraint: Constraint_Object = None,
        unit: str = "",
        **kwargs
    ):

        super().__init__(
            constraint = constraint,
            unit       = unit,
            **kwargs
        )

        self.value_from = value_from

    def _measure(self, ctx, path_stack, values):
        # Get value from ctx values
        vv = values.get(self.value_from, path_stack)
        return self._transform(ctx, path_stack, vv)

    def _transform(self, ctx, path_stack, value):
        """
        this functions take the value argument input, and turns it
        into another value. For example, takes signal as input, and
        transforms it in RMS value.
        """
        # To be implemeted
        return value

