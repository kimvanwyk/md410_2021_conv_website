from dateutil import parser 

dt = None
with open('../../content/program/_index.md', 'r') as fh: 
    for l in fh: 
        if l[0] == '#': 
            try: 
                dt = parser.parse(l[2:].strip()) 
            except Exception as e: 
                pass              
        if dt and (len(l) > 5) and l[5] == '-':
            (time, event, location) = l.strip().split('|')
            event = event.strip().split(']')[0].strip('[')
            time = time.strip()
            location = location.strip()
            with open(f"{event.replace(' ', '_').replace('/', '_').lower()}.txt", 'w') as fout:
                fout.write(f"{event}\n")
                fout.write(f"{dt.date():%y/%m/%d}\n")
                fout.write(f"{time}\n")
                fout.write(f"{location}\n\n")
                print(f"Wrote {fout.name}")

