# 🔖 linkding-cli: A CLI to interact with a linkding instance

[![CI](https://github.com/bachya/linkding-cli/workflows/CI/badge.svg)](https://github.com/bachya/linkding-cli/actions)
[![PyPi](https://img.shields.io/pypi/v/linkding-cli.svg)](https://pypi.python.org/pypi/linkding-cli)
[![Version](https://img.shields.io/pypi/pyversions/linkding-cli.svg)](https://pypi.python.org/pypi/linkding-cli)
[![License](https://img.shields.io/pypi/l/linkding-cli.svg)](https://github.com/bachya/linkding-cli/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/linkding-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/linkding-cli)
[![Maintainability](https://api.codeclimate.com/v1/badges/f01be3cd230902508636/maintainability)](https://codeclimate.com/github/bachya/linkding-cli/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`linkding-cli` is a CLI to interact with a linkding instance.

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Usage](#usage)
  * [linkding Configuration Parameters](#linkding-configuration-parameters)
  * [Managing Bookmarks](#managing-bookmarks)
  * [Managing Tags](#managing-tags)
- [Contributing](#contributing)

# Installation

```python
pip install linkding-cli
```

# Python Versions

`linkding-cli` is currently supported on:

* Python 3.8
* Python 3.9
* Python 3.10

# Usage

Usage instructions are provided via the `--help` option (either on the main `linkding`
executable or on any of its commands):

```
$ linkding --help
Usage: linkding [OPTIONS] COMMAND [ARGS]...

  Interact with a linkding instance.

Options:
  -u, --url URL         A URL to a linkding instance.  [env var: LINKDING_URL]
  -t, --token TOKEN     A linkding API token.  [env var: LINKDING_TOKEN]
  -v, --verbose         Increase verbosity of standard output.
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  bookmarks  Manage bookmarks
  tags       Manage tags
```

## linkding Configuration Parameters

`linkding-cli` requires two configuration parameters in order to run:

* A URL to a linkding instance
* A linkding API token

These can be provided via multiple sources:

* CLI Options
* Environment Variables
* Configuration File

### CLI Options

* The linkding URL can be provided via either `-u` or `--url`.
* The linkding API token can be provided via either `-t` or `--token`.

```
$ linkding -u http://127.0.0.1:8000 -t abcde12345 ...
```

### Environment Variables

* The linkding URL can be provided via the `LINKDING_URL` environment variable.
* The linkding API token can be provided via the `LINKDING_TOKEN` environment variable.

```
$ LINKDING_URL=http://127.0.0.1:8000 LINKDING_TOKEN=abcde12345 linkding ...
```

### Configuration File

The configuration file can be formatted as either JSON:

```json
{
  "token": "abcde12345",
  "url": "http://127.0.0.1:8000"
}
```

...or YAML

```yaml
---
token: "abcde12345"
url: "http://127.0.0.1:8000"
```

Then, the linkding file can be provided via either `-c` or `--config`.

```
$ linkding -c ~/.config/linkding.json ...
```

### Merging Configuration Options

When parsing configuration options, `linkding-cli` looks at the configuration sources in
the following order:

1. Configuration File
2. Environment Variables
3. CLI Options

This allows you to mix and match sources – for instance, you might have "defaults" in
the configuration file and override them via environment variables.

## Managing Bookmarks

```
$ linkding bookmarks --help
Usage: linkding bookmarks [OPTIONS] COMMAND [ARGS]...

  Manage bookmarks

Options:
  --help  Show this message and exit.

Commands:
  all  Get all bookmarks.
```

## Managing Tags

```
$ linkding tags --help
Usage: linkding tags [OPTIONS] COMMAND [ARGS]...

  Manage bookmarks

Options:
  --help  Show this message and exit.

Commands:
  all  Get all tags.
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/linkding-cli/issues)
  or [initiate a discussion on one](https://github.com/bachya/linkding-cli/issues/new).
2. [Fork the repository](https://github.com/bachya/linkding-cli/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `nox -rs coverage`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
