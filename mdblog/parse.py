import re


def extract_links(template):
    "Extracts all the relative links from a template"
    return {match.group(2) for match in re.finditer('(href|src)="([^"]+)"',
                                                    template)}


