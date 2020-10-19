from pyfakefs.fake_filesystem_unittest import TestCase
from os import path
from src.main import change_files_name_format


class MockedUserInput:
    def __init__(self, directory, prefix, is_dry_run):
        self.directory = directory
        self.prefix = prefix
        self.dry_run = is_dry_run
        self.files_extension = ".txt"


class SeriesRenamerTestsBaseClass(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def build_checked_file_path(self, file_index):
        return f"{self.user_input.directory}file{file_index}{self.user_input.files_extension}"

    def build_expected_file_path(self, episode_number):
        return self.user_input.directory + self.user_input.prefix + episode_number + self.user_input.files_extension

    def create_input_files(self, number_of_files):
        for file_index in range(number_of_files):
            file_path = self.build_checked_file_path(file_index)
            self.fs.create_file(file_path)
            self.assertTrue(path.exists(file_path))

    def validate_old_file_name_deletion(self, file_index):
        original_file_path = self.build_checked_file_path(file_index)
        if self.user_input.dry_run:
            self.assertTrue(path.exists(original_file_path))
        else:
            self.assertFalse(path.exists(original_file_path))

    def validate_new_file_name_creation(self, episode_number):
        updated_file_path = self.build_expected_file_path(episode_number)
        if self.user_input.dry_run:
            self.assertFalse(path.exists(updated_file_path))
        else:
            self.assertTrue(path.exists(updated_file_path))

    def validate_format_change(self, number_of_files):
        number_of_expected_file_digits = len(str(number_of_files))
        for file_index in range(number_of_files):
            episode_number = f"{file_index + 1}".zfill(number_of_expected_file_digits)
            self.validate_old_file_name_deletion(file_index)
            self.validate_new_file_name_creation(episode_number)


class TestSeriesRenamerNotInDryMode(SeriesRenamerTestsBaseClass):
    @classmethod
    def setUpClass(cls):
        cls.user_input = MockedUserInput("/test/", "family_matters", False)

    def test_single_digit_episodes(self):
        number_of_checked_episodes = 6
        self.create_input_files(number_of_checked_episodes)
        change_files_name_format(self.user_input)
        self.validate_format_change(number_of_checked_episodes)

    def test_multiple_digits_episodes(self):
        number_of_checked_episodes = 77
        self.create_input_files(number_of_checked_episodes)
        change_files_name_format(self.user_input)
        self.validate_format_change(number_of_checked_episodes)


class TestSeriesRenamerInDryMode(SeriesRenamerTestsBaseClass):
    @classmethod
    def setUpClass(cls):
        cls.user_input = MockedUserInput("/dry_test/", "the_office", True)

    def test_single_digit_episodes(self):
        number_of_checked_episodes = 6
        self.create_input_files(number_of_checked_episodes)
        change_files_name_format(self.user_input)
        self.validate_format_change(number_of_checked_episodes)

    def test_multiple_digits_episodes(self):
        number_of_checked_episodes = 77
        self.create_input_files(number_of_checked_episodes)
        change_files_name_format(self.user_input)
        self.validate_format_change(number_of_checked_episodes)
