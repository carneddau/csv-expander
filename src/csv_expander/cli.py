from pathlib import Path

from typer import Exit, Option, Typer

from .expand import expand_csv
from .utils import console, version

# Allow invocation without subcommand so --version option does not produce an error
interface = Typer(invoke_without_command=True, no_args_is_help=True)


@interface.callback()
def version_callback(
    print_version: bool = Option(False, "--version", "-v", is_eager=True),
):
    if print_version:
        console.print(version())
        raise Exit()


@interface.command()
def expand(
    data: Path = Option(
        ...,
        "-f",
        "--file",
        exists=True,
        readable=True,
        resolve_path=True,
        dir_okay=False,
        help="CSV file to be expanded.",
    ),
    backup: bool = Option(
        True,
        help="Whether or not to backup csv file. File will be copied with a '.old' extension.",
    ),
):
    expand_csv(data, backup)


def cli():
    """Run the CLI tool"""
    interface()
