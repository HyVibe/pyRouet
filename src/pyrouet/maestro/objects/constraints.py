"""
┌──────────────────────────────────────────────┐
│ Base class for measure constraint definition │
└──────────────────────────────────────────────┘

 Florian Dupeyron
 August 2020
 Revised February 2022
"""

from abc import ABC,abstractmethod


# ┌────────────────────────────────────────┐
# │ Default constraints                    │
# └────────────────────────────────────────┘
class Constraint_Object:
    def __init__( self, __class ):
        self.__class = __class
    
    def validate(self,v):
        if v is None : return False
        else         : return bool(self._validate(v))

    @abstractmethod
    def _validate(self,v):pass

    def data(self): return {
        "class": self.__class
    }

