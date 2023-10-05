# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.result as result
import benchexec.tools.template


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for BtorSim: A witness simulator and checker for Btor2.
    URL: https://github.com/Boolector/btor2tools
    """

    def executable(self, tool_locator):
        return tool_locator.find_executable("btorsim", subdir="build/bin")

    def name(self):
        return "BtorSim"

    def cmdline(self, executable, options, task, rlimits):
        # force BtorSim to be verbose,
        # such that "[btorsim] reached bad state properties" is printed
        if "-v" not in options:
            options.append("-v")
        return [executable, task.single_input_file, *options]

    def determine_result(self, run):
        if run.was_timeout:
            return result.RESULT_TIMEOUT
        if run.exit_code.value == 0:
            for line in run.output[::-1]:
                if line.startswith("[btorsim] reached bad state properties"):
                    return result.RESULT_FALSE_PROP
            return result.RESULT_ERROR + "(unexpected behavior)"
        else:  # exit_code != 0
            line = run.output[-1]
            if "claimed bad state property" in line and "not reached" in line:
                return result.RESULT_UNKNOWN + "(violation not reached)"
            if "parse error" in line:
                return result.RESULT_ERROR + "(parsing failed)"
            return result.RESULT_ERROR
