
from . import compiler
from . import process

class JudgerError(Exception):
    def __init__(self, *args):
        self.args = args
        return
    pass

class JudgerResult:
    """ Result of judger. """
    def __init__(self,
            judge_result = 'IJI',
            input_compile_result = compiler.CompilerResult(),
            input_execute_result = process.ProcessResult(),
            out_compile_result = compiler.CompilerResult(),
            out_execute_result = process.ProcessResult(),
            stdout_compile_result = compiler.CompilerResult(),
            stdout_execute_result = process.ProcessResult()):
        self.judge_result = judge_result
        self.input_compile_result = input_compile_result
        self.input_execute_result = input_execute_result
        self.out_compile_result = out_compile_result
        self.out_execute_result = out_execute_result
        self.stdout_compile_result = stdout_compile_result
        self.stdout_execute_result = stdout_execute_result
        return
    pass

status_codes = {
    'AC': 'Accepted',
    'CE': 'Compile Error',
    'WA': 'Wrong Answer',
    'RE': 'Runtime Error',
    'TLE': 'Time Limit Exceeded',
    'MLE': 'Memory Limit Exceeded',
    'OLE': 'Output Limit Exceeded',
    'PE': 'Presentation Error',
    'IJI': 'Invalid Judger Input',
}

class Judger:
    """ Base judger, always returns NotImplementedError on all actions. Extend
    this class for further functionalities.

    Additional arguments must be passed in upon __init__. judge() function upon
    call should be accustomed with limits, when necessary. It always should
    return a dict() with a JudgerResult. """

    def __init__(self):
        return

    def judge(self, *args, **kwargs):
        raise NotImplementedError()
    pass

class DataComparisonJudger(Judger):
    """ Compares data between files, will raise presentation error if found
    correct answer yet incorrect formatting. Receives following arguments at
    initialization:

        input_handle : Input file handle
        out_handle : User output handle
        stdout_handle : Handle of standard output
        seed : Random seed, randomize if not given

    Used to judge I/O from local files. """


    def judge(self, out_str, stdout_str, time_limit=0, memory_limit=0):
        def __strip_down(s_in, flag):
            lout = list()
            for i in s_in:
                if len(i) <= 0:
                    continue
                lin = i.split(flag)
                for j in lin:
                    if len(j) > 0:
                        lout.append(j)
                continue
            return lout
        def __strip_down_all(s_in):
            s_in = [s_in]
            for i in ' \t\r\n':
                s_in = __strip_down(s_in)
            return s_in
        # Checking info
        if out_str['time'] > time_limit > 0:
            return 'TLE'
        if out_str['memory'] > memory_limit > 0:
            return 'MLE'
        if out_str['return_code'] != 0:
            return 'RE'
        out_s = out_str['stdout']
        stdout_s = stdout_str['stdout']
        out_l = __strip_down_all(out_s)
        stdout_l = __strip_down_all(stdout_s)
        if out_l != stdout_l:
            return 'WA'
        if out_s != stdout_s:
            return 'PE'
        return 'AC'
    pass
