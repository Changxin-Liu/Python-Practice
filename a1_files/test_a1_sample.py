#!/usr/bin/env python3

"""
READ ME
Core tests are run in order of task 4, 3, 2, 1 due to the nature of the
assignment structure so the numbering looks a bit off in the output.
Once a test passes all following tests will be skipped.

If you have only implemented up to task 2 for example and would like to only
test task 2 then you can comment out the tests for tasks 4, 3 since the error
messages can get very lengthy. Be sure to uncomment them when you move on.

Please remember that these tests are not comprehensive so be sure to perform
your own testing and validation.
"""

__author__ = "Steven Summers"


from pathlib import Path

from testrunner import OrderedTestCase, TestMaster, RedirectStdIO, skipIfFailed


TEST_DATA = Path('test_data') / 'sample'


class TestDesign(OrderedTestCase):
    def setUp(self):
        if self.a1 is None:
            raise RuntimeError('Failed to import travel.py')

    def test_main_defined(self):
        self.assertFunctionDefined(self.a1, 'main', 0)

    def test_clean_import(self):
        self.assertIsCleanImport(self.a1, msg="You should not be printing on import for travel.py")

    # @skipIfFailed(test_name='test_main_defined')
    # def test_doc_strings(self):
    #     self.assertDocString(self.a1.main)


class A1Test(OrderedTestCase):
    INPUTS_PATH = TEST_DATA
    OUTPUTS_PATH = TEST_DATA

    def _run_main(self, in_path, out_path):
        with open(self.INPUTS_PATH / in_path) as fin, \
                open(self.OUTPUTS_PATH / out_path) as fout:
            in_data = fin.read()
            expected_output = fout.read()

        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(in_data)
            self.a1.main()

        self.assertMultiLineEqual(stdio.stdinout, expected_output)

    def _run_main_other(self, in_path, out_path, out_path_other):
        try:

            self._run_main(in_path, out_path)
            task_6_implemented = False
        except AssertionError:
            task_6_implemented = True

        # checks if task 6 plural wording was added
        # doesn't check for task 6 functionality
        if task_6_implemented:
            self._run_main(in_path, out_path_other)


@skipIfFailed(TestDesign, TestDesign.test_main_defined.__name__)
class TestCore(A1Test):
    _passed_task = False

    def test_task4(self):
        """ test Task 4: Interests """
        self._run_main_other('1_to_4.in', '4.out', '4_with_6.out')
        TestCore._passed_task = True

    def test_task3(self):
        """ test Task 3: Climate & Season Factor """
        if not TestCore._passed_task:
            self._run_main('1_to_4.in', '3.out')
            TestCore._passed_task = True

    def test_task2(self):
        """ test Task 2: First Exact Match """
        if not TestCore._passed_task:
            self._run_main('1_to_4.in', '2.out')
            TestCore._passed_task = True

    def test_task1(self):
        """ test Task 1: Questions & Inputs """
        if not TestCore._passed_task:
            self._run_main('1_to_4.in', '1.out')
            TestCore._passed_task = True


@skipIfFailed(TestDesign, TestDesign.test_main_defined.__name__)
class TestAdvanced(A1Test):
    def test_validation(self):
        """ test Task 5: Input Validation """
        self._run_main_other('5.in', '5.out', '5_with_6.out')

    def test_multiple_input(self):
        """ test Task 6: Multiple Inputs """
        self._run_main('6.in', '6.out')


def main():
    test_cases = [
        TestDesign,
        TestCore,
        TestAdvanced  # comment out to skip advanced tests
    ]

    master = TestMaster(max_diff=None,
                        # suppress_stdout=True,
                        timeout=1,
                        # include_no_print=True,
                        scripts=[
                            ('a1', 'travel.py'),
                        ])
    master.run(test_cases)


if __name__ == '__main__':
    main()
