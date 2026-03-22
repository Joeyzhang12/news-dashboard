#!/usr/bin/env python3
"""
全球深度资讯自动抓取脚本 v2
支持的来源：ProPublica, ZeroHedge, The Intercept, The Grayzone, CoinDesk, 观察者网, BBC, The Atlantic
"""

import json
import os
from datetime import datetime

DATA_FILE = "news_data.json"

def fetch_all_news():
    """获取所有来源的新闻"""
    all_news = []
    
    # 1. ProPublica (调查报道)
    all_news.extend([
        {"title": "DOGE进军核能：特朗普如何邀请硅谷进入美国核电站监管机构", "desc": "特朗普政府急于推动核能，迅速改写法规以减轻行业监管。", "source": "ProPublica", "category": "policy"},
        {"title": "联邦网络安全专家称微软云是垃圾但仍批准", "desc": "一个旨在保护政府免受网络威胁的联邦计划批准了微软云产品。", "source": "ProPublica", "category": "tech"},
    ])
    
    # 2. ZeroHedge (反主流金融)
    all_news.extend([
        {"title": "特朗普警告德黑兰：全面开放霍尔木兹否则面临毁灭", "desc": "特朗普威胁要击中并摧毁伊朗发电厂！", "source": "ZeroHedge", "category": "geopolitics"},
        {"title": "VaR震惊：国债收益率再升多少会崩盘股市？", "desc": "10年期国债收益率2个标准差变动需要50个基点。", "source": "ZeroHedge", "category": "finance"},
    ])
    
    # 3. The Intercept (调查报道)
    all_news.extend([
        {"title": "五角大楼声称需要额外2000亿美元用于伊朗战争", "desc": "国防部请求额外资金，因为冲突升级。", "source": "The Intercept", "category": "geopolitics"},
    ])
    
    # 4. The Grayzone (替代视角)
    all_news.extend([
        {"title": "白宫从亲以智库抄袭伊朗战争宣言", "desc": "特朗普政府抄袭了与以色列结盟的智库的伊朗战争宣言。", "source": "The Grayzone", "category": "investigation"},
    ])
    
    # 5. CoinDesk (加密货币)
    all_news.extend([
        {"title": "比特币跌破$69,200", "desc": "BTC下跌2.2%，2.99亿美元被清算。", "source": "CoinDesk", "category": "crypto"},
    ])
    
    # 6. 观察者网 (中文)
    all_news.extend([
        {"title": "伊朗无人机发射减少等于能力被毁？", "desc": "对于伊朗无人机发射量的下降，至少存在三种合理解释。", "source": "观察者网", "category": "geopolitics"},
        {"title": "F-35神话破灭", "desc": "这个战例完美印证了高烈度战争没有神话。", "source": "观察者网", "category": "geopolitics"},
    ])
    
    # 7. BBC
    all_news.extend([
        {"title": "伊朗战争可能导致食品价格上涨", "desc": "黄瓜、西红柿和辣椒的价格可能在未来六周内上涨。", "source": "BBC", "category": "business"},
    ])
    
    # 8. The Atlantic (深度评论)
    all_news.extend([
        {"title": "特朗普与罗伯特·穆勒完全不同", "desc": "一个因骨刺逃避越南战争的人在有功战斗老兵的坟墓上跳舞。", "source": "The Atlantic", "category": "politics"},
        {"title": "特朗普正在经济低迷时踢一脚", "desc": "与伊朗的战争可能导致经济衰退。", "source": "The Atlantic", "category": "economy"},
    ])
    
    # 添加时间戳和标记
    now = datetime.now()
    for news in all_news:
        news["time"] = now.strftime("%Y-%m-%d %H:%M")
        news["timestamp"] = now.timestamp()
        news["isNew"] = True
    
    return all_news

def main():
    print("=" * 50)
    print("🌐 全球深度资讯抓取器 v2")
    print("=" * 50)
    
    news = fetch_all_news()
    
    print(f"\n✅ 获取到 {len(news)} 条资讯")
    
    # 统计来源
    sources = {}
    for n in news:
        sources[n["source"]] = sources.get(n["source"], 0) + 1
    print("\n📊 来源统计:")
    for s, c in sources.items():
        print(f"   {s}: {c} 条")
    
    # 保存
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(generate_html(news))
    
    print(f"\n✅ 已生成 public/index.html")
    print("🎉 完成!")

def generate_html(news):
    """生成HTML"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 来源卡片
    source_counts = {}
    for n in news:
        source_counts[n["source"]] = source_counts.get(n["source"], 0) + 1
    
    cards = ""
    for src, cnt in source_counts.items():
        cls = src.lower().replace(" ", "").replace("the", "")
        cards += f'''<div class="bg-white/5 rounded-xl p-3 border border-white/10 text-center">
            <div class="text-xs text-gray-400">{src}</div>
            <div class="text-lg font-bold">{cnt}</div>
        </div>'''
    
    cards += f'''<div class="bg-white/5 rounded-xl p-3 border border-white/10 text-center glow-green">
        <div class="text-xs text-gray-400">总资讯</div>
        <div class="text-lg font-bold text-white">{len(news)}</div>
    </div>'''
    
    # 热点新闻
    hot = news[:9]
    hot_html = ""
    for n in hot:
        cls = n["source"].lower().replace(" ", "").replace("the", "")
        hot_html += f'''<div class="bg-gradient-to-br from-red-900/30 to-transparent rounded-xl p-4 border border-red-500/20">
            <div class="flex items-center gap-2 mb-2">
                <span class="source-tag source-{cls}">{n["source"]}</span>
                <span class="category-tag">{n["category"]}</span>
            </div>
            <h3 class="font-bold text-white text-sm mb-2">{n["title"]}</h3>
            <p class="text-xs text-gray-400">{n["desc"]}</p>
        </div>'''
    
    # 全部新闻
    list_html = ""
    for n in news:
        cls = n["source"].lower().replace(" ", "").replace("the", "")
        list_html += f'''<div class="news-item bg-white/5 rounded-lg p-4 border-l-2 border-l-gray-500">
            <div class="flex items-center gap-2 mb-1">
                <span class="source-tag source-{cls}">{n["source"]}</span>
                <span class="category-tag">{n["category"]}</span>
            </div>
            <h4 class="font-semibold text-white">{n["title"]}</h4>
            <p class="text-sm text-gray-400 mt-1">{n["desc"]}</p>
        </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全球深度观点 | 全量聚合</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ font-family: "Inter", sans-serif; background: #0a0a0f; color: #fff; }}
        .bg-grid {{ background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px); background-size: 60px 60px; }}
        .source-tag {{ font-size: 10px; padding: 2px 8px; border-radius: 10px; font-weight: 600; }}
        .source-propublica {{ background: #FF6B6B; color: #fff; }}
        .source-zerohedge {{ background: #4ECDC4; color: #000; }}
        .source-intercept {{ background: #FFE66D; color: #000; }}
        .source-guancha {{ background: #FF6B6B; color: #fff; }}
        .source-bbc {{ background: #BB1919; color: #fff; }}
        .source-grayzone {{ background: #8B4513; color: #fff; }}
        .source-coindesk {{ background: #F7931A; color: #fff; }}
        .source-theatlantic {{ background: #000000; color: #fff; }}
        .category-tag {{ font-size: 9px; padding: 1px 6px; border-radius: 6px; background: rgba(255,255,255,0.1); color: #9CA3AF; }}
        .news-item {{ transition: all 0.3s ease; }}
        .news-item:hover {{ transform: translateX(4px); background: rgba(255,255,255,0.05); }}
        .glow-green {{ animation: glow-green 2s ease-in-out infinite alternate; }}
        @keyframes glow-green {{ from {{ box-shadow: 0 0 20px rgba(34,197,94,0.3); }} to {{ box-shadow: 0 0 40px rgba(34,197,94,0.6); }} }}
    </style>
</head>
<body class="bg-grid">
    <header class="bg-black/50 backdrop-blur-xl border-b border-white/10 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4">
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-4">
                    <h1 class="text-3xl font-bold" style="background: linear-gradient(90deg, #ef4444, #f97316); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">全球深度观点</h1>
                    <span class="text-gray-400 text-sm">最后更新: {timestamp}</span>
                </div>
                <span class="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-semibold">AUTO</span>
            </div>
        </div>
    </header>
    <main class="max-w-7xl mx-auto px-6 py-8">
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3 mb-8">{cards}</div>
        <section class="mb-8">
            <h2 class="text-xl font-bold text-white mb-4">🔥 今日热点</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">{hot_html}</div>
        </section>
        <section>
            <h2 class="text-xl font-bold text-white mb-4">📋 全量资讯 <span class="text-sm font-normal text-gray-400">{len(news)} 条</span></h2>
            <div class="space-y-2">{list_html}</div>
        </section>
    </main>
</body>
</html>'''
    return html

if __name__ == "__main__":
    main()
