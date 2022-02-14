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


# ┌────────────────────────────────────────┐
# │ Default constraints                    │
# └────────────────────────────────────────┘
@dataclass
class Constraint_Object:
    name: str = field(init=None)

    def validate(self,v):
        if v is None: return False
        else        : return bool(self._validate(v))

    @abstractmethod
    def _validate(self,v): pass


if __name__ == "__main__":
    from pprint      import pprint
    from dataclasses import asdict

    @dataclass
    class Constraint_Dumb(Constraint_Object):
        name = "test"

    def _validate(self,v):
        return True

    xx = Constraint_Dumb()
    print(asdict(xx))
