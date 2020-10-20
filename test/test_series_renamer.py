from pyfakefs.fake_filesystem_unittest import TestCase
from os import path
from src.main import change_files_name_format, calculate_new_file_name, calculate_episode_precision,\
    change_file_name_format
from mock import patch, call

FILES_EXTENSION = ".txt"
FILES_NAME_PREFIX = 'file'
MULTIPLE_DIGITS_NUMBER_OF_EPISODES = 77
SINGLE_DIGIT_NUMBER_OF_EPISODES = 7


class MockedUserInput:
    def __init__(self, directory, prefix, is_dry_run):
        self.directory = directory
        self.prefix = prefix
        self.dry_run = is_dry_run


def build_file_names_collection(original_file_name_prefix, number_of_files):
    return [original_file_name_prefix + str(file_number) for file_number in range(number_of_files)]


class TestSupportingFunctions(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_input = MockedUserInput(
            "/additional/tests/", "seinfeld", True)

        cls.original_file_name = f"{FILES_NAME_PREFIX}57{FILES_EXTENSION}"
        cls.full_path = cls.user_input.directory + cls.original_file_name

    def setUp(self):
        self.episode_number = 5
        self.episode_precision = 1

    def get_expected_episode_number(self):
        return str(self.episode_number).zfill(self.episode_precision)

    def validate_new_file_name_calculation(self, calculated_file_name):
        # Assert
        expected_episode_number = self.get_expected_episode_number()
        expected_file_name = f"{self.user_input.prefix}{expected_episode_number}{FILES_EXTENSION}"
        self.assertEqual(expected_file_name, calculated_file_name)

    def test_calculate_new_file_name_with_single_digit_episode_precision(self):
        self.episode_number = 5
        self.episode_precision = 1
        # Act
        calculated_file_name = calculate_new_file_name(self.user_input.prefix, self.full_path, episode_number,
                                                       episode_precision)
        # Assert
        self.validate_new_file_name_calculation(
            calculated_file_name, self.episode_precision, self.episode_number)

    def test_calculate_new_file_name_with_multiple_digits_episode_precision(self):
        # Arrange
        self.episode_precision = 3
        # Act
        calculated_file_name = calculate_new_file_name(self.user_input.prefix, self.full_path, self.episode_number,
                                                       self.episode_precision)
        # Assert
        self.validate_new_file_name_calculation(
            calculated_file_name, self.episode_precision, self.episode_number)

    def test_calculate_single_digit_episode_precision(self):
        # Arrange
        file_names_collection = build_file_names_collection(
            FILES_NAME_PREFIX, 3)
        # Act
        episode_precision = calculate_episode_precision(file_names_collection)
        # Assert
        expected_precision = 1
        self.assertEqual(expected_precision, episode_precision)

    def test_calculate_multiple_digits_episode_precision(self):
        # Arrange
        file_names_collection = build_file_names_collection(
            FILES_NAME_PREFIX, 125)
        # Act
        episode_precision = calculate_episode_precision(file_names_collection)
        # Assert
        expected_precision = 3
        self.assertEqual(expected_precision, episode_precision)

    def test_calculate_border_multiple_digits_episode_precision(self):
        # Arrange
        file_names_collection = build_file_names_collection(
            FILES_NAME_PREFIX, 10)
        # Act
        episode_precision = calculate_episode_precision(file_names_collection)
        # Assert
        expected_precision = 2
        self.assertEqual(expected_precision, episode_precision)


class SeriesRenamerTestsBaseClass:
    def build_checked_file_path(self, file_name):
        return self.user_input.directory + file_name + FILES_EXTENSION

    def build_expected_file_path(self, episode_number):
        return self.user_input.directory + self.user_input.prefix + episode_number + FILES_EXTENSION

    def create_input_file(self, file_name):
        file_path = self.build_checked_file_path(file_name)
        self.fs.create_file(file_path)
        self.assertTrue(path.exists(file_path))

    def create_input_files(self, file_names):
        for file_name in file_names:
            self.create_input_file(file_name)

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

    def validate_format_change(self, original_file_name, episode_number, episode_precision):
        episode_number = f"{episode_number}".zfill(episode_precision)
        self.validate_old_file_name_deletion(original_file_name)
        self.validate_new_file_name_creation(episode_number)

    def add_invalid_directory(self):
        self.is_input_invalid = True
        self.user_input.directory = "5"

    def test_change_file_name_to_single_digit_episode_name(self):
        file_name = f"{FILES_NAME_PREFIX}55"
        episode_number = 8
        episode_precision = 1
        self.create_input_file(file_name)
        change_file_name_format(file_name + FILES_EXTENSION,
                                episode_number, episode_precision, self.user_input)
        self.validate_format_change(
            file_name, episode_number, episode_precision)

    def test_change_file_name_to_multiple_digits_episode_name(self):
        file_name = f"{FILES_NAME_PREFIX}11"
        episode_number = 23
        episode_precision = 2
        self.create_input_file(file_name)
        change_file_name_format(file_name + FILES_EXTENSION,
                                episode_number, episode_precision, self.user_input)
        self.validate_format_change(
            file_name, episode_number, episode_precision)

    @patch("src.main.change_file_name_format")
    def test_change_files_name_format(self, mocked_file_name_format_changer):
        file_names_collection = build_file_names_collection(
            FILES_NAME_PREFIX, 7)
        self.create_input_files(file_names_collection)
        change_files_name_format(self.user_input)
        expected_episode_precision = 1
        mocked_file_name_format_changer.assert_has_calls([call(f"{FILES_NAME_PREFIX}{file_index}{FILES_EXTENSION}",
                                                               self.user_input,
                                                               file_index + 1,
                                                               expected_episode_precision)
                                                          for file_index in range(len(file_names_collection))])

    @patch("src.main.change_file_name_format")
    def test_change_files_name_format_with_invalid_directory(self, mocked_file_name_format_changer):
        self.add_invalid_directory()
        file_names_collection = build_file_names_collection(
            FILES_NAME_PREFIX, 4)
        self.create_input_files(file_names_collection)
        change_files_name_format(self.user_input)
        mocked_file_name_format_changer.assert_not_called()


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
