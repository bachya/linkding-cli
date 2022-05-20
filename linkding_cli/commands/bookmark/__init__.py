"""Define the bookmark command."""
import typer

from linkding_cli.commands.bookmark.all import BOOKMARK_ALL_APP

BOOKMARK_APP = typer.Typer()
BOOKMARK_APP.add_typer(
    BOOKMARK_ALL_APP, name="all", help="Operations for dealing with all bookmarks"
)
