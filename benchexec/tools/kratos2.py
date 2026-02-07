import benchexec
import benchexec.result as result
from benchexec.tools.sv_benchmarks_util import get_data_model_from_task, ILP32, LP64


class Tool(benchexec.tools.template.BaseTool2):
    """
    Info object for the tool Kratos2.
    URL: TODO
    """

    REQUIRED_PATHS = ["."]

    def executable(self, tool_locator):
        return tool_locator.find_executable("kratos_svcomp.py")

    def environment(self, executable):
        return {'additionalEnv' : {'PYTHONPATH' : ':/home/ae/.local/lib/python3.10/site-packages'}}

    def name(self):
        """The human-readable name of the tool."""
        return "kratos2"

    def cmdline(self, executable, options, task, rlimits):
        return ["python3", executable] + options + list(task.input_files_or_identifier)

    def determine_result(self, run):
        reason = None

        for line in run.output:
            if line.startswith("c2kratos exception:"):
                reason = "c2kratos"

            if line.startswith("result = "):
                res = line[9:]
                if res == "safe":
                    return result.RESULT_TRUE_PROP
                if res == "unsafe":
                    return result.RESULT_FALSE_PROP
                if res == "unknown":
                    if reason is None:
                        return result.RESULT_UNKNOWN
                    else:
                        return f"{result.RESULT_UNKNOWN} ({reason})"
                return f"{result.RESULT_UNKNOWN} ({res})"

        if run.exit_code.value is not None and run.exit_code.value not in (0, 9):
            return f"{result.RESULT_ERROR} (ret {run.exit_code.value})"
        if run.exit_code.signal is not None and run.exit_code.signal not in (0, 9):
            return f"{result.RESULT_ERROR} (sig {run.exit_code.signal})"

        return result.RESULT_ERROR
