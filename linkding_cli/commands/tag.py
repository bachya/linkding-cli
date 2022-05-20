"""Define the tag command."""
import typer


def get_all(ctx: typer.Context) -> None:
    """Get all tags."""
    typer.echo("PLACEHOLDER")


TAG_APP = typer.Typer()
TAG_APP.command(name="all")(get_all)
