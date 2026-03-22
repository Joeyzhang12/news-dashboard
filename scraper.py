#!/usr/bin/env python3
import os, json, requests
from datetime import datetime

PROXY_API = "http://route.xiongmaodaili.com/xiongmao-web/cx/cxip?secret=90b74a9e1ad7d012e19ad08d3578a156&orderNo=CX20260322154320M1jba2Tr&isTxt=1&removal=0&cityId=0&proxyType=1&returnAccount=1"

def get_proxy():
    try:
        r = requests.get(PROXY_API, timeout=10)
        text = r.text.strip()
        if text:
            # 返回格式: ip:端口
            return text
    except Exception as e:
        print(f"Proxy error: {e}")
    return None

def main():
    print("全球深度资讯抓取器 v4")
    
    # 获取代理
    proxy = get_proxy()
    print(f"Proxy: {proxy or 'Direct'}")
    
    news = []
    sources = ["ProPublica", "ZeroHedge", "The Intercept", "The Grayzone", "CoinDesk", "观察者网", "BBC", "The Atlantic", "Politico", "Axios", "Punchbowl"]
    cats = ["调查", "金融", "调查", "调查", "加密", "地缘", "商业", "政治", "政治", "政治", "政治"]
    
    for i, src in enumerate(sources):
        news.append({"title": f"{src} 深度报道", "desc": f"来自 {src} 的最新分析", "source": src, "category": cats[i]})
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>全球深度观点</title><script src="https://cdn.tailwindcss.com"></script></head><body style="background:#0a0a0f;color:#fff;font-family:sans-serif"><header style="background:#000;padding:24px"><h1 style="font-size:32px;background:linear-gradient(90deg,#ef4444,#f97316);-webkit-background-clip:text">全球深度观点</h1><p style="color:#999">最后更新: {timestamp} | 代理: {proxy or "直连"}</p></header><main style="max-width:1200px;margin:0 auto;padding:32px"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:32px">
'''
    for i, src in enumerate(sources):
        html += f'<div style="background:rgba(255,255,255,0.05);padding:12px;border-radius:8px;text-align:center"><div style="color:#999;font-size:12px">{src}</div><div style="font-size:20px;font-weight:bold">1</div></div>'
    
    html += f'<div style="background:rgba(34,197,94,0.2);padding:12px;border-radius:8px;text-align:center"><div style="color:#999;font-size:12px">总计</div><div style="font-size:20px;font-weight:bold">{len(news)}</div></div></div><h2 style="font-size:24px;margin-bottom:16px">全部资讯 ({len(news)}条)</h2><div style="display:flex;flex-direction:column;gap:8px">'
    
    for n in news:
        html += f'<div style="background:rgba(255,255,255,0.05);padding:16px;border-radius:8px"><span style="background:#FF6B6B;padding:2px 8px;border-radius:10px;font-size:10px">{n["source"]}</span><h3 style="font-weight:bold;margin-top:8px">{n["title"]}</h3><p style="color:#999;font-size:14px">{n["desc"]}</p></div>'
    
    html += '</div></main></body></html>'
    
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Done! Generated {len(news)} articles")

if __name__ == "__main__":
    main()
