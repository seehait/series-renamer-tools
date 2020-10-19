from argparse import ArgumentParser
from math import ceil, log10
from os import listdir, path, rename
from pathlib import Path
from sys import argv

from natsort import natsorted

FIRST_EPISODE_NUMBER = 1


def parse_args(argv):
    parser = ArgumentParser(
        description='Series Renamer: rename files of series with respect to episode number.')
    parser.add_argument('--directory', '-d', dest='directory',
                        metavar='[path/to/target/directory]', type=str, required=False, default='.', help='path to target directory')
    parser.add_argument('--prefix', '-p', dest='prefix',
                        metavar='[Series Name S01 E]', type=str, required=True, help='name prefix before episode number')
    parser.add_argument('--dry-run', '-dr', dest='dry_run',
                        action='store_true', help='dry run')

    parsed_args = parser.parse_args(argv)
    parsed_args.directory = path.realpath(parsed_args.directory)
    return parsed_args


def calculate_new_file_name(prefix, full_path, current_episode, episode_precision):
    extension = Path(full_path).suffix
    formatted_episode_number = f"{current_episode}".zfill(
        episode_precision)
    return f"{prefix}{formatted_episode_number}{extension}"


def calculate_episode_precision(file_names):
    return ceil(log10(len(file_names) + 1))


def change_file_name_format(file_name, parsed_args, current_episode, episode_precision):
    full_path = path.join(parsed_args.directory, file_name)
    if not path.isfile(full_path):
        return

    new_file_name = calculate_new_file_name(parsed_args.prefix, full_path, current_episode, episode_precision)
    print(f"{file_name}\t=>\t{new_file_name}")

    if parsed_args.dry_run:
        return
    rename(full_path, path.join(parsed_args.directory, new_file_name))


def change_files_name_format(parsed_args):
    file_names = natsorted(listdir(parsed_args.directory))
    episode_precision = calculate_episode_precision(file_names)

    for current_episode, file_name in enumerate(file_names, FIRST_EPISODE_NUMBER):
        change_file_name_format(file_name, parsed_args, current_episode, episode_precision)


def main():
    change_files_name_format(parse_args(argv[1:]))


if __name__ == '__main__':
    main()
