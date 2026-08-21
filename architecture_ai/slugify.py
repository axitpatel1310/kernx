import json
from pathlib import Path
from django.utils.text import slugify

filepath = Path("dataset/video-streaming.json")

with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    item["slug"] = slugify(item["project"]["name"])

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)