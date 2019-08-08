CLUBS = []
with open('clubs.txt', "r") as fh:
    CLUBS = [l.strip() for l in fh]

class HTML(object):
    def __init__(self):
        self.out = ["---",
            "title: Registration Form",
            "draft: false",
            "---",
            "",
            '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>',
            '<script src="/js/reg_form.js"></script>',
            '<form name="registration" method="POST" data-netlify="true">',
        ]

    def close(self):
        self.out.append("</form>")

    def render(self):
        return "\n".join([l.replace('~','   ') for l in self.out])

    def add_form_item(self, tag, label, inner):
        self.out.extend(
            (
                '~<div class="form-group row">',
                f'~~<label for="{tag}" class="col-sm-4 col-form-label">{label}: </label>',
                '~~<div class="col-sm-8">',
            )
        )
        self.out.extend(inner)
        self.out.extend(("~~</div>", "~</div>"))

    def add_header(self, text):
        self.out.append(f"~<h2>{text}</h2>")

    def add_text(self, tag, label, help="", type="text"):
        if help:
            help_attr = f' aria-describedby="{tag}_help"'
        else:
            help_attr = ""
        inner = [
            f'~~~<input type="{type}" class="form-control" id="{tag}" name="{tag}"{help_attr}>'
        ]
        if help:
            inner.extend(
                (
                    f'~~~<small id="{tag}_help" class="form-text text-muted">',
                    f"~~~{help}",
                    "~~~</small>",
                )
            )
        self.add_form_item(tag, label, inner)

    def add_email(self, tag, label, help=""):
        self.add_text(tag, label, help=help, type="email")

    def add_selector(self, tag, label, items, help=""):
        if help:
            help_attr = f' aria-describedby="{tag}_help"'
        else:
            help_attr = ""
        inner = [
            f'~~~<select class="form-control" id="{tag}" name="{tag}"{help_attr}>'
        ]
        inner.extend([f'~~~~<option value="{item}">{item}</option>' for item in items])
        inner.append('~~~</select>')
        if help:
            inner.extend(
                (
                    f'~~~<small id="{tag}_help" class="form-text text-muted">',
                    f"~~~~{help}",
                    "~~~</small>",
                )
            )
        self.add_form_item(tag, label, inner)

html = HTML()
html.add_header("First Attendee")
html.add_text(
    "main_first_names",
    "First Names(s)",
    "Your first name or names. Please use your real name rather than a nickname - nicknames can however be used for your name badge later in this form.",
)
html.add_text("main_last_name", "Last Name")
html.add_selector("main_club", "Lions Club", CLUBS)
html.add_text("main_cell", "Cell Phone", "A cellphone number you can be reached at if needed. Your number may also be used for urgent SMSes for changes of plan during the convention.")
html.add_email("main_email", "Email Address")
html.add_text("main_dietary", "Dietary Requirements", help="Please be VERY clear with these requirements")
html.add_text("main_disability", "Special Access Requirements", help="Please indicate any requirements for wheel chair access or the like, if applicable")
html.add_text("main_name_badge", "Name Badge", help="The name you would like to appear on your name badge. eg Kim van Wyk; Lion Trevor Hobbs, ZC Dave Shone; PDG Lyn Botha")
html.close()

with open('../../content/registration/_index.html', 'w') as fh:
    fh.write(html.render())
print(html.render())

