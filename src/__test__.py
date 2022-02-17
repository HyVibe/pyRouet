"""
┌───────────────────┐
│ Dumb pyrouet test │
└───────────────────┘

 Florian Dupeyron
 February 2022
"""

import logging

from pyrouet.maestro.procedure.step import (
    Step_Action,
    Step_Measure
)

from pyrouet.maestro.procedure.ctx  import (
    Procedure_Context
)

from pprint      import pprint
from dataclasses import asdict

class Hello_Action(Step_Action):
    def __init__(self, msg, **kwargs):
        super().__init__(**kwargs)
        self.msg = msg

    def _impl(self, ctx, path_stack):
        print(self.msg)


class Hello_Measure(Step_Measure):
    def __init__(self, mes_value, **kwargs):
        super().__init__(**kwargs)
        self.mes_value = mes_value

    def _measure(self, ctx, path_stack, values):
        return self.mes_value


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    proc = (
        ("hello1", Hello_Action,  {"msg": "Hello world 1!", "store_timestamp": True}),
        ("hello2", Hello_Measure, {"mes_value": 23, "unit": "patates"}),
        ("cont1" , (
            ("hello1_1", Hello_Action, {"msg": "Hello world again!"}),
            ("hello1_2", Hello_Action, {"msg": "Hello world again encore!"})
        )),
        ("hello3", Hello_Action, {"msg": "Hello world 3!"})
    )

    # Init procedure context
    ctx      = Procedure_Context()
    res, err = ctx.procedure_run(proc)

    pprint(asdict(res, dict_factory=lambda x: {k:v for (k,v) in x if v is not None}))
    pprint(err)
