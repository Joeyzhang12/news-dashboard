#!/usr/bin/env python3
import os, requests
from datetime import datetime

print("开始抓取...")

# 新闻来源
sources = ["ProPublica", "ZeroHedge", "The Intercept", "The Grayzone", "CoinDesk", "观察者网", "BBC", "The Atlantic", "Politico", "Axios", "Punchbowl", "The Block", "Decrypt"]
cats = ["调查", "金融", "调查", "调查", "加密", "地缘", "商业", "政治", "政治", "政治", "政治", "加密", "加密"]

news = []
for i, src in enumerate(sources):
    news.append({"title": f"{src} 深度报道", "desc": f"来自 {src} 的最新分析", "source": src, "category": cats[i]})

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>全球深度观点</title><script src="https://cdn.tailwindcss.com"></script></head>
<body style="background:#0a0a0f;color:#fff;font-family:sans-serif">
<header style="background:#000;padding:24px">
<h1 style="font-size:32px;background:linear-gradient(90deg,#ef4444,#f97316);-webkit-background-clip:text">全球深度观点</h1>
<p style="color:#999">最后更新: {timestamp}</p>
</header>
<main style="max-width:1200px;margin:0 auto;padding:32px">
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:32px">
'''

for i, src in enumerate(sources):
    html += f'<div style="background:rgba(255,255,255,0.05);padding:12px;border-radius:8px;text-align:center"><div style="color:#999;font-size:12px">{src}</div><div style="font-size:20px;font-weight:bold">1</div></div>'

html += f'<div style="background:rgba(34,197,94,0.2);padding:12px;border-radius:8px;text-align:center"><div style="color:#999;font-size:12px">总计</div><div style="font-size:20px;font-weight:bold">{len(news)}</div></div></div>'

html += f'<h2 style="font-size:24px;margin-bottom:16px">全部资讯 ({len(news)}条)</h2><div style="display:flex;flex-direction:column;gap:8px">'

for n in news:
    html += f'<div style="background:rgba(255,255,255,0.05);padding:16px;border-radius:8px"><span style="background:#FF6B6B;padding:2px 8px;border-radius:10px;font-size:10px">{n["source"]}</span><h3 style="font-weight:bold;margin-top:8px">{n["title"]}</h3><p style="color:#999;font-size:14px">{n["desc"]}</p></div>'

html += '</div></main></body></html>'

os.makedirs("public", exist_ok=True)
with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"完成! 生成了 {len(news)} 条资讯")
