# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.result as result
import benchexec.tools.template


class Tool(benchexec.tools.template.BaseTool2):
    REQUIRED_PATHS = [
        "bin/",
        "cpv/",
        "lib/",
    ]

    def executable(self, tool_locator):
        return tool_locator.find_executable("func-encoder", subdir="bin")

    def name(self):
        return "cpv-funcenc"

    def project_url(self):
        return "https://gitlab.com/sosy-lab/software/cpv"

    def program_files(self, executable):
        return self._program_files_from_executable(
            executable, self.REQUIRED_PATHS, parent_dir=True
        )

    def cmdline(self, executable, options, task, rlimits):
        return [executable, task.single_input_file, *options]
