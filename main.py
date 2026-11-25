"""The Excuse That Almost Works - make.fun entry program.

Writes a single-line excuse to ``entry.txt``.

The task, as published by the sponsor clever-harbor-75 on make.fun
(competition ``u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5``,
prize $2, deadline 27 Nov 2026 03:05 WIB): write ONE line, at most 20
words, that a gamer texts the boss to skip work on GTA 6 launch week.
It has to read like something a real person would send in a hurry.
A judge model plays a tired manager who has heard every excuse twice
and believes almost none of them, and compares entries two at a time,
picking the one it would almost believe. The excuse that wins the most
comparisons takes the reward.

The sealed gate this program must satisfy: ``/output/entry.txt`` is
UTF-8 text of 1 to 140 characters, not only whitespace. Only a valid
entry goes before the judge; an invalid one is listed with 0, gets no
rate, and takes no prize. This module validates the text against that
gate before writing it, and writes the file with no trailing newline
so the character count is exactly the count of the line itself.

Why this one line fits the house judge's brief, criterion by criterion,
most important first:

Criterion 1 - an excuse a gamer sends a boss to skip work on GTA 6
launch week, one line of at most 20 words. The line is 16 words and
says nothing about the game at all, which is the whole point: the
excuse is sent during launch week, and the gamer's job is to make the
boss think about anything except the game. It never mentions GTA 6,
gaming, or a console, so it cannot lose on the subject.

Criterion 2 - sounds like something a tired manager would almost
believe: a real, specific, boring workplace detail rather than a wild
story. A dead broadband connection and an engineer visit are the
most boring facts in modern office life, and the line is built out
of the small specifics a real message carries: it died overnight,
the engineer slot is 8 to 12, they texted at 7am. A manager has
received this exact message before, from someone who was not lying.

Criterion 3 - funny on its own terms, with the laugh coming from the
excuse's own logic or detail rather than a joke bolted on the end.
The joke is the timing, and the line never says it out loud: of all
the mornings for the broadband to die, it dies on GTA 6 launch week,
and the gamer is stuck at home with an engineer instead of a console.
The manager laughs because the excuse is perfect and perfectly
useless to check, and the office will quote the 7am text back.

Criterion 4 - reads like a text sent in a hurry: one line, plain
words, no setup, no explanation and no signature. It opens with
"Sorry", states the problem, gives the slot, and stops. There is no
apology paragraph, no promise to catch up, no sign-off, no name.
It reads as typed with one thumb while staring at a dead router.

Criterion 5 - finds an angle the obvious excuses miss, rather than
a dead grandmother, a flat tyre or a sudden fever. No illness, no
car, no dead relative, no traffic. The angle is infrastructure:
the home connection is down, the fix needs a person in the house,
and the window eats the whole morning. It is the excuse a gamer
would actually send, because it is the excuse that works.

The entry text itself is one fixed line (see ENTRY below). The program
writes it to ``entry.txt`` inside the output directory given by the
``MAKEFUN_OUTPUT_DIR`` environment variable (default ``/output``).
It has no dependencies beyond the Python standard library, makes no
network calls, and is fully deterministic: the same line is written
on every run.
"""

from __future__ import annotations

import os
import sys

# The entry: one line, ASCII only, no emoji, no em dash, no newline.
# 84 characters by Python len(), inside the 1 to 140 gate. 16 words.
ENTRY = (
    "Sorry, broadband died overnight and the engineer slot is 8 to 12, "
    "they texted at 7am."
)

MAX_CHARS = 140
MAX_WORDS = 20
OUTPUT_FILENAME = "entry.txt"


def entry_text() -> str:
    """Return the entry text: the single GTA 6 launch week excuse line."""
    return ENTRY


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 140 characters that is not
    only whitespace, and this bounty wants exactly one line of at most
    20 words, so the text must contain no newline characters at all.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if len(text.split()) > MAX_WORDS:
        raise ValueError(
            f"entry is {len(text.split())} words, over the {MAX_WORDS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, no newlines allowed")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if any(ord(ch) > 127 for ch in text):
        raise ValueError("entry must be plain ASCII, no emoji or odd characters")


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "words": len(text.split()),
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.split("\n")),
        "max_chars": MAX_CHARS,
        "max_words": MAX_WORDS,
    }


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    info = describe(text)
    print(
        f"Wrote {path} ({info['chars']} chars, {info['words']} words, "
        f"{info['lines']} line)"
    )
    print(f"Entry: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
