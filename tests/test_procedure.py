"""
┌─────────────────────────────┐
│ test for procedures objects │
└─────────────────────────────┘

 Florian Dupeyron
 September 2020
"""

from pyrouet.maestro.procedure.ctx    import Procedure_Context
from pyrouet.maestro.procedure.step import (
    Step_Base,
    Step_Action
)

from pyrouet.maestro.errors import (
    Procedure_Error,
    Procedure_Abort_Error,
    Procedure_Stop_Error
)

from   dataclasses import asdict
from   pprint      import pprint
import pytest
import time

# ┌────────────────────────────────────────┐
# │ Mock step definition                   │
# └────────────────────────────────────────┘
class My_Step(Step_Action):
    def __init__(self, msg, fail=False, delay=0, **kwargs):
        super().__init__(**kwargs)

        self.msg   = msg
        self.fail  = fail
        self.delay = delay

        self.mustfail = False

    def _impl(self, ctx, path_stack):
        self.mustfail = False
        print("Msg : {}".format(self.msg))

        if self.fail or self.mustfail : raise Procedure_Error("I must fail !", path_stack)
        self.mustfail = True

        if self.delay:
            time.sleep(self.delay/1000)

# ┌────────────────────────────────────────┐
# │ Step tests                             │
# └────────────────────────────────────────┘
def test_step_success():
    stp = My_Step("Hello world", fail=False)
    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.step_run("test", stp)

        assert res.result == True
        assert res.err    is None


def test_step_fail():
    stp = My_Step("Hello world", fail=True)
    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.step_run("test", stp)

        assert res.result == False
        assert isinstance(res.err, Procedure_Error)

# ┌────────────────────────────────────────┐
# │ Procedure tests                        │
# └────────────────────────────────────────┘
def test_procedure_basic():
    proc = (
        ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False}),
        ("test2", My_Step, {"msg": "Hello world 2 !", "fail": False}),
        ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False})
    )

    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.procedure_run(proc)

        assert res.result == True
        assert res.err is None
        assert len(res.tests) == 3 # All tests were executed

def test_procedure_fail():
    proc = (
        ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False}),
        ("test2", My_Step, {"msg": "Hello world 2 !", "fail": True }),
        ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False})
    )

    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.procedure_run(proc)

        assert res.result == False
        assert res.err is None

        pprint(res.tests)
        assert len(res.tests) == 3 # All tests were executed even
                                   # if the middle one failed

# ┌────────────────────────────────────────┐
# │ Subproc tests                          │
# └────────────────────────────────────────┘
def test_subproc_basic():
    proc = ( ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False}),
             ("test2", My_Step, {"msg": "Hello world 2 !", "fail": False}),
             ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False}) )

    proc2 = ( ("subproc1", proc),
              ("subproc2", proc) )

    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.procedure_run(proc2)

        assert res.result == True
        assert res.err is None
        assert len(res.tests) == 2
        assert len(res.tests[0].tests) == 3
        assert len(res.tests[1].tests) == 3

        assert res.tests[0].step_id == "subproc1"
        assert res.tests[1].step_id == "subproc2"

def test_subproc_fail():
    subproc1 = ( ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False}),
                 ("test2", My_Step, {"msg": "Hello world 2 !", "fail": False}),
                 ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False}) )

    subproc2 = ( ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False}),
                 ("test2", My_Step, {"msg": "Hello world 2 !", "fail": True }),
                 ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False}) )

    proc = ( ("subproc1", subproc1),
              ("subproc2", subproc2) )

    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.procedure_run(proc)

        pprint(asdict(res))


        assert len(res.tests) == 2
        assert len(res.tests[0].tests) == 3 # All steps were executed
        assert len(res.tests[1].tests) == 3 # All steps were executed

        assert res.tests[0].step_id == "subproc1"
        assert res.tests[1].step_id == "subproc2"

        assert res.tests[0].result == True
        assert res.tests[1].result == False

        assert res.result == False
        assert res.err is None # No critical step → No error at global level
#
# ┌────────────────────────────────────────┐
# │ Execution flow flags                   │
# └────────────────────────────────────────┘
def test_critical_flag():
    subproc1 = ( ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False, "critical": True}), # Flag doesn't have any effect as step will pass
                 ("test2", My_Step, {"msg": "Hello world 2 !", "fail": True , "critical": True}), # Flag must stop all procedure execution
                 ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False}) )

    subproc2 = ( ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False}),
                 ("test2", My_Step, {"msg": "Hello world 2 !", "fail": False}),
                 ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False}) )

    proc = (  ("subproc1", subproc1),
              ("subproc2", subproc2) )

    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.procedure_run(proc)

        pprint(asdict(res))

        assert len(res.tests) == 1                       # Only first subproc started executing
        assert len(res.tests[0].tests) == 2              # Only first two steps executed

        assert res.result == False
        assert isinstance(res.err, Procedure_Stop_Error) # Critical step failed → Raised Stop_Error

        assert res.tests[0].step_id == "subproc1"

def test_break_if_error_flag():
    subproc1 = ( ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False, "break_if_error": True}), # Flag doesn't have any effect as step will pass
                 ("test2", My_Step, {"msg": "Hello world 2 !", "fail": True , "break_if_error": True}), # Flag must stop subproc execution only
                 ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False}) )

    subproc2 = ( ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False}),
                 ("test2", My_Step, {"msg": "Hello world 2 !", "fail": False}),
                 ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False}) )

    proc     = ( ("subproc1", subproc1),
                 ("subproc2", subproc2) )

    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.procedure_run(proc)

        pprint(asdict(res))

        assert len(res.tests) == 2                       # Two subprocs executed
        assert len(res.tests[0].tests) == 2              # Only first two steps executed in first subproc
        assert len(res.tests[1].tests) == 3              # All tests executed in second subproc

        assert res.tests[0].err is None                  # No error raised at subproc level
        assert res.tests[0].result == False              # But result if False
        assert res.tests[1].result == True

        assert res.result == False
        assert res.err is None

        assert res.tests[0].step_id == "subproc1"
        assert res.tests[1].step_id == "subproc2"

# ┌────────────────────────────────────────┐
# │ Misc coverage tests                    │
# └────────────────────────────────────────┘
def test_procedure_globerr():
    proc = (
        ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False}),
        ("test2", My_Step, {"msg": "Hello world 2 !", "fail": False}),
        ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False})
    )

    ctx = Procedure_Context()
    ctx.step_run = lambda id_,stp,path_stack,errlist:None # Break something !!!

    for i in range(2):
        res, errlist = ctx.procedure_run(proc)

        assert res.result == False
        print(res.err)
        assert isinstance(res.err, TypeError) # TypeError('cannot unpack non-iterable NoneType object')
        assert len(res.tests) == 0 # Global error → No tests saved !
    
def test_procedure_invalid_shape():
    proc = (
        ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False}),
        ("test2", "12", {"msg": "Hello world 2 !", "fail": False}), # Oopsie
        ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False})
    )

    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.procedure_run(proc)

        assert res.result == False
        assert isinstance(res.err, TypeError) # missing "err" attribute in result from step_run
        assert len(res.tests) == 0 # Global error → No tests saved !

# ┌────────────────────────────────────────┐
# │ Timing storage                         │
# └────────────────────────────────────────┘
def test_timing_storage():
    proc = (
        ("test1", My_Step, {"msg": "Hello world 1 !", "fail": False, "store_timestamp": True}),
        ("test2", My_Step, {"msg": "Hello world 2 !", "delay": 500, "fail": False, "store_duration": True}),
        ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False})
    )

    ctx = Procedure_Context()

    for i in range(2):
        res,errlist = ctx.procedure_run(proc)

        assert res.result == True
        assert res.err is None
        assert len(res.tests) == 3 # All tests were executed

        assert res.tests[1].duration >= 500
        assert isinstance(res.tests[0].timestamp, int) # Timestamp was stored
