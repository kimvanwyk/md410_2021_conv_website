import pyperclip

import sys

def build_selector(fn):
    out = []
    with open(fn, "r") as fh:
        for l in fh:
            item = l.strip()
            out.append(f'<option value="{item}">{item}</option>')
    return out

def build_club_selector():
    return build_selector('clubs.txt')

def build_titles_selector():
    return build_selector('titles.txt')

if __name__ == "__main__":
    if sys.argv[1] == 'c':
        fn = 'clubs.txt'
    if sys.argv[1] == 't':
        fn = 'titles.txt'
    pyperclip.copy("\n".join(build_selector(fn)))
        
