#!/usr/bin/env python3

"""
Note:
"""

__author__ = "Steven Summers"


import inspect
import re
from pathlib import Path
from string import punctuation

from destinations import Destinations
from testrunner import OrderedTestCase, TestMaster, RedirectStdIO, skipIfFailed

# So we don't remove $ from output
punctuation = punctuation.replace('$', '')

TEST_DATA = Path('test_data') / 'marking'

# Compile regex expression "dest_1|dest_2|dest_3|dest_n"
# Reverse order because some destinations have names that are part other other
# destinations. Search in reverse to match the longer destination name first.
DESTINATIONS_PATTERN = re.compile(
    '|'.join(sorted((fr'{re.escape(d.get_name())}'
                    for d in Destinations('destinations_long.csv').get_all()), reverse=True) + ['None']),
    flags=re.MULTILINE | re.IGNORECASE
)
NEWLINES_PATTERN = re.compile(r'\n+')
SPACES_PATTERN = re.compile(r'[^\S\n]{2,}')


class TestDesign(OrderedTestCase):
    def setUp(self):
        if self.a1 is None:
            raise RuntimeError('Failed to import travel.py')

    def test_main_defined(self):
        """ test a main function has been defined """
        self.assertFunctionDefined(self.a1, 'main', 0)

    def test_clean_import(self):
        """ test no prints on import """
        self.assertIsCleanImport(self.a1, msg="You should not be printing on import for travel.py")

    def test_doc_strings(self):
        """ test all functions have documentation strings """
        for attr_name, attr in inspect.getmembers(self.a1, predicate=inspect.isfunction):
            self.aggregate(self.assertDocString, self.a1, attr_name)

        self.aggregate_tests()


class A1Test(OrderedTestCase):
    INPUTS_PATH = TEST_DATA / 'inputs'
    OUTPUTS_PATH = TEST_DATA / 'outputs'
    def _run_main(self, in_data, raw_data=False):

        if not raw_data:
            with open(self.INPUTS_PATH / in_data) as fin:
                in_data = fin.read()

        error = None
        with RedirectStdIO(stdinout=True) as stdio:
            stdio.set_stdin(in_data)
            try:
                self.a1.main()
            except EOFError as e:
                error = e

        if error:
            raise EOFError(
                f'Below is the captured output until EOF\n{stdio.stdinout}'
            ).with_traceback(error.__traceback__)

        return stdio

    def _assert_main_runs(self, in_file):
        stdio = self._run_main(in_file)
        if stdio.stdin != '':
            self.fail(msg=f"Not all input was read\n{stdio.stdinout}")

    @staticmethod
    def _clean_output(text):
        """
        Used to re-format text for partial output matching
        """
        text = NEWLINES_PATTERN.sub('\n', text.lower())
        text = SPACES_PATTERN.sub(' ', text)
        text = text.translate(str.maketrans('', '', punctuation))
        text = '\n'.join(s.strip() for s in text.splitlines(keepends=True))
        return text

    @staticmethod
    def _clean_task_6(text):
        """
        Remove task 6 specific formatting
            'continents' -> 'continent'
            'seasons'    -> 'season'
        """
        text = text.replace('continents', 'continent').replace('seasons', 'season')
        return text

    def _get_destination(self, in_path, expected_destination):
        """
        Used to check destination output only, ignores other output
        """
        stdio = self._run_main(in_path)
        destinations = DESTINATIONS_PATTERN.findall(stdio.stdinout)
        if not destinations:
            self.fail(msg=f'Found no matching destination with {in_path}.\n{stdio.stdinout}')

        if len(destinations) != 1:
            self.fail(msg=(f'Found multiple destinations with {in_path}.'
                           f'Got {destinations} expected {expected_destination}\n{stdio.stdinout}'))

        destination = destinations[0]
        if stdio.stdin != '':
            self.fail(msg=f"Not all input was read\n{stdio.stdinout}")
        self.assertEqual(destination, expected_destination, msg=in_path)

    def _check_main(self, in_path, *out_paths, clean=False, task_6=False):
        """
        Used to check output format ignoring destination output
        """
        with open(self.INPUTS_PATH / in_path) as fin:
            in_data = fin.read()

        errors = []
        passed = False
        for out_path in out_paths:
            with open(self.OUTPUTS_PATH / out_path) as fout:
                expected_output = fout.read()

            stdio = self._run_main(in_data, raw_data=True)
            output = DESTINATIONS_PATTERN.sub('', stdio.stdinout)

            if not task_6:
                output = self._clean_task_6(output)
                expected_output = self._clean_task_6(expected_output)
            if clean:
                output = self._clean_output(output)
                expected_output = self._clean_output(expected_output)

            try:
                self.assertMultiLineEqual(output, expected_output, msg=out_path)
                # Makes sure all input was read and they didn't just happen to get a match
                if stdio.stdin != '':
                    self.fail(msg=f"Not all input was read\n{stdio.stdinout}")
            except AssertionError as e:
                errors.append(e)
            else:
                passed = True
                break

        if not passed:
            raise errors[0]


@skipIfFailed(TestDesign, TestDesign.test_main_defined.__name__)
class TestFormat(A1Test):
    """
    Checks full and partial output
    """
    def test_reads_most_input(self):
        """ Task 1: Reads Most Input
        at least name and destination preferences are read
        """
        stdio = self._run_main('3_&_4_with_kids.in')
        if len(stdio.stdin.split()) > 7:
            self.fail(f'Does not read most input given\n{stdio.stdinout}')

    @skipIfFailed(test_name='test_reads_most_input')
    def test_reads_all_input(self):
        """ Task 1: Reads All Input """
        self._assert_main_runs('3_&_4_with_kids.in')

    def test_some_output(self):
        """ Task 1: Some Output Produced """
        stdio = self._run_main('3_&_4_with_kids.in')
        if stdio.stdout == '':
            self.fail(f'No output produced.\n{stdio.stdinout}')

    @skipIfFailed(test_name='test_some_output')
    def test_partial_output(self):
        """ Task 1: Partial Output Match """
        self._check_main('3_&_4_with_kids.in',
                         '1_to_4_format.out', clean=True, task_6=False)

    @skipIfFailed(test_name='test_partial_output')
    def test_full_output(self):
        """ Task 1: Full Output Match """
        self._check_main('3_&_4_with_kids.in',
                         '1_to_4_format.out', task_6=False)


@skipIfFailed(TestFormat, TestFormat.test_reads_all_input.__name__)
class TestCore(A1Test):
    """
    Test:
        Task 1-4 with same inputs (positive interest)
        Task 2 with no match
        Task 2 + 3/4 -> None (no matching climate)
        Task 2-4 with kids Yes
        Task 3 first climate match without comparing season factor
        Task 2 first match of possible multiple matches

        Set 1: cost $$$, crime High, Kids No
            First match is a Kid Friendly destination,
            so has_kids != destination.is_kid_friendly()
        Set 2: cost $$, crime Average, Kids Yes

    """
    passed_with_no_kids = False
    passed_with_kids = False
    passed_task = 0

    def test_task4_no_kids_kid_friendly(self):
        """ Task 4: Interests with No Kids & Kid Friendly """
        self._get_destination('3_&_4_no_kids.in', "Acapulco, Mexico")
        TestCore.passed_with_no_kids = True
        TestCore.passed_task = 4

    def test_task4_with_kids(self):
        """ Task 4: Interests with Kids """
        self._get_destination('3_&_4_with_kids.in', "Paris, France")
        TestCore.passed_with_kids = True
        TestCore.passed_task = 4

    def test_task4_negative_interests(self):
        """ Task 4: Negative Interests """
        self._get_destination('4_negative_interests.in', "Ireland")
        TestCore.passed_with_kids = True
        TestCore.passed_task = 4

    def test_task4_multiple_score_matches(self):
        """ Task 4: Interests with Multiple Score Matches """
        if TestCore.passed_task != 4:
            self.skipTest("Skipped due to not passing at least one of "
                          "TestCore.test_task4_no_kids_kid_friendly or "
                          "TestCore.test_task4_with_kids")

        self._get_destination('4_multiple_matches.in', "Hong Kong, China")

    def test_task3_no_kids_kid_friendly(self):
        """ Task 3: Climate & Season Factor with No Kids & Kid Friendly """
        if not TestCore.passed_with_no_kids:
            self._get_destination('3_&_4_no_kids.in', "Boca Raton, United States")
            TestCore.passed_with_no_kids = True
            TestCore.passed_task = 3

    def test_task3_with_kids(self):
        """ Task 3: Climate & Season Factor with Kids """
        if not TestCore.passed_with_kids:
            self._get_destination('3_&_4_with_kids.in', "Amsterdam, Netherlands")
            TestCore.passed_with_kids = True
            TestCore.passed_task = 3

    def test_task2_no_kids_kid_friendly(self):
        """ Task 2: First Exact Match with No Kids & Kid Friendly """
        if not TestCore.passed_with_no_kids:
            self._get_destination('2_no_kids.in', "Buenos Aires, Argentina")
            TestCore.passed_with_no_kids = True
            TestCore.passed_task = 2

    def test_task2_with_kids(self):
        """ Task 2: First Exact Match with Kids """
        if not TestCore.passed_with_kids:
            self._get_destination('2_with_kids.in', "Vienna, Austria")
            TestCore.passed_with_kids = True
            TestCore.passed_task = 2

    def test_task2_no_match(self):
        """ Task 2: No Match """
        if TestCore.passed_task < 2:
            self.skipTest("Skipped due to not passing at least one of "
                          "TestCore.test_task2_no_kids_kid_friendly or "
                          "TestCore.test_task2_with_kids")

        self._get_destination('2_no_match.in', "None")

    @skipIfFailed(test_name='test_task2_no_kids_kid_friendly')
    def test_first_climate_match_no_kids(self):
        """ Task 2 + 3: First Climate Only Match no Kids """
        # Test only if passed up to task 2 (testing half of task 3)
        if TestCore.passed_task == 2:
            self._get_destination('3_first_climate_match_no_kids.in', "Cancun, Mexico")

    @skipIfFailed(test_name='test_task2_with_kids')
    def test_first_climate_match_with_kids(self):
        """ Task 2 + 3: First Climate Only Match with Kids """
        # Test only if passed up to task 2 (testing half of task 3)
        if TestCore.passed_task == 2:
            self._get_destination('3_first_climate_match_with_kids.in', "Prague, Czech Republic")

    @skipIfFailed(test_name='test_task2_no_match')
    def test_task3_no_climate_match(self):
        """ Task 3: No Climate Match
        Test None is output, requires destination passing task 2 criteria and
        failing climate criteria
        """
        self._get_destination('3_no_climate_match.in', "None")

    def test_task1(self):
        """ Task 1: Questions & Inputs """
        if not TestCore.passed_task:
            self._get_destination('2_no_kids.in', "None")
            TestCore.passed_task = 1


@skipIfFailed(TestFormat, TestFormat.test_reads_all_input.__name__)
class TestTask5(A1Test):
    """
    Task 5 Ignores destination output
        Failing validation should lead to error or not all input was read

    Test:
        The following are tested for
            Single simple preference question
            Single interest question
            All preference questions
            All interest questions

        Works multiple times
        Accounts for alphabetical characters
        Large numbers don't cause IndexError
        Negatives aren't treated as valid for non-interest questions
        Handles Empty input
    """

    # Tests one simple prompt
    def test_out_of_range_pref(self):
        """ Task 5: Pref Input Validation with out of range input """
        self._assert_main_runs('5_out_of_range_pref.in')

    def test_non_numeric_pref(self):
        """ Task 5: Pref Input Validation with non-numeric input """
        self._assert_main_runs('5_non_numeric_pref.in')

    def test_repeat_pref(self):
        """ Task 5: Pref Input Validation Repeat Invalid """
        self._assert_main_runs('5_repeat_pref.in')

    def test_negative_pref(self):
        """ Task 5: Pref Input Validation Negative
        Negative numbers are given to non-interest questions that would take a
        digit as valid input.
        """
        self._assert_main_runs('5_negative_pref.in')

    def test_empty_pref(self):
        """ Task 5: Pref Input Validation Empty Input
        A carriage return (empty input) is entered at the prompts.
        """
        self._assert_main_runs('5_empty_pref.in')

    # Tests one interest prompt
    def test_out_of_range_interest(self):
        """ Task 5: Interest Input Validation with out of range input """
        self._assert_main_runs('5_out_of_range_interest.in')

    def test_non_numeric_interest(self):
        """ Task 5: Interest Input Validation with non-numeric input """
        self._assert_main_runs('5_non_numeric_interest.in')

    def test_repeat_interest(self):
        """ Task 5: Interest Input Validation Repeat Invalid """
        self._assert_main_runs('5_repeat_interest.in')

    def test_empty_interest(self):
        """ Task 5: Interest Input Validation Empty Input
        A carriage return (empty input) is entered at the prompts.
        """
        self._assert_main_runs('5_empty_interest.in')

    # Tests all prompts for preference
    @skipIfFailed(test_name='test_out_of_range_pref')
    def test_out_of_range_all_pref(self):
        """ Task 5: All Preference Input Validation with out of range input """
        self._assert_main_runs('5_out_of_range_all_pref.in')

    @skipIfFailed(test_name='test_non_numeric_pref')
    def test_non_numeric_all_pref(self):
        """ Task 5: All Preference Input Validation with non-numeric input """
        self._assert_main_runs('5_non_numeric_all_pref.in')

    @skipIfFailed(test_name='test_repeat_pref')
    def test_repeat_all_pref(self):
        """ Task 5: All Preference Input Validation Repeat Invalid """
        self._assert_main_runs('5_repeat_all_pref.in')

    @skipIfFailed(test_name='test_negative_pref')
    def test_negative_all_pref(self):
        """ Task 5: All Input Validation Negative
        Negative numbers are given to non-interest questions that would take a
        digit as valid input.
        """
        self._assert_main_runs('5_negative_all_pref.in')

    @skipIfFailed(test_name='test_empty_pref')
    def test_empty_all_pref(self):
        """ Task 5: All Preference Input Validation Empty Input
        A carriage return (empty input) is entered at the prompts.
        """
        self._assert_main_runs('5_empty_all_pref.in')

    # Tests all prompts for interest
    @skipIfFailed(test_name='test_out_of_range_interest')
    def test_out_of_range_all_interest(self):
        """ Task 5: All Interest Input Validation with out of range input """
        self._assert_main_runs('5_out_of_range_all_interest.in')

    @skipIfFailed(test_name='test_non_numeric_interest')
    def test_non_numeric_all_interest(self):
        """ Task 5: All Interest Input Validation with non-numeric input """
        self._assert_main_runs('5_non_numeric_all_interest.in')

    @skipIfFailed(test_name='test_repeat_interest')
    def test_repeat_all_interest(self):
        """ Task 5: All Interest Input Validation Repeat Invalid """
        self._assert_main_runs('5_repeat_all_interest.in')

    @skipIfFailed(test_name='test_empty_interest')
    def test_empty_all_interest(self):
        """ Task 5: All Interest Input Validation Empty Input
        A carriage return (empty input) is entered at the prompts.
        """
        self._assert_main_runs('5_empty_all_interest.in')

    def test_partial_output(self):
        """ Task 5: Partial Output Match """
        self._check_main('5_out_of_range_pref.in',
                         '5_format.out', clean=True, task_6=False)

    @skipIfFailed(test_name='test_partial_output')
    def test_full_output(self):
        """ Task 5: Full Output Match """
        self._check_main('5_out_of_range_pref.in',
                         '5_format.out', task_6=False)

    def test_not_recursive(self):
        """ Task 5: Check if recursion was used instead of loop """
        self.assertIsNotRecursive(lambda: self._run_main('5_repeat_pref.in'))


@skipIfFailed(TestFormat, TestFormat.test_reads_all_input.__name__)
class TestTask6(A1Test):
    """
    Task 6 functionality and validation
    requires task 4 has been passed

    Test:
        Correct or partial format. 's' added to continent and season question.

        General case
            Multiple Continents
            Multiple Seasons
            Multiple Seasons & Continents
        unordered options
        duplicate options

        Validation:
            non-numeric options
            negative numbers
            extra and trailing comma

            Comma checks 1,,3 and 1,2,3,

    """

    def setUp(self):
        if TestCore.passed_task < 4:
            self.skipTest("Skipped due to not passing Task4")

    def test_partial_output(self):
        """ Task 6: Partial Output Match """
        self._check_main('3_&_4_with_kids.in',
                         '6_format.out', clean=True, task_6=True)

    @skipIfFailed(test_name='test_partial_output')
    def test_full_output(self):
        """ Task 6: Full Output Match """
        self._check_main('3_&_4_with_kids.in',
                         '6_format.out', task_6=True)

    def test_multiple_continents_only(self):
        """ Task 6: Multiple Inputs Continents Only """
        self._get_destination('6_continents.in', 'Kenya')

    def test_multiple_seasons_only(self):
        """ Task 6: Multiple Inputs Seasons Only """
        self._get_destination('6_seasons.in', 'Karachi, Pakistan')

    @skipIfFailed(test_name='test_multiple_continents_only')
    def test_multiple_inputs(self):
        """ Task 6: Multiple Inputs """
        self._get_destination('6.in', 'Shanghai, China')

    # Valid alternative input formats
    @skipIfFailed(test_name='test_multiple_inputs')
    def test_unordered(self):
        """ Task 6: Unordered Multiple Inputs """
        self._get_destination('6_unordered.in', 'Bolivia')

    @skipIfFailed(test_name='test_multiple_inputs')
    def test_duplicate(self):
        """ Task 6: Duplicate Multiple Inputs """
        self._get_destination('6_duplicate.in', 'Shanghai, China')

    @skipIfFailed(test_name='test_multiple_inputs')
    def test_spaces(self):
        """ Task 6: Spaces Between Comma Options """
        self._get_destination('6_spaces.in', 'Shanghai, China')

    # Task 5 + 6: Validation
    # Not checking format for invalid message
    @skipIfFailed(test_name='test_multiple_inputs')
    def test_non_numeric(self):
        """ Task 6: Multiple Inputs Non-numeric Option """
        self._get_destination('6_non_numeric.in', 'Shanghai, China')

    @skipIfFailed(test_name='test_multiple_inputs')
    def test_negative_numbers(self):
        """ Task 6: Multiple Inputs Negative Option """
        self._get_destination('6_negative.in', 'Shanghai, China')

    @skipIfFailed(test_name='test_multiple_inputs')
    def test_bad_comma(self):
        """ Task 6: Multiple Inputs with Bad Comma """
        self._get_destination('6_comma.in', 'Shanghai, China')


def main():
    test_cases = [
        TestDesign,
        TestFormat,
        TestCore,
        TestTask5,
        TestTask6,
    ]

    master = TestMaster(max_diff=None,  # set to None to see full output
                        # suppress_stdout=False,
                        timeout=1,
                        # include_no_print=True,
                        scripts=[
                            ('a1', 'travel.py')
                        ])
    master.run(test_cases)


if __name__ == '__main__':
    main()
