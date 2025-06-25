# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import benchexec.result as result
import benchexec.tools.template
from benchexec.tools.sv_benchmarks_util import get_data_model_from_task, ILP32, LP64


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for KLEE.
    """

    def executable(self, tool_locator):
        return tool_locator.find_executable("klee", subdir="bin")

    def program_files(self, executable):
        return self._program_files_from_executable(
            executable, self.REQUIRED_PATHS, parent_dir=True
        )

    def version(self, executable):
        """
        The output looks like this:
        KLEE 0.2.0 (https://klee.github.io)
          Built May 22 2015 (12:47:34)
          Build mode: Release
          Build revision: 6118403fa4315388946babd25be38a9524a5e2c5

        LLVM (http://llvm.org/):
          LLVM version 3.4.2

          Optimized build.
          Built Oct 15 2014 (13:57:47).
          Default target: x86_64-pc-linux-gnu
          Host CPU: bdver1
        """
        version = self._version_from_tool(executable, line_prefix="KLEE")
        return version.split("(")[0].strip()

    def cmdline(self, executable, options, task, rlimits):
        if task.property_file:
            options += [f"--property-file={task.property_file}"]
        if rlimits.memory:
            options += [f"--max-memory={rlimits.memory}"]
        if rlimits.cputime:
            options += [f"--max-cputime-soft={rlimits.cputime}"]

        data_model_param = get_data_model_from_task(task, {ILP32: "--32", LP64: "--64"})
        if data_model_param and data_model_param not in options:
            options += [data_model_param]

        return [executable] + options + list(task.input_files_or_identifier)

    def name(self):
        return "KLEE"

    def project_url(self):
        return "https://klee.github.io"

    def determine_result(self, run):
        if run.exit_code.value != 0:
            return result.RESULT_ERROR
        errors = set()
        has_done = False
        num_partial_paths = None
        for line in run.output[::-1]:
            if line.startswith("KLEE: ERROR: "):
                if "ASSERTION FAIL:" in line:
                    errors.add("unreach-call")
                elif "memory error: out of bound pointer" in line:
                    errors.add("valid-deref")
                elif "overflow" in line:
                    errors.add("no-overflow")
                elif "invalid klee_assume call (provably false)" in line:
                    errors.add("valid-assume")
                elif "abort failure" in line:
                    errors.add("abort")
                elif "concretized symbolic size" in line:
                    errors.add("conc-sym-size")
                else:
                    errors.add("other")
            if line.startswith("KLEE: done"):
                has_done = True
                if "partially completed paths" in line:
                    if num_partial_paths is not None:
                        logging.warning(
                            "Duplicate entries for partially completed paths"
                        )
                    pos = line.find("=") + 1
                    num_partial_paths = line[pos:].strip()
                    if not num_partial_paths.isdigit():
                        logging.warning(
                            "Non-numeric value for number of "
                            "partially completed paths: '%s'",
                            num_partial_paths,
                        )
                    else:
                        num_partial_paths = int(num_partial_paths)

        if errors:
            suffix = ",".join(sorted(errors))
            return result.RESULT_FALSE_PROP + f"({suffix})"
        if has_done and num_partial_paths == 0:
            return result.RESULT_TRUE_PROP
        return result.RESULT_UNKNOWN + ("(done)" if has_done else "")

    def get_value_from_output(self, lines, identifier):
        # search for the text in output and get its value,
        # stop after the first line, that contains the searched text
        for line in lines:
            if line.startswith("KLEE: done: ") and line.find(identifier + " = ") != -1:
                startPosition = line.rfind("=") + 2
                return line[startPosition:].strip()
        return None
