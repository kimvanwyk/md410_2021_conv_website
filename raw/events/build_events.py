from dateutil import parser
from glob import glob
import string
import textwrap

SPECIAL_CASES = {"MD410 Convention resumption":"md_convention"}

events = []
for f in glob('*.txt'):
    with open(f, 'r') as fh:
        lines = [l.strip() for l in fh]
    if "## DISABLE" in lines[0]:
        continue
    event = lines[0]
    date = parser.parse(lines[1], yearfirst=True, dayfirst=False)
    time = lines[2]
    fn = f"{f[:-3]}md"
    location = lines[3]
    if location == 'TBC':
        location = 'To be confirmed'

    body = '\n'.join([f"{l}\n" for l in lines[4:] if l])
    if not body:
        body = 'More details will be made available closer to the event. \\'

    events.append((date, int(time[:2]), fn, time, event, location, body))

events.sort()
dt = None

program = []
for (date, _, fn, time, event, location, body) in events:
    out = []
    if event not in SPECIAL_CASES:
        with open(f"../../content/events/{fn}", 'w') as fh:
            fh.write(textwrap.dedent(f'''\
            ---
            title: {event}
            draft: false
            ---

            '''))
            fh.write(body)

            fh.write(textwrap.dedent(f'''\
            \\
            \\
            **Date and Time**: {date:%A %d %B %Y}, {time} \\
            **Location**: {location}
            \\
            \\
            [Back to Program](/program)
            '''))

    if date != dt:
        dt = date
        program.extend(['',f'## {dt:%A %d %B %Y}','','Time | Event (click on event for further details) | Venue (click for map to venue)',' ---|---  |---'])
    fn = SPECIAL_CASES.get(event, f"{f[:-3]}md")
    program.append(f"{time} | [{event}](/events/{fn}) | {location}") 

with open('../../content/program/_index.md', 'w') as fh:
    fh.write(textwrap.dedent('''
    ---
    title: "Lions MD410 2020 Convention Program"
    draft: false
    ---
    
    The Lions MD410 2020 Convention will be held on Friday 1 May and Saturday 2 May 2020. Some Lions serving in District and Multiple District portfolios will be attending events on Thursday 30 April but most Lions will only need to arrive during the morning of Friday 1 May.
    
    Some events will be held at the North Durban Lions Clubhouse which is less than 5 minutes travel from the Riverside Hotel.
    '''))
    
    fh.write("\n".join(program))
    fh.write("\n")

        
