# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec
import benchexec.result as result
from benchexec.tools.sv_benchmarks_util import get_data_model_from_task, ILP32, LP64


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info Kratos2's SV-COMP wrapper
    (taken and adapted from https://doi.org/10.5281/zenodo.7890411)
    """

    REQUIRED_PATHS = [
        "bin/",
        "include/",
        "lib/",
        "tools/",
    ]

    def executable(self, tool_locator):
        return tool_locator.find_executable("kratos_svcomp.py", subdir="bin")

    def name(self):
        return "Kratos2"

    def project_url(self):
        return "https://kratos.fbk.eu/"

    def version(self, executable):
        return self._version_from_tool(executable, line_prefix="Kratos2")

    def program_files(self, executable):
        return self._program_files_from_executable(
            executable, self.REQUIRED_PATHS, parent_dir=True
        )

    def cmdline(self, executable, options, task, rlimits):
        assert task.options.get("language") == "C"
        options += ["--svcomp-spec", task.property_file]
        data_model = get_data_model_from_task(task, {ILP32: "32", LP64: "64"})
        if data_model and "--bitvectors" not in options:
            options += ["--bitvectors", data_model]
        return [executable, *options, task.single_input_file]

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
