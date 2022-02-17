"""
┌─────────────────────────────────────┐
│ Module defining measure constraints │
└─────────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from dataclasses           import dataclass
from ..objects.constraints import Constraint_Object

# ┌────────────────────────────────────────┐
# │ Special constraints                    │
# └────────────────────────────────────────┘

@dataclass
class Constraint_None(Constraint_Object):
    constraint_class = "none"

    def _validate(self,v):
        return True

# ┌────────────────────────────────────────┐
# │ Boolean constraints                    │
# └────────────────────────────────────────┘

from .boolean import Constraint_Boolean


# ┌────────────────────────────────────────┐
# │ Numeric constraints                    │
# └────────────────────────────────────────┘

from .numeric import (
    Constraint_Below,
    Constraint_Above,
    Constraint_Tolerance,
    Constraint_Range
)

