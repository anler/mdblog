import re


def extract_links(template):
    "Extracts all the relative links from a template"
    return {match.group(1) for match in re.finditer('href="([^"]+)"',
                                                    template)}


