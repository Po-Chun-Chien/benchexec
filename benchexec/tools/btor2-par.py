# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

BASE_CLASS = __import__("benchexec.tools.btor2-select", fromlist=["Tool"]).Tool


class Tool(BASE_CLASS):
    def executable(self, tool_locator):
        return tool_locator.find_executable("btor2-par", subdir="bin")

    def name(self):
        return "Btor2-Par"
