"""CLI entry point using Click."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from loguru import logger

from second_brain.app import configure_logging
from second_brain.notes import create_note


@click.group()
def cli():
    """second_brain -- capture and organise your thoughts."""
    configure_logging()


@cli.command()
@click.argument("title")
@click.option("--content", "-c", default=None, help="Note body content.")
@click.option(
    "--from-file",
    "from_file",
    type=click.Path(exists=True),
    default=None,
    help="Read body content from file.",
)
def new(title: str, content: str | None, from_file: str | None):
    """Create a new note with the given TITLE."""
    base_dir = Path(
        os.environ.get("SECOND_BRAIN_DIR", str(Path.home() / "second_brain"))
    ).expanduser()

    stdin_data = None if sys.stdin.isatty() else sys.stdin.read()

    active_sources = sum(x is not None for x in [content, from_file, stdin_data])
    if active_sources > 1:
        click.echo(
            "Warning: multiple body sources provided; using --content > --from-file > stdin.",
            err=True,
        )

    if content is not None:
        body = content
    elif from_file is not None:
        body = Path(from_file).read_text(encoding="utf-8")
    else:
        body = stdin_data

    logger.debug("Creating note in {}", base_dir)
    path = create_note(title, base_dir, body=body)
    logger.info("Created note: {}", path)
    click.echo(path)


@cli.command("list")
def list_notes():
    """List all notes in the notes directory."""
    base_dir = Path(
        os.environ.get("SECOND_BRAIN_DIR", str(Path.home() / "second_brain"))
    ).expanduser()

    if not base_dir.is_dir():
        logger.warning("Notes directory does not exist: {}", base_dir)
        click.echo(f"Notes directory does not exist: {base_dir}")
        return

    files = sorted(base_dir.glob("*.md"), reverse=True)

    click.echo(f"Notes: {base_dir}")

    if not files:
        logger.info("No notes found in {}", base_dir)
        click.echo("No notes found.")
        return

    logger.debug("Found {} note(s) in {}", len(files), base_dir)
    for i, f in enumerate(files, 1):
        click.echo(f"{i}. {f.name}")


@cli.command()
@click.argument("number", type=int)
def show(number: int):
    """Display the contents of note NUMBER."""
    base_dir = Path(
        os.environ.get("SECOND_BRAIN_DIR", str(Path.home() / "second_brain"))
    ).expanduser()

    if not base_dir.is_dir():
        logger.error("Notes directory does not exist: {}", base_dir)
        click.echo(f"Error: Notes directory does not exist: {base_dir}", err=True)
        raise SystemExit(1)

    files = sorted(base_dir.glob("*.md"), reverse=True)

    if not files:
        logger.error("No notes found in {}", base_dir)
        click.echo("Error: No notes found.", err=True)
        raise SystemExit(1)

    if number < 1 or number > len(files):
        logger.error("Note {} out of range ({}  available)", number, len(files))
        click.echo(
            f"Error: Note {number} not found. Only {len(files)} notes available.",
            err=True,
        )
        raise SystemExit(1)

    logger.debug("Showing note {}: {}", number, files[number - 1].name)
    click.echo(files[number - 1].read_text())
