import re

import pytest
from loguru import logger

from second_brain.app import LOG_FORMAT, configure_logging, main


def test_main_logs_greeting(capfd):
    main()
    captured = capfd.readouterr()
    assert "Hello from second_brain!" in captured.err


def test_log_output_format(capfd):
    """Log line matches: YYYY-MM-DD HH:mm:ss | L | mod:func:line | message."""
    main()
    captured = capfd.readouterr()
    pattern = (
        r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| "
        r"[DIWEC] \| "
        r"\S+:\S+:\d+ \| "
        r".+$"
    )
    assert re.search(pattern, captured.err, re.MULTILINE)


@pytest.mark.parametrize(
    ("level", "letter"),
    [
        ("DEBUG", "D"),
        ("INFO", "I"),
        ("WARNING", "W"),
        ("ERROR", "E"),
        ("CRITICAL", "C"),
    ],
)
def test_log_level_shorthands(capfd, monkeypatch, level, letter):
    """Each level is rendered as a single letter."""
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    configure_logging()
    logger.log(level, "probe")
    captured = capfd.readouterr()
    # Extract the level field (second pipe-delimited segment)
    match = re.search(r"\| ([DIWEC]) \|", captured.err)
    assert match, f"no single-letter level found in: {captured.err!r}"
    assert match.group(1) == letter


def test_log_format_constant():
    """LOG_FORMAT contains the key format fragments."""
    assert "{time:YYYY-MM-DD HH:mm:ss}" in LOG_FORMAT
    assert "{level.name:.1}" in LOG_FORMAT
    assert "| <level>{message}</level>" in LOG_FORMAT
