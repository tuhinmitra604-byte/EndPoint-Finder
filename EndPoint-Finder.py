import argparse
import re

import requests


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="Input a URL")
parser.add_argument("-f", "--file", help="Input file location")
parser.add_argument("-o", "--output", help="Output file location")
parser.add_argument(
    "-c", "--cookie",
    help='Add a URL cookie, for example "PHPSESSID=qw32312313"',
)
args = parser.parse_args()

if not args.file and not args.url:
    parser.print_help()
    parser.exit()

print(r"""
.___     ..__         ,      .___      .
[__ ._  _|[__) _ *._ -+- ___ [__ *._  _| _ ._.
[___[ )(_]|   (_)|[ ) |      |   |[ )(_](/,[

            author: $_SpyD3r_$
""")

if args.file:
    with open(args.file, "r", encoding="utf-8", errors="replace") as file:
        content = file.read()

if args.url:
    cookies = None
    if args.cookie:
        name, value = args.cookie.split("=", 1)
        cookies = {name: value}

    response = requests.get(args.url, cookies=cookies, timeout=10)
    response.raise_for_status()
    content = response.text

content_parts = content.split('"')

extensions = (".png", ".jpg", ".wav", ".jpeg", ".json", ".js", ".php", ".xml")
starts = ("/", "http://", "https://", "file://", "php://", "ftp://", "./", "../")
remote_starts = ("http://", "https://", "file://", "php://", "ftp://")
pattern = re.compile(r"[a-zA-Z0-9_/ :&?%.\-=]*".replace(" ", ""))

endpoints = []

for item in content_parts:
    if pattern.fullmatch(item) and (
        item.startswith(starts) or item.endswith(extensions)
    ):
        endpoints.append(item)

for item in content_parts:
    if pattern.fullmatch(item) and not item.startswith(starts):
        first_part = item.split("/")[0]
        if any(prefix + first_part in endpoints for prefix in ("/", "./", "../")):
            endpoints.append(item)

endpoints = sorted(set(endpoints))

sections = [
    (
        "Remote files which are added",
        [item for item in endpoints if item.startswith(remote_starts)],
    ),
    (
        "These files are present in server",
        [item for item in endpoints if item.endswith(extensions)],
    ),
    (
        "These are files and directory, you can look into",
        [
            item for item in endpoints
            if item.startswith(("/", "./", "../"))
            and not item.endswith(extensions)
        ],
    ),
    (
        "These directory can be present (not sure!!)",
        [
            item for item in endpoints
            if not item.startswith(starts)
            and not item.endswith(extensions)
        ],
    ),
]

lines = []
for title, items in sections:
    lines.append(f"\n-----------------{title}-----------------")
    lines.extend(items)

result = "\n".join(lines)
print(result)

if args.output:
    with open(args.output, "a", encoding="utf-8") as file:
        file.write(result + "\n")
