"""
┌─────────────────────────────┐
│ test for procedures objects │
└─────────────────────────────┘

 Florian Dupeyron
 September 2020
"""

from pyrouet.maestro.procedure.ctx    import Procedure_Context

from pyrouet.maestro.constraints import (
    Constraint_None,
    Constraint_Above
)

from pyrouet.maestro.procedure.step import (
    Step_Base,
    Step_Action,
    Step_Measure,
    Step_Measure_Transform
)

from pyrouet.maestro.errors import (
    Procedure_Error,
    Procedure_Abort_Error,
    Procedure_Stop_Error,
    Procedure_Constraint_Error
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


class My_Broken_Step(Step_Action):
    """
    This step's implementation is voluntary broken,
    so that it raises an non-Procedure_Error derived
    exception.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _impl(self, ctx, path_stack):
        broken_dict = {"a": 1, "b": 2}
        print(broken_dict["c"]) # Raises KeyError


class My_Measure(Step_Measure):
    def __init__(self, value, constraint, unit="", delay=0, **kwargs):
        super().__init__(constraint, unit, **kwargs)
        self.value = value
        self.delay = delay

    def _measure(self, ctx, path_stack, values):
        if self.delay:
            time.sleep(self.delay/1000)

        return self.value

class My_Broken_Measure(Step_Measure):
    """
    This step's implementation is voluntary broken,
    so that it raises an non-Procedure_Error derived
    exception.
    """

    def __init__(self, constraint, unit="", **kwargs):
        super().__init__(constraint, unit, **kwargs)

    def _measure(self, ctx, path_stack, values):
        broken_dict = {"a": 1, "b": 2}
        return broken_dict["c"] # Raises KeyError

class My_Transform(Step_Measure_Transform):
    def __init__(self, value_from, constraint, unit = "", **kwargs):
        super().__init__(value_from, constraint, unit, **kwargs)

    #def _transform(self, ctx, path_stack, value):
    #    return value+1

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

def test_step_broken():
    stp = My_Broken_Step()
    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.step_run("test", stp)

        assert res.result == False
        assert not isinstance(res.err, Procedure_Error)


def test_measure_success():
    stp = My_Measure(1.0, constraint=Constraint_Above(ref_value=0.0))
    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.step_run("test", stp)

        pprint(asdict(res))

        assert res.result == True
        assert res.err    is None


def test_measure_fail():
    stp = My_Measure(-1.0, constraint=Constraint_Above(ref_value=0.0))
    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.step_run("test", stp)

        pprint(res)
        pprint(asdict(res))

        assert res.result == False
        assert isinstance(res.err, Procedure_Constraint_Error)


def test_measure_broken():
    stp = My_Broken_Measure(constraint=None)
    ctx = Procedure_Context()

    for i in range(2):
        res, errlist = ctx.step_run("test", stp)

        assert res.result == False
        assert not isinstance(res.err, Procedure_Error)

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

    # Nested error_subproc tests condition to check Stop_Error in procedure context execution
    proc = (  ("subproc1", subproc1),
              ("subproc2", (
                    ("error_subproc", subproc2)
              )) )

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
        ("test3", My_Step, {"msg": "Hello world 3 !", "fail": False}),
        ("test4", "kdjr")
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
        ("test1", My_Step,    {"msg": "Hello world 1 !", "fail": False, "store_timestamp": True}),
        ("test2", My_Measure, {"value": 1, "constraint": None,          "store_timestamp": True}),
        ("test3", My_Step,    {"msg": "Hello world 2 !", "delay": 200, "fail": False, "store_duration": True}),
        ("test4", My_Measure, {"value": 1, "constraint": None, "delay": 200, "store_duration": True}),
        ("test5", My_Step,    {"msg": "Hello world 3 !", "fail": False})
    )

    ctx = Procedure_Context()

    for i in range(2):
        res,errlist = ctx.procedure_run(proc)

        assert res.result == True
        assert res.err is None
        assert len(res.tests) == 5 # All tests were executed

        assert isinstance(res.tests[0].timestamp, int) # Timestamp was stored
        assert isinstance(res.tests[1].timestamp, int) # Timestamp was stored
        assert res.tests[2].duration >= 200            # Duration was stored
        assert res.tests[3].duration >= 200            # Duration was stored


# ┌────────────────────────────────────────┐
# │ Measure store and transform            │
# └────────────────────────────────────────┘

def test_measure_values():
    """
    Tests value save_flag option and measure transforms
    """
    proc = (
        ("measure"  , My_Measure,   {"value": 2, "constraint": None, "save_value": True}),
        ("transform", My_Transform, {"value_from": "^measure", "constraint": Constraint_Above(2)})
    )
    
    ctx = Procedure_Context()

    for i in range(2):
        res,errlist = ctx.procedure_run(proc)

        assert res.result == True
        assert res.err is None
