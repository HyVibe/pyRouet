"""
┌──────────────────────────────────────────────┐
│ Base class for measure constraint definition │
└──────────────────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from abc         import ABC,abstractmethod
from dataclasses import dataclass, field
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

############################################

if __name__ == "__main__":
    from pprint      import pprint
    from dataclasses import asdict

    @dataclass
    class Constraint_Dumb(Constraint_Object):
        constraint_class = "test"

    def _validate(self,v):
        return True

    xx = Constraint_Dumb()
    print(asdict(xx))
