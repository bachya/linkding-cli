"""Define tag commands."""
import typer

TAG_APP = typer.Typer()


def get_all() -> None:
    """Get all tags."""
    typer.echo("PLACEHOLDER")


TAG_APP.command(name="all")(get_all)
