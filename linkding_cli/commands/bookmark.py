"""Define the bookmark command."""
from __future__ import annotations

import asyncio
import json

import typer

from linkding_cli.const import CONF_LIMIT, CONF_OFFSET
from linkding_cli.helpers.logging import log_exception
from linkding_cli.util import generate_api_payload

CONF_ARCHIVED = "archived"
CONF_DESCRIPTION = "description"
CONF_QUERY = "query"
CONF_SHARED = "shared"
CONF_TAG_NAMES = "tag_names"
CONF_TITLE = "title"
CONF_UNREAD = "unread"
CONF_URL = "url"


@log_exception()
def archive(
    ctx: typer.Context,
    bookmark_id: int = typer.Argument(..., help="The ID of a bookmark to archive."),
) -> None:
    """Archive a bookmark by its linkding ID.

    Args:
        ctx: A Typer Context object.
        bookmark_id: The ID of the bookmark to archive.
    """
    asyncio.run(ctx.obj.client.bookmarks.async_archive(bookmark_id))
    typer.echo(f"Bookmark {bookmark_id} archived.")


@log_exception()
def create(
    ctx: typer.Context,
    url: str = typer.Argument(..., help="The URL to bookmark."),
    archived: bool = typer.Option(
        False,
        "--archived",
        "-a",
        help="Whether the newly-created bookmark should be immediately archived.",
    ),
    description: str = typer.Option(
        None,
        "--description",
        "-d",
        help="The description to give the bookmark.",
        metavar="DESCRIPTION",
    ),
    shared: bool = typer.Option(
        False,
        "--shared",
        help=(
            "Whether the newly-created bookmark should be shareable with other users"
        ),
    ),
    tag_names: str = typer.Option(
        None,
        "--tags",
        help="The tags to apply to the bookmark.",
        metavar="TAG1,TAG2,...",
    ),
    title: str = typer.Option(
        None,
        "--title",
        "-t",
        help="The title to give the bookmark.",
        metavar="TITLE",
    ),
    unread: bool = typer.Option(
        False,
        "--unread",
        help="Whether the newly-created bookmark should be marked as unread.",
    ),
) -> None:
    """Create a bookmark.

    Args:
        ctx: A Typer Context object.
        url: The URL to bookmark.
        archived: Whether the newly-created bookmark should be immediately archived.
        description: The description to give the bookmark.
        shared: Whether the newly-created bookmark should be shareable with other users.
        tag_names: The tags to apply to the bookmark.
        title: The title to give the bookmark.
        unread: Whether to mark the bookmark as unread.
    """
    if tag_names:
        tags = tag_names.split(",")
    else:
        tags = None

    payload = generate_api_payload(
        (
            (CONF_ARCHIVED, archived),
            (CONF_DESCRIPTION, description),
            (CONF_SHARED, shared),
            (CONF_TAG_NAMES, tags),
            (CONF_TITLE, title),
            (CONF_UNREAD, unread),
        )
    )

    data = asyncio.run(ctx.obj.client.bookmarks.async_create(url, **payload))
    typer.echo(json.dumps(data))


@log_exception()
def delete(
    ctx: typer.Context,
    bookmark_id: int = typer.Argument(..., help="The ID of a bookmark to delete."),
) -> None:
    """Delete a bookmark by its linkding ID.

    Args:
        ctx: A Typer Context object.
        bookmark_id: The ID of the bookmark to delete.
    """
    asyncio.run(ctx.obj.client.bookmarks.async_delete(bookmark_id))
    typer.echo(f"Bookmark {bookmark_id} deleted.")


@log_exception()
def get_all(
    ctx: typer.Context,
    archived: bool = typer.Option(
        False,
        "--archived",
        "-a",
        help="Return archived bookmarks.",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        "-l",
        help="The number of bookmarks to return.",
    ),
    offset: int = typer.Option(
        None,
        "--offset",
        "-o",
        help="The index from which to return results.",
    ),
    query: str = typer.Option(
        None,
        "--query",
        "-q",
        help="Return bookmarks containing a query string.",
        metavar="QUERY",
    ),
) -> None:
    """Get all bookmarks.

    Args:
        ctx: A Typer Context object.
        archived: Return archived bokomarks.
        limit: The number of bookmarks to return.
        offset: The index from which to return results.
        query: Return bookmarks containing a query string.
    """
    api_kwargs = generate_api_payload(
        (
            (CONF_LIMIT, limit),
            (CONF_OFFSET, offset),
            (CONF_QUERY, query),
        )
    )

    if archived:
        api_func = ctx.obj.client.bookmarks.async_get_archived
    else:
        api_func = ctx.obj.client.bookmarks.async_get_all
    data = asyncio.run(api_func(**api_kwargs))
    typer.echo(json.dumps(data))


@log_exception()
def get_by_id(
    ctx: typer.Context,
    bookmark_id: int = typer.Argument(..., help="The ID of a bookmark to retrieve."),
) -> None:
    """Get a bookmark by its linkding ID.

    Args:
        ctx: A Typer Context object.
        bookmark_id: The ID of the bookmark to retrieve.
    """
    data = asyncio.run(ctx.obj.client.bookmarks.async_get_single(bookmark_id))
    typer.echo(json.dumps(data))


@log_exception()
def main(_: typer.Context) -> None:
    """Interact with bookmarks."""
    pass


@log_exception()
def unarchive(
    ctx: typer.Context,
    bookmark_id: int = typer.Argument(..., help="The ID of a bookmark to archive."),
) -> None:
    """Unarchive a bookmark by its linkding ID.

    Args:
        ctx: A Typer Context object.
        bookmark_id: The ID of the bookmark to archive.
    """
    asyncio.run(ctx.obj.client.bookmarks.async_unarchive(bookmark_id))
    typer.echo(f"Bookmark {bookmark_id} unarchived.")


@log_exception()
def update(
    ctx: typer.Context,
    bookmark_id: int = typer.Argument(..., help="The ID of a bookmark to update."),
    url: str = typer.Option(
        None,
        "--url",
        "-u",
        help="The URL to assign to the bookmark.",
        metavar="URL",
    ),
    description: str = typer.Option(
        None,
        "--description",
        "-d",
        help="The description to give the bookmark.",
        metavar="DESCRIPTION",
    ),
    shared: bool = typer.Option(
        False,
        "--shared",
        help=("Whether the -created bookmark should be shareable with other users"),
    ),
    tag_names: str = typer.Option(
        None,
        "--tags",
        help="The tags to apply to the bookmark.",
        metavar="TAG1,TAG2,...",
    ),
    title: str = typer.Option(
        None,
        "--title",
        "-t",
        help="The title to give the bookmark.",
        metavar="TITLE",
    ),
    unread: bool = typer.Option(
        False,
        "--unread",
        help="Whether the bookmark should be marked as unread.",
    ),
) -> None:
    """Update a bookmark by its linkding ID.

    Args:
        ctx: A Typer Context object.
        bookmark_id: The ID of a bookmark to update.
        url: The URL to bookmark.
        description: The description to give the bookmark.
        shared: Whether the newly-created bookmark should be shareable with other users.
        tag_names: The tags to apply to the bookmark.
        title: The title to give the bookmark.
        unread: Whether to mark the bookmark as unread.
    """
    if tag_names:
        tags = tag_names.split(",")
    else:
        tags = None

    payload = generate_api_payload(
        (
            (CONF_DESCRIPTION, description),
            (CONF_SHARED, shared),
            (CONF_TAG_NAMES, tags),
            (CONF_TITLE, title),
            (CONF_UNREAD, unread),
            (CONF_URL, url),
        )
    )

    data = asyncio.run(ctx.obj.client.bookmarks.async_update(bookmark_id, **payload))
    typer.echo(json.dumps(data))


BOOKMARK_APP = typer.Typer(callback=main)
BOOKMARK_APP.command(name="all")(get_all)
BOOKMARK_APP.command(name="archive")(archive)
BOOKMARK_APP.command(name="create")(create)
BOOKMARK_APP.command(name="delete")(delete)
BOOKMARK_APP.command(name="get")(get_by_id)
BOOKMARK_APP.command(name="unarchive")(unarchive)
BOOKMARK_APP.command(name="update")(update)
