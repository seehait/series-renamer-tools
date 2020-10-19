from pyfakefs.fake_filesystem_unittest import TestCase
import os
from src.main import change_series_episodes_names


class MockedUserInput:
    def __init__(self, directory, prefix, is_dry_run):
        self.directory = directory
        self.prefix = prefix
        self.dry_run = is_dry_run


class TestSeriesRenamerNotInDryMode(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_input = MockedUserInput('/test/', 'family_matters', False)

    def setUp(self):
        self.setUpPyfakefs()

    def build_checked_file_path(self, file_index):
        return f"{self.user_input.directory}file{file_index}.txt"

    def validate_format_change(self, number_of_files):
        number_of_expected_file_digits = len(str(number_of_files))
        for file_index in range(number_of_files):
            episode_number = f"{file_index + 1}".zfill(number_of_expected_file_digits)
            self.assertFalse(os.path.exists(self.build_checked_file_path(file_index)))
            self.assertTrue(os.path.exists(f"{self.user_input.directory}{self.user_input.prefix}{episode_number}.txt"))

    def create_input_files(self, number_of_files):
        for file_index in range(number_of_files):
            file_path = self.build_checked_file_path(file_index)
            self.fs.create_file(file_path)
            self.assertTrue(os.path.exists(file_path))

    def test_single_digit_episodes(self):
        number_of_checked_episodes = 6
        self.create_input_files(number_of_checked_episodes)
        change_series_episodes_names(self.user_input)
        self.validate_format_change(number_of_checked_episodes)

    def test_multiple_digits_episodes(self):
        number_of_checked_episodes = 77
        self.create_input_files(number_of_checked_episodes)
        change_series_episodes_names(self.user_input)
        self.validate_format_change(number_of_checked_episodes)
