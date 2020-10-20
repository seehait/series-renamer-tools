from math import ceil, log10
from os import listdir, path, rename
from pathlib import Path
from sys import argv
from src.utils import parse_args

from natsort import natsorted

FIRST_EPISODE_NUMBER = 1


def calculate_new_file_name(prefix, full_path, current_episode, episode_precision):
    extension = Path(full_path).suffix
    formatted_episode_number = f"{current_episode}".zfill(
        episode_precision)
    return f"{prefix}{formatted_episode_number}{extension}"


def calculate_episode_precision(file_names):
    return ceil(log10(len(file_names) + 1))


def change_file_name_format(file_name, episode_number, episode_precision, parsed_args):
    full_path = path.join(parsed_args.directory, file_name)

    new_file_name = calculate_new_file_name(
        parsed_args.prefix, full_path, episode_number, episode_precision)
    print(f"{file_name}\t=>\t{new_file_name}")

    if not parsed_args.dry_run:
        rename(full_path, path.join(parsed_args.directory, new_file_name))


def change_files_name_format(parsed_args):
    if not path.isdir(parsed_args.directory):
        print(f"received invalid directory path: {parsed_args.directory}")
        return

    file_names = natsorted(listdir(parsed_args.directory))
    episode_precision = calculate_episode_precision(file_names)

    for episode_number, file_name in enumerate(file_names, FIRST_EPISODE_NUMBER):
        change_file_name_format(file_name, episode_number,
                                episode_precision, parsed_args)


def main():
    change_files_name_format(parse_args(argv[1:]))


if __name__ == '__main__':
    main()
