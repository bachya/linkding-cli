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
  * [Main Help](#main-help)
  * [Configuration](#configuration)
    + [Example: CLI Options](#example--cli-options)
    + [Example: Environment Variables](#example--environment-variables)
    + [Example: Configuration File](#example--configuration-file)
    + [Merging Configuration Options](#merging-configuration-options)
  * [Bookmarks](#bookmarks)
    + [The `bookmarks all` command](#the-bookmarks-all-command)
    + [The `bookmarks archive` command](#the-bookmarks-archive-command)
    + [The `bookmarks create` command](#the-bookmarks-create-command)
    + [The `bookmarks delete` command](#the-bookmarks-delete-command)
    + [The `bookmarks get` command](#the-bookmarks-get-command)
    + [The `bookmarks unarchive` command](#the-bookmarks-unarchive-command)
    + [The `bookmarks update` command](#the-bookmarks-update-command)
  * [Tags](#tags)
    + [The `tags all` command](#the-tags-all-command)
    + [The `tags create` command](#the-tags-create-command)
    + [The `tags get` command](#the-tags-get-command)
  * [Misc.](#misc)
    + [Parsing and Pretty Printing Data](#parsing-and-pretty-printing-data)
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

## Main Help

```
$ linkding --help
Usage: linkding [OPTIONS] COMMAND [ARGS]...

  Interact with a linkding instance.

Options:
  -c, --config PATH     A path to a config file.  [env var: LINKDING_CONFIG]
  -t, --token TOKEN     A linkding API token.  [env var: LINKDING_TOKEN]
  -u, --url URL         A URL to a linkding instance.  [env var: LINKDING_URL]
  -v, --verbose         Increase verbosity of standard output.
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  bookmarks  Work with bookmarks.
  tags       Work with tags.
  ```

## Configuration

Configuration can be provided via a variety of sources:

* CLI Options
* Environment Variables
* Configuration File

### Example: CLI Options

```
$ linkding -u http://127.0.0.1:8000 -t abcde12345 ...
```

### Example: Environment Variables

```
$ LINKDING_URL=http://127.0.0.1:8000 LINKDING_TOKEN=abcde12345 linkding ...
```

### Example: Configuration File

The configuration file can be formatted as either JSON:

```json
{
  "token": "abcde12345",
  "url": "http://127.0.0.1:8000",
  "verbose": false
}
```

...or YAML

```yaml
---
token: "abcde12345"
url: "http://127.0.0.1:8000"
verbose: false
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

## Bookmarks

```
Usage: linkding bookmarks [OPTIONS] COMMAND [ARGS]...

  Work with bookmarks.

Options:
  --help  Show this message and exit.

Commands:
  all        Get all bookmarks.
  archive    Archive a bookmark by its linkding ID.
  create     Create a bookmark.
  delete     Delete a bookmark by its linkding ID.
  get        Get a bookmark by its linkding ID.
  unarchive  Unarchive a bookmark by its linkding ID.
  update     Update a bookmark by its linkding ID.
  ```

### The `bookmarks all` command

```
Usage: linkding bookmarks all [OPTIONS]

  Get all bookmarks.

Options:
  -a, --archived        Return archived bookmarks.
  -l, --limit INTEGER   The number of bookmarks to return.
  -o, --offset INTEGER  The index from which to return results.
  -q, --query TEXT      Return bookmarks containing a query string.
  --help                Show this message and exit.
  ```

#### Examples:

```sh
# Get all bookmarks, but limit the results to 10:
$ linkding bookmarks all --limit 10

# Get all archived bookmarks that contain "software":
$ linkding bookmarks all --archived --query software
```

### The `bookmarks archive` command

```
Usage: linkding bookmarks archive [OPTIONS] [BOOKMARK_ID]

  Archive a bookmark by its linkding ID.

Arguments:
  [BOOKMARK_ID]  The ID of a bookmark to archive.

Options:
  --help  Show this message and exit.
  ```

#### Examples:

```sh
# Archive bookmark 12:
$ linkding bookmarks archive 12
```

### The `bookmarks create` command

```
Usage: linkding bookmarks create [OPTIONS] URL

  Create a bookmark.

Arguments:
  URL  The URL to bookmark.  [required]

Options:
  -d, --description DESCRIPTION  The description to give the bookmark.
  --tags TAG1,TAG2,...           The tags to apply to the bookmark.
  -t, --title TITLE              The title to give the bookmark.
  --help                         Show this message and exit.
  ```

#### Examples:

```sh
# Create a bookmark:
$ linkding bookmarks create https://example.com

# Create a bookmark with title, description, and tags:
$ linkding bookmarks create https://example.com -t Example -d "A description" --tags tag1,tag2
```

### The `bookmarks delete` command

```
Usage: linkding bookmarks delete [OPTIONS] [BOOKMARK_ID]

  Delete a bookmark by its linkding ID.

Arguments:
  [BOOKMARK_ID]  The ID of a bookmark to delete.

Options:
  --help  Show this message and exit.
  ```

#### Examples:

```sh
# Delete the bookmark with an ID of 12:
$ linkding bookmarks delete 12
```

### The `bookmarks get` command

```
Usage: linkding bookmarks get [OPTIONS] [BOOKMARK_ID]

  Get a bookmark by its linkding ID.

Arguments:
  [BOOKMARK_ID]  The ID of a bookmark to retrieve.

Options:
  --help  Show this message and exit.
  ```

#### Examples:

```sh
# Get bookmark 12:
$ linkding bookmarks get 12
```

### The `bookmarks unarchive` command

```
Usage: linkding bookmarks unarchive [OPTIONS] [BOOKMARK_ID]

  Unarchive a bookmark by its linkding ID.

Arguments:
  [BOOKMARK_ID]  The ID of a bookmark to unarchive.

Options:
  --help  Show this message and exit.
  ```

#### Examples:

```sh
# Unarchive bookmark 12:
$ linkding bookmarks unarchive 12
```

### The `bookmarks update` command

```
Usage: linkding bookmarks update [OPTIONS] BOOKMARK_ID

  Update a bookmark by its linkdingn ID.

Arguments:
  BOOKMARK_ID  The ID of a bookmark to update.  [required]

Options:
  -u, --url URL                  The URL to assign to the bookmark.
  -d, --description DESCRIPTION  The description to give the bookmark.
  --tags TAG1,TAG2,...           The tags to apply to the bookmark.
  -t, --title TITLE              The title to give the bookmark.
  --help                         Show this message and exit.
  ```

#### Examples:

```sh
# Update a bookmark with a new url:
$ linkding bookmarks update 12 -u https://example.com

# Update a bookmark with title, description, and tags:
$ linkding bookmarks update 12 -t Example -d "A description" --tags tag1,tag2
```

## Tags

```
Usage: linkding tags [OPTIONS] COMMAND [ARGS]...

  Work with tags.

Options:
  --help  Show this message and exit.

Commands:
  all     Get all tags.
  create  Create a tag.
  get     Get a tag by its linkding ID.
  ```

### The `tags all` command

```
Usage: linkding tags all [OPTIONS]

  Get all tags.

Options:
  -l, --limit INTEGER   The number of tags to return.
  -o, --offset INTEGER  The index from which to return results.
  --help                Show this message and exit.
  ```

#### Examples:

```sh
# Get all tags, but limit the results to 10:
$ linkding tags all --limit 10
```

### The `tags create` command

```
Usage: linkding tags create [OPTIONS] TAG_NAME

  Create a tag.

Arguments:
  TAG_NAME  The tag to create.  [required]

Options:
  --help  Show this message and exit.
  ```

#### Examples:

```sh
# Create a tag:
$ linkding tags create sample-tag
```

### The `tags get` command

```
Usage: linkding tags get [OPTIONS] TAG_ID

  Get a tag by its linkding ID.

Arguments:
  TAG_ID  The ID of a tag to retrieve.  [required]

Options:
  --help  Show this message and exit.
  ```

#### Examples:

```sh
# Get tag 12:
$ linkding tags get 12
```

## Misc.

### Parsing and Pretty Printing Data

`linkding-cli` doesn't have built-in utilities for modifying JSON output in any way.
Instead, it's recommended to use a tool like [`jq`](https://stedolan.github.io/jq/).
This allows for multiple new outcomes, like pretty-printing:

```
$ linkding bookmarks all | jq
{
  "count": 123,
  "next": "http://127.0.0.1:8000/api/bookmarks/?limit=100&offset=100",
  "previous": null,
  "results": [
    {
      "id": 1,
      "url": "https://example.com",
      "title": "Example title",
      "description": "Example description",
      "website_title": "Website title",
      "website_description": "Website description",
      "tag_names": [
        "tag1",
        "tag2"
      ],
      "date_added": "2020-09-26T09:46:23.006313Z",
      "date_modified": "2020-09-26T16:01:14.275335Z"
    }
  ]
}
```

...and slicing/parsing data:

```
$ linkding bookmarks all | jq '.results[0].title'
"Example title"
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
