"""
┌──────────────────────────────────┐
│ Boolean constraints for measures │
└──────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from pyrouet.maestro.objects.constraints import Constraint_Object
from dataclasses                         import dataclass, field


@dataclass
class Constraint_Boolean(Constraint_Object):
    name = "boolean"
    ref_value: any

    def _validate(self,v):
        return v == self.ref_value
