from argparse import ArgumentParser
from os import path

DIRECTORY_PARAMETER_VALID_KEYS = ['--directory', '-d']
PREFIX_PARAMETER_VALID_KEYS = ['--prefix', '-p']
DRY_RUN_PARAMETER_VALID_KEYS = ['--dry-run', '-dr']


def parse_args(argv):
    parser = ArgumentParser(
        description='Series Renamer: rename files of series with respect to episode number.')
    parser.add_argument(*DIRECTORY_PARAMETER_VALID_KEYS, dest='directory',
                        metavar='[path/to/target/directory]', type=str, required=False, default='.',
                        help='path to target directory')
    parser.add_argument(*PREFIX_PARAMETER_VALID_KEYS, dest='prefix',
                        metavar='[Series Name S01 E]', type=str, required=True,
                        help='name prefix before episode number')
    parser.add_argument(*DRY_RUN_PARAMETER_VALID_KEYS, dest='dry_run',
                        action='store_true', help='dry run')

    parsed_args = parser.parse_args(argv)
    parsed_args.directory = path.realpath(parsed_args.directory)
    return parsed_args
