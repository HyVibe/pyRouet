"""
┌───────────────────┐
│ Dumb pyrouet test │
└───────────────────┘

 Florian Dupeyron
 February 2022
"""

import logging

from pyrouet.maestro.procedure.step import (
    Step_Action
)

from pyrouet.maestro.procedure.ctx  import (
    Procedure_Context
)

from pprint import pprint

class Hello_Step(Step_Action):
    def __init__(self, msg, **kwargs):
        super().__init__(**kwargs)
        self.msg = msg

    def _impl(self, ctx, path_stack):
        print(self.msg)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    proc = (
        ("hello1", Hello_Step, {"msg": "Hello world 1!"}),
        ("hello2", Hello_Step, {"msg": "Hello world 2!"}),
        ("hello3", Hello_Step, {"msg": "Hello world 3!"}),
        ("hello4", Hello_Step, {"msg": "Hello world 4!"}),
    )

    # Init procedure context
    ctx      = Procedure_Context()
    res, err = ctx.procedure_run(proc)

    pprint(res)
