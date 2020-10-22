from pyfakefs.fake_filesystem_unittest import TestCase
from src.utils import parse_args, DIRECTORY_PARAMETER_VALID_KEYS, PREFIX_PARAMETER_VALID_KEYS,\
    DRY_RUN_PARAMETER_VALID_KEYS
from os import path


class TestUtils(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prefix_name = "wheel_of_fortune"
        cls.non_default_directory_component = "parse_test"
        cls.non_default_input_directory = path.sep + cls.non_default_directory_component + path.sep
        cls.non_default_full_input_directory = path.join(path.sep, cls.non_default_directory_component)
        cls.directory_parameter_key = DIRECTORY_PARAMETER_VALID_KEYS[0]
        cls.prefix_parameter_key = PREFIX_PARAMETER_VALID_KEYS[0]
        cls.dry_run_parameter_key = DRY_RUN_PARAMETER_VALID_KEYS[0]

    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory(path.dirname(path.realpath(__file__)))
        self.expected_default_directory = path.sep

    def validate_parsed_input_content(self, user_input, expected_directory, expected_prefix, is_dry_run):
        self.assertEqual(expected_directory, user_input.directory)
        self.assertEqual(expected_prefix, user_input.prefix)
        self.assertEqual(is_dry_run, user_input.dry_run)

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
        user_input = parse_args([self.directory_parameter_key, self.non_default_input_directory,
                                 self.prefix_parameter_key, self.prefix_name])
        self.validate_parsed_input_content(
            user_input, self.non_default_full_input_directory, self.prefix_name, False)

    def test_parse_args_with_non_default_parameters(self):
        user_input = parse_args([self.directory_parameter_key, self.non_default_input_directory,
                                 self.prefix_parameter_key, self.prefix_name, self.dry_run_parameter_key])
        self.validate_parsed_input_content(
            user_input, self.non_default_full_input_directory, self.prefix_name, True)
