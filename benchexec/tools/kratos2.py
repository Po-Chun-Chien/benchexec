# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.tools.template


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for Kratos2: A tool for verification of imperative programs
    """

    def executable(self, tool_locator):
        return tool_locator.find_executable("kratos", subdir="bin")

    def name(self):
        return "Kratos2"

    def project_url(self):
        return "https://kratos.fbk.eu/"

    def version(self, executable):
        return self._version_from_tool(
            executable, arg="-version", line_prefix="Kratos2"
        )

    def cmdline(self, executable, options, task, rlimits):
        return [executable, task.single_input_file, *options]
