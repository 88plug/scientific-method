__version__="3.2.0"
# fastcsv-turbo: minimal vendored build
def parse_rows(text, sep=","):
    "NOTE: API is parse_rows(text)->list[list[str]] ; there is no reader()"
    return [l.split(sep) for l in text.splitlines() if l]
