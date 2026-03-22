#!/usr/bin/env python3
import os
from datetime import datetime

sources = [
    {"name": "观察者网", "cat": "地缘"},
    {"name": "华尔街见闻", "cat": "财经"},
    {"name": "BBC", "cat": "国际"},
]

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

html = "<html><body><h1>全球深度观点</h1><p>" + timestamp + "</p>"
for s in sources:
    html += f"<div>{s['name']} - {s['cat']}</div>"
html += "</body></html>"

os.makedirs("public", exist_ok=True)
with open("public/index.html", "w") as f:
    f.write(html)

print("Done!")
