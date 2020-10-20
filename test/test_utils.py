import unittest
from src.utils import parse_args, DIRECTORY_PARAMETER_VALID_KEYS, PREFIX_PARAMETER_VALID_KEYS,\
    DRY_RUN_PARAMETER_VALID_KEYS
from os import path


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prefix_name = "wheel_of_fortune"
        cls.non_default_input_directory_suffix = "/parse_test/"
        cls.non_default_full_input_directory = path.realpath(
            cls.non_default_input_directory_suffix)
        cls.expected_default_directory = path.dirname(path.realpath(__file__))
        cls.directory_parameter_key = DIRECTORY_PARAMETER_VALID_KEYS[0]
        cls.prefix_parameter_key = PREFIX_PARAMETER_VALID_KEYS[0]
        cls.dry_run_parameter_key = DRY_RUN_PARAMETER_VALID_KEYS[0]

    def validate_parsed_input_content(self, user_input, expected_directory, expected_prefix, is_dry_run):
        self.assertEqual(user_input.directory, expected_directory)
        self.assertEqual(user_input.prefix, expected_prefix)
        self.assertEqual(user_input.dry_run, is_dry_run)

    def test_parse_args_with_default_directory_and_dry_run(self):
        user_input = parse_args([self.prefix_parameter_key, self.prefix_name])
        self.validate_parsed_input_content(
            user_input, self.expected_default_directory, self.prefix_name, False)

    def test_parse_args_with_default_directory(self):
        user_input = parse_args(
            [self.prefix_parameter_key, self.prefix_name, self.dry_run_parameter_key])
        self.validate_parsed_input_content(
            user_input, self.expected_default_directory, self.prefix_name, True)

    def test_parse_args_with_default_dry_run(self):
        user_input = parse_args([self.directory_parameter_key, self.non_default_input_directory_suffix,
                                 self.prefix_parameter_key, self.prefix_name])
        self.validate_parsed_input_content(
            user_input, self.non_default_full_input_directory, self.prefix_name, False)

    def test_parse_args_with_non_default_parameters(self):
        user_input = parse_args([self.directory_parameter_key, self.non_default_input_directory_suffix,
                                 self.prefix_parameter_key, self.prefix_name, self.dry_run_parameter_key])
        self.validate_parsed_input_content(
            user_input, self.non_default_full_input_directory, self.prefix_name, True)
