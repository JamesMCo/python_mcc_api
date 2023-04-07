import os
import unittest


class Result(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        if os.getenv("GITHUB_STEP_SUMMARY"):
            self.job_summary = open(os.getenv("GITHUB_STEP_SUMMARY"), "a", encoding="utf-8")
            self.job_summary.write("# Test Results\n\nName|Result\n-|-\n")
        else:
            self.job_summary = None

    def addSuccess(self, test):
        super().addSuccess(test)
        if self.job_summary:
            self.job_summary.write(f"{self.getDescription(test).split()[0]}|✅\n")

    def addError(self, test, err):
        super().addError(test, err)
        if self.job_summary:
            self.job_summary.write(f"{self.getDescription(test).split()[0]}|❗\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        if self.job_summary:
            self.job_summary.write(f"{self.getDescription(test).split()[0]}|❌\n")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        if self.job_summary:
            self.job_summary.write(f"{self.getDescription(test).split()[0]}|↪️\n")

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        if self.job_summary:
            self.job_summary.write(f"{self.getDescription(test).split()[0]}|✅\n")

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        if self.job_summary:
            self.job_summary.write(f"{self.getDescription(test).split()[0]}|❌\n")

    def printErrors(self):
        super().printErrors()
        if self.job_summary:
            self.job_summary.write("# Statistics\n")
            errors = len(self.errors)
            expected_failures = len(self.expectedFailures)
            failures = len(self.failures)
            skipped = len(self.skipped)
            unexpected_successes = len(self.unexpectedSuccesses)

            successes = self.testsRun - (errors + expected_failures + failures + skipped + unexpected_successes)
            self.job_summary.write(f"- Tests Run: {self.testsRun}\n")
            self.job_summary.write(f"- Successes: {successes}\n")
            self.job_summary.write(f"- Errors: {errors}\n")
            self.job_summary.write(f"- Expected Failures: {expected_failures}\n")
            self.job_summary.write(f"- Failures: {failures}\n")
            self.job_summary.write(f"- Skipped: {skipped}\n")
            self.job_summary.write(f"- Unexpected Successes: {unexpected_successes}\n")

            if self.errors:
                self.job_summary.write("# Errors\n")
                for test, err in self.errors:
                    test_name = self.getDescription(test).split()[1].strip("()")
                    self.job_summary.write(f"## {test_name}\n")
                    self.job_summary.write(f"```python-traceback\n{err.rstrip()}\n```\n")
            if self.failures:
                self.job_summary.write("# Failures\n")
                for test, err in self.failures:
                    test_name = self.getDescription(test).split()[1].strip("()")
                    self.job_summary.write(f"## {test_name}\n")
                    self.job_summary.write(f"```python-traceback\n{err.rstrip()}\n```\n")
            if self.unexpectedSuccesses:
                self.job_summary.write("# Unexpected Successes\n")
                for test in self.unexpectedSuccesses:
                    test_name = self.getDescription(test).split()[1].strip("()")
                    self.job_summary.write(f"## {test_name}\n")

    def __del__(self):
        if self.job_summary:
            self.job_summary.close()


class Runner(unittest.TextTestRunner):
    def __init__(self, stream=None, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=Result, warnings=None,
                 *, tb_locals=False):
        super().__init__(stream, descriptions, verbosity, failfast, buffer, resultclass, warnings, tb_locals=tb_locals)


if __name__ == "__main__":
    from test_event import *
    from test_halloffame import *
    from test_participants import *
    from test_rundown import *

    if job_summary_path := os.getenv("GITHUB_STEP_SUMMARY"):
        with open(job_summary_path, "w", encoding="utf-8") as job_summary:
            job_summary.write("")
    unittest.main(verbosity=2, testRunner=Runner)
