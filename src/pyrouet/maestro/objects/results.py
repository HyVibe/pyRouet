"""
┌────────────────────────────────┐
│ Results objects for test exec. │
└────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from dataclasses import dataclass
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

    options:   Optional[Dict[str,any]] = field(default_factory=dict)


# ┌────────────────────────────────────────┐
# │ Procedure result object                │
# └────────────────────────────────────────┘

class Result_Procedure(Result_Object):
    tests: List[Result_Object] = field(default_factory=list)
    result: bool


# ┌────────────────────────────────────────┐
# │ Identifiable result object             │
# └────────────────────────────────────────┘

class Result_ID_Object(Result_Object):
    class_: str
    id_   : str


# ┌────────────────────────────────────────┐
# │ Container result object                │
# └────────────────────────────────────────┘

class Result_Container(Result_ID_Object):
    class_ = "container"

    tests: List[Result_Object]


# ┌────────────────────────────────────────┐
# │ Action result object                   │
# └────────────────────────────────────────┘

class Result_Action(Result_ID_Object):
    class_ = "action"
    result_: Optional[bool] = None


# ┌────────────────────────────────────────┐
# │ Measure result object                  │
# └────────────────────────────────────────┘

class Result_Measure(Result_ID_Object):
    class_ = "measure"

    constraint: Constraint_Object,
    unit: str,

    # value is optional because the measure can fail
    value: Optional[any] = None
