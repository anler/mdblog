import re

urls_regexp = re.compile(r'href="([^"]+)"')

def extract_links(template):
    "Extracts all the relative links from a template"
    urls = []
    for match in urls_regexp.finditer(template):
        url = match.group(1)
        if "://" not in url:
            urls.append(url)

    return urls
