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

    def add_text(self, tag, label, help=""):
        if help:
            help_attr = f' aria-describedby="{tag}_help"'
        else:
            help_attr = ""
        inner = [
            f'~~~<input type="text" class="form-control" id="{tag}" name="{tag}"{help_attr}>'
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


html = HTML()
html.add_header("First Attendee")
html.add_text(
    "main_first_names",
    "First Names(s)",
    "Your first name or names. Please use your real name rather than a nickname - nicknames can however be used for your name badge later in this form.",
)
html.add_text("main_last_name", "Last Name")
html.close()

with open('../../content/registration/_index.html', 'w') as fh:
    fh.write(html.render())
print(html.render())

# <div class="form-group row">
#   <label for="main_first_names" class="col-sm-4 col-form-label">First Name(s): </label>
#   <div class="col-sm-8">
#     <input type="text" class="form-control" id="main_first_names" name="main_first_names" aria-describedby="main_first_names_help">
#     <small id="main_first_names_help" class="form-text text-muted">
#       Your first name or names. Please use your real name rather than a nickname - nicknames can be however used for your name badge later in this form.
#     </small>
#   </div>
# </div>
