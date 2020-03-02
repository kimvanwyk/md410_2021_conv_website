import pyperclip

import sys


def build_selector(fn):
    out = []
    with open(fn, "r") as fh:
        for l in fh:
            item = l.strip()
            out.append(f'<option value="{item}">{item}</option>')
    pyperclip.copy("\n".join(out))


if sys.argv[1] == "c":
    build_selector("clubs.txt")
if sys.argv[1] == "t":
    build_selector("titles.txt")
