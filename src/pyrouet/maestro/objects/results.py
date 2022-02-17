"""
┌────────────────────────────────┐
│ Results objects for test exec. │
└────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from dataclasses import dataclass, field
from typing      import (
    ClassVar,
    List,
    Optional,
    Dict
)

from .constraints import (
    Constraint_Object,
    Constraint_Description
)

from copy         import deepcopy

# ┌────────────────────────────────────────┐
# │ Base result object                     │
# └────────────────────────────────────────┘

@dataclass
class Result_Object:
    err:       Optional[Exception]     = None # Exception object
    timestamp: Optional[int]           = None # Timestamp in ms time
    duration:  Optional[int]           = None # Duration is ms

    options:   Dict[str,any]           = field(default_factory=dict)


# ┌────────────────────────────────────────┐
# │ Procedure result object                │
# └────────────────────────────────────────┘

@dataclass
class Result_Procedure(Result_Object):
    tests: List[Result_Object] = field(default_factory=list)
    result: bool = None


# ┌────────────────────────────────────────┐
# │ Identifiable result object             │
# └────────────────────────────────────────┘

@dataclass
class Result_ID_Object(Result_Object):
    step_class: str = field(default="", init=False)
    step_id   : str = ""


# ┌────────────────────────────────────────┐
# │ Container result object                │
# └────────────────────────────────────────┘

@dataclass
class Result_Container(Result_ID_Object):
    step_class = "container"
    tests: List[Result_Object] = field(default_factory=list)


# ┌────────────────────────────────────────┐
# │ Action result object                   │
# └────────────────────────────────────────┘

@dataclass
class Result_Action(Result_ID_Object):
    step_class             = "action"
    result: Optional[bool] = None


# ┌────────────────────────────────────────┐
# │ Measure result object                  │
# └────────────────────────────────────────┘

@dataclass
class Result_Measure(Result_ID_Object):
    step_class = "measure"

    constraint: Constraint_Description = Constraint_Description(constraint_class="none", options=dict())
    unit: str = ""

    # value is optional because the measure can fail
    value: Optional[any] = None

# ┌────────────────────────────────────────┐
# │ Construct from dict                    │
# └────────────────────────────────────────┘

#def from_dict(dd: Dict[str, any]):
#    step_class   = dd["step_class"]
#    step_options = dd["options"   ]
#    r            = None # Result object
#    
#    if   step_class == "container":
#        # Construct base result object
#        r = Result_Container(step_id=dd["step_id"])
#
#        # Process inner tests
#        for t_res in dd["tests"]:
#            r.tests.append(from_dict(t_res))
#
#    elif step_class == "action":
#        r = Result_Action(**dd)
#
#    elif step_class == "measure":
#        # Build constraint description
#        const_name = d_copy["constraint"]["name"]
#        del d_copy["constraint"]["name"]
#
#        d_options = deepcopy(dd["constraint"])
#        del d_options["constraint_class"]
#
#        r_constraint = Constraint_Description(
#            name    = const_name,
#            options = deepcopy(d_copy)
#        )
#
#        # Build result object
#        r = Result_Measure(**d_copy)
#
#    return r
