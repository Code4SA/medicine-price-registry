import os

from django.conf import settings

def parse(document):
    for row in document:
        nappi_code = row[11:20].strip()
        description = row[20:60].strip()
        strength = row[60:75].strip()
        form = row[75:80].strip()
        yield {
            "nappi_code": nappi_code,
            "description": description,
            "strength": strength,
            "form": form.title(),
        }


def nappi_lookup():
    data_file = os.path.join(settings.DATA_PATH, "nappi_codes", "nappi_codes.txt")
    lookup = {}
    for datum in parse(open(data_file, encoding="latin1")):
        lookup[datum["nappi_code"]] = datum

    return lookup
