"""
┌──────────────────────────────────────────────┐
│ Base class for measure constraint definition │
└──────────────────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from abc         import ABC,abstractmethod
from dataclasses import dataclass, field, asdict
from typing      import Dict


# ┌────────────────────────────────────────┐
# │ Default constraints                    │
# └────────────────────────────────────────┘

@dataclass
class Constraint_Object:
    constraint_class: str = field(init=None)

    def validate(self,v):
        if v is None: return False
        else        : return bool(self._validate(v))

    @abstractmethod
    def _validate(self,v): pass


# ┌────────────────────────────────────────┐
# │ Constraint description                 │
# └────────────────────────────────────────┘

# constraint description object: Read/write from results
# file

@dataclass
class Constraint_Description:
    constraint_class: str
    options: Dict[str, any]

    @classmethod
    def from_constraint(cls, c: Constraint_Object):
        cnst_dict  = asdict(c)
        cnst_class = cnst_dict["constraint_class"]

        del cnst_dict["constraint_class"]

        return cls(
            constraint_class=cnst_class,
            options         = cnst_dict
        )
