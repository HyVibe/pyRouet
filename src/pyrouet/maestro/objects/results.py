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

from .constraints import Constraint_Object

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

    constraint: Constraint_Object = None
    unit: str = ""

    # value is optional because the measure can fail
    value: Optional[any] = None
