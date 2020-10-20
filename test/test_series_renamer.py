from pyfakefs.fake_filesystem_unittest import TestCase
from os import path
from src.main import change_files_name_format, calculate_new_file_name, calculate_episode_precision

SINGLE_DIGIT_NUMBER_OF_EPISODES = 7
MULTIPLE_DIGITS_NUMBER_OF_EPISODES = 77
FILES_EXTENSION = ".txt"


class MockedUserInput:
    def __init__(self, directory, prefix, is_dry_run):
        self.directory = directory
        self.prefix = prefix
        self.dry_run = is_dry_run


class TestSupportingFunctions(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user_input = MockedUserInput("/additional/tests/", "seinfeld", True)
        cls.original_file_name_prefix = 'file'
        cls.original_file_name = f"{cls.original_file_name_prefix}57{FILES_EXTENSION}"
        cls.full_path = cls.user_input.directory + cls.original_file_name

    def build_file_names_collection(self, number_of_files):
        return [self.original_file_name_prefix + str(file_number) for file_number in range(number_of_files)]

    def get_expected_episode_number(self, episode_precision, episode_number):
        return "0" * (episode_precision - len(str(episode_number))) + str(episode_number)

    def validate_new_file_name_calculation(self, calculated_file_name, episode_precision, episode_number):
        expected_episode_number = self.get_expected_episode_number(episode_precision, episode_number)
        expected_file_name = f"{self.user_input.prefix}{expected_episode_number}{FILES_EXTENSION}"
        self.assertEqual(expected_file_name, calculated_file_name)

    def test_calculate_new_file_name_with_single_digit_episode_precision(self):
        episode_number = 5
        episode_precision = 1
        calculated_file_name = calculate_new_file_name(self.user_input.prefix, self.full_path, episode_number,
                                                       episode_precision)
        self.validate_new_file_name_calculation(calculated_file_name, episode_precision, episode_number)

    def test_calculate_new_file_name_with_multiple_digits_episode_precision(self):
        episode_number = 5
        episode_precision = 3
        calculated_file_name = calculate_new_file_name(self.user_input.prefix, self.full_path, episode_number,
                                                       episode_precision)
        self.validate_new_file_name_calculation(calculated_file_name, episode_precision, episode_number)

    def test_calculate_single_digit_episode_precision(self):
        file_names_collection = self.build_file_names_collection(3)
        episode_precision = calculate_episode_precision(file_names_collection)
        expected_precision = 1
        self.assertEqual(expected_precision, episode_precision)

    def test_calculate_multiple_digits_episode_precision(self):
        file_names_collection = self.build_file_names_collection(125)
        episode_precision = calculate_episode_precision(file_names_collection)
        expected_precision = 3
        self.assertEqual(expected_precision, episode_precision)

    def test_calculate_border_multiple_digits_episode_precision(self):
        file_names_collection = self.build_file_names_collection(10)
        episode_precision = calculate_episode_precision(file_names_collection)
        expected_precision = 2
        self.assertEqual(expected_precision, episode_precision)


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
