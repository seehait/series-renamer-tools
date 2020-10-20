from pyfakefs.fake_filesystem_unittest import TestCase
from os import path
from src.main import change_files_name_format

SINGLE_DIGIT_NUMBER_OF_EPISODES = 7
MULTIPLE_DIGITS_NUMBER_OF_EPISODES = 77
FILES_EXTENSION = ".txt"


class MockedUserInput:
    def __init__(self, directory, prefix, is_dry_run):
        self.directory = directory
        self.prefix = prefix
        self.dry_run = is_dry_run


class SeriesRenamerTestsBaseClass:
    def build_checked_file_path(self, file_index):
        return f"{self.user_input.directory}file{file_index}{FILES_EXTENSION}"

    def build_expected_file_path(self, episode_number):
        return self.user_input.directory + self.user_input.prefix + episode_number + FILES_EXTENSION

    def create_input_files(self, number_of_files):
        for file_index in range(number_of_files):
            file_path = self.build_checked_file_path(file_index)
            self.fs.create_file(file_path)
            self.assertTrue(path.exists(file_path))

    def validate_old_file_name_deletion(self, file_index):
        original_file_path = self.build_checked_file_path(file_index)
        if self.user_input.dry_run or self.is_input_invalid:
            self.assertTrue(path.exists(original_file_path))
        else:
            self.assertFalse(path.exists(original_file_path))

    def validate_new_file_name_creation(self, episode_number):
        updated_file_path = self.build_expected_file_path(episode_number)
        if self.user_input.dry_run or self.is_input_invalid:
            self.assertFalse(path.exists(updated_file_path))
        else:
            self.assertTrue(path.exists(updated_file_path))

    def validate_format_change(self, number_of_files):
        number_of_expected_file_digits = len(str(number_of_files))
        for file_index in range(number_of_files):
            episode_number = f"{file_index + 1}".zfill(number_of_expected_file_digits)
            self.validate_old_file_name_deletion(file_index)
            self.validate_new_file_name_creation(episode_number)

    def add_invalid_directory(self):
        self.is_input_invalid = True
        self.user_input.directory = "5"

    def test_single_digit_episodes(self):
        self.create_input_files(SINGLE_DIGIT_NUMBER_OF_EPISODES)
        change_files_name_format(self.user_input)
        self.validate_format_change(SINGLE_DIGIT_NUMBER_OF_EPISODES)

    def test_single_digit_episodes_with_invalid_directory(self):
        self.add_invalid_directory()
        self.create_input_files(SINGLE_DIGIT_NUMBER_OF_EPISODES)
        change_files_name_format(self.user_input)
        self.validate_format_change(SINGLE_DIGIT_NUMBER_OF_EPISODES)

    def test_multiple_digits_episodes(self):
        self.create_input_files(MULTIPLE_DIGITS_NUMBER_OF_EPISODES)
        change_files_name_format(self.user_input)
        self.validate_format_change(MULTIPLE_DIGITS_NUMBER_OF_EPISODES)

    def test_multiple_digits_episodes_with_invalid_directory(self):
        self.add_invalid_directory()
        self.create_input_files(MULTIPLE_DIGITS_NUMBER_OF_EPISODES)
        change_files_name_format(self.user_input)
        self.validate_format_change(MULTIPLE_DIGITS_NUMBER_OF_EPISODES)


class TestSeriesRenamerNotInDryMode(TestCase, SeriesRenamerTestsBaseClass):
    def setUp(self):
        self.setUpPyfakefs()
        self.is_input_invalid = False
        self.user_input = MockedUserInput("/test/", "family_matters", False)


class TestSeriesRenamerInDryMode(TestCase, SeriesRenamerTestsBaseClass):
    def setUp(self):
        self.setUpPyfakefs()
        self.is_input_invalid = False
        self.user_input = MockedUserInput("/dry_test/", "the_office", True)
