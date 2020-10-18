# Series Renamer Tools

[![Travis](https://travis-ci.com/seehait/series-renamer-tools.svg?branch=master)](https://travis-ci.com/seehait/series-renamer-tools)
[![GitHub license](https://img.shields.io/github/license/seehait/series-renamer-tools.svg)](https://github.com/seehait/series-renamer-tools/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/series-renamer-tools.svg)](https://pypi.org/project/series-renamer-tools)

Bulk changing file names into prettier format.

## Table of Contents

- [Requirement](#requirement)
- [Installation](#installation)
  - [Installing from PyPI](#installing-from-pypi)
  - [Installing from Git](#installing-from-git)
- [Usage](#usage)
  - [Options](#options)
  - [YAML Input](#yaml-input)
- [License](#license)

## Requirement

- Python 3.6+

## Installation

### Installing from PyPI

```sh
pip3 install series-renamer-tools
```

### Installing from Git

```sh
python3 setup.py install
```

## Usage

```sh
series-renamers --directory [path/to/target/directory] --prefix 'Series S01 E' [--dry-run]
```

### Options
| Name                | Type      | Description              | Required | Default           |
| ------------------- | --------- | ------------------------ | -------- |-------------------|
| `--directory`, `-d` | `string`  | path to target directory | `false`  | current directory |
| `--prefix`, `-p`    | `string`  | new file name prefix     | `true`   |                   |
| `--dry-run`, `-dr`  | `boolean` | only preview the results | `false`  | `false`           |

## License

Series Renamer Tools is an open-source tool licensed under [MIT License](LICENSE).
