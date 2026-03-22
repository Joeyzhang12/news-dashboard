#!/usr/bin/env python3
"""
全球深度资讯自动抓取脚本
每天自动运行，抓取多个来源的新闻，生成HTML
"""

import json
import os
from datetime import datetime
import re

# 新闻数据存储文件
DATA_FILE = os.path.join(os.path.dirname(__file__), 'news_data.json')
HTML_TEMPLATE = os.path.join(os.path.dirname(__file__), 'template.html')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'public', 'index.html')

# 模拟数据（实际项目中替换为真实API调用）
# 这些数据会在GitHub Actions中每天更新
def get_sample_news():
    """生成模拟的新闻数据 - 实际使用时替换为真实爬虫"""
    return [
        # ProPublica
        {"title": "DOGE进军核能：特朗普如何邀请硅谷进入美国核电站监管机构", "desc": "特朗普政府急于推动核能，迅速改写法规以减轻行业监管。", "source": "ProPublica", "category": "policy", "isNew": True},
        {"title": "联邦网络安全专家称微软云是'一堆屎'，但仍然批准了", "desc": "一个旨在保护政府免受网络威胁的联邦计划批准了一个庞大的微软云产品。", "source": "ProPublica", "category": "tech", "isNew": True},
        
        # ZeroHedge
        {"title": "特朗普警告德黑兰：全面开放霍尔木兹否则面临'毁灭'", "desc": "特朗普威胁要'击中并摧毁'伊朗发电厂！", "source": "ZeroHedge", "category": "geopolitics", "isNew": True},
        {"title": "VaR震惊：国债收益率再升多少会崩盘股市？", "desc": "10年期国债收益率2个标准差变动需要50个基点。", "source": "ZeroHedge", "category": "finance", "isNew": True},
        
        # The Intercept
        {"title": "五角大楼声称需要额外2000亿美元用于伊朗战争", "desc": "国防部请求额外资金，因为冲突升级。", "source": "The Intercept", "category": "geopolitics", "isNew": True},
        
        # The Grayzone
        {"title": "白宫从亲以智库抄袭伊朗战争宣言", "desc": "特朗普政府抄袭了与以色列结盟的智库的伊朗战争宣言。", "source": "The Grayzone", "category": "investigation", "isNew": False},
        
        # CoinDesk
        {"title": "比特币跌破$69,200，特朗普给出48小时最后通牒", "desc": "BTC下跌2.2%，2.99亿美元被清算。", "source": "CoinDesk", "category": "crypto", "isNew": True},
        {"title": "加密公司因市场疲软和AI强劲裁员数百人", "desc": "2026年初的加密裁员潮暴露了两个便利叙事之间的差距。", "source": "CoinDesk", "category": "crypto", "isNew": False},
        
        # 观察者网
        {"title": "伊朗无人机发射减少等于能力被毁？华盛顿可能误读了对手", "desc": "对于伊朗无人机发射量的下降，至少存在三种合理解释。", "source": "观察者网", "category": "geopolitics", "isNew": True},
        {"title": "F-35神话破灭", "desc": "这个战例完美印证了高烈度战争没有神话。", "source": "观察者网", "category": "geopolitics", "isNew": True},
        {"title": "美伊冲突：会再现1970年代的全球通胀吗？", "desc": "油价飙升叠加关税推升进口成本。", "source": "观察者网", "category": "finance", "isNew": False},
        
        # BBC
        {"title": "伊朗战争可能导致食品价格上涨", "desc": "黄瓜、西红柿和辣椒的价格可能在未来六周内上涨。", "source": "BBC", "category": "business", "isNew": True},
        {"title": "美国解除部分伊朗石油制裁", "desc": "此举将迅速向全球市场投放约1.4亿桶石油。", "source": "BBC", "category": "finance", "isNew": True},
    ]

def generate_html(news_data):
    """生成HTML页面"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 按来源统计
    source_counts = {}
    for news in news_data:
        source = news['source']
        source_counts[source] = source_counts.get(source, 0) + 1
    
    # 生成来源卡片HTML
    source_cards = ""
    for source, count in source_counts.items():
        source_class = source.lower().replace(' ', '').replace('the', '')
        source_cards += f'''
            <div class="bg-white/5 rounded-xl p-3 border border-white/10 text-center">
                <div class="text-xs text-gray-400">{source}</div>
                <div class="text-lg font-bold">{count}</div>
            </div>'''
    
    # 添加总数卡片
    source_cards += f'''
        <div class="bg-white/5 rounded-xl p-3 border border-white/10 text-center glow-green">
            <div class="text-xs text-gray-400">总资讯</div>
            <div class="text-lg font-bold text-white">{len(news_data)}</div>
        </div>'''
    
    # 生成热点新闻HTML
    hot_news = news_data[:9]
    hot_html = ""
    for news in hot_news:
        is_new = '<span class="text-green-400">🆕 新</span>' if news.get('isNew') else ''
        hot_html += f'''
            <div class="bg-gradient-to-br from-red-900/30 to-transparent rounded-xl p-4 border border-red-500/20">
                <div class="flex items-center gap-2 mb-2">
                    <span class="source-tag source-{news['source'].lower().replace(' ', '').replace('the', '')}">{news['source']}</span>
                    <span class="category-tag">{news['category']}</span>
                </div>
                <h3 class="font-bold text-white text-sm mb-2 line-clamp-2">{news['title']}</h3>
                <p class="text-xs text-gray-400 line-clamp-2">{news['desc']}</p>
                <div class="flex items-center justify-between mt-2 text-xs text-gray-500">
                    <span>{timestamp}</span>
                    {is_new}
                </div>
            </div>'''
    
    # 生成全量新闻列表HTML
    news_list_html = ""
    for news in news_data:
        is_new = '<span class="text-green-400">🆕 新</span>' if news.get('isNew') else ''
        border_colors = {
            'geopolitics': 'border-l-blue-500',
            'finance': 'border-l-yellow-500', 
            'crypto': 'border-l-orange-500',
            'investigation': 'border-l-red-500',
            'tech': 'border-l-purple-500',
            'business': 'border-l-green-500',
            'policy': 'border-l-orange-500'
        }
        border_color = border_colors.get(news['category'], 'border-l-gray-500')
        
        news_list_html += f'''
            <div class="news-item bg-white/5 rounded-lg p-4 border-l-2 {border_color}">
                <div class="flex items-start justify-between gap-4">
                    <div class="flex-1">
                        <div class="flex items-center gap-2 mb-1">
                            <span class="source-tag source-{news['source'].lower().replace(' ', '').replace('the', '')}">{news['source']}</span>
                            <span class="category-tag">{news['category']}</span>
                        </div>
                        <h4 class="font-semibold text-white">{news['title']}</h4>
                        <p class="text-sm text-gray-400 mt-1">{news['desc']}</p>
                    </div>
                </div>
            </div>'''
    
    # 读取模板文件
    if os.path.exists(HTML_TEMPLATE):
        with open(HTML_TEMPLATE, 'r', encoding='utf-8') as f:
            html_template = f.read()
    else:
        # 使用内置模板
        html_template = get_default_template()
    
    # 替换占位符
    html = html_template.replace('{{SOURCE_CARDS}}', source_cards)
    html = html_template.replace('{{HOT_NEWS}}', hot_html)
    html = html_template.replace('{{NEWS_LIST}}', news_list_html)
    html = html_template.replace('{{TIMESTAMP}}', timestamp)
    html = html_template.replace('{{NEWS_COUNT}}', str(len(news_data)))
    
    return html

def get_default_template():
    """默认HTML模板"""
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>全球深度观点 | 全量聚合</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: "Inter", sans-serif; background: #0a0a0f; min-height: 100vh; color: #fff; }
        .bg-grid { background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px); background-size: 60px 60px; }
        .source-tag { font-size: 10px; padding: 2px 8px; border-radius: 10px; font-weight: 600; }
        .source-propublica { background: #FF6B6B; color: #fff; }
        .source-zerohedge { background: #4ECDC4; color: #000; }
        .source-intercept { background: #FFE66D; color: #000; }
        .source-guancha { background: #FF6B6B; color: #fff; }
        .source-bbc { background: #BB1919; color: #fff; }
        .source-grayzone { background: #8B4513; color: #fff; }
        .source-coindesk { background: #F7931A; color: #fff; }
        .category-tag { font-size: 9px; padding: 1px 6px; border-radius: 6px; background: rgba(255,255,255,0.1); color: #9CA3AF; }
        .news-item { transition: all 0.3s ease; border-left: 3px solid transparent; }
        .news-item:hover { transform: translateX(4px); background: rgba(255,255,255,0.05); }
        .glow-green { animation: glow-green 2s ease-in-out infinite alternate; }
        @keyframes glow-green { from { box-shadow: 0 0 20px rgba(34,197,94,0.3); } to { box-shadow: 0 0 40px rgba(34,197,94,0.6); } }
        .pulse-dot { animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .gradient-text { background: linear-gradient(90deg, #ef4444, #f97316, #eab308); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
</head>
<body class="bg-grid">
    <header class="bg-black/50 backdrop-blur-xl border-b border-white/10 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4">
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-4">
                    <div class="w-3 h-3 rounded-full bg-green-500 pulse-dot"></div>
                    <h1 class="text-3xl font-black gradient-text">全球深度观点</h1>
                    <span class="text-gray-400 text-sm">最后更新: {{TIMESTAMP}}</span>
                </div>
                <span class="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-semibold">AUTO</span>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3 mb-8">
            {{SOURCE_CARDS}}
        </div>

        <section class="mb-8">
            <h2 class="text-xl font-bold text-white flex items-center gap-2 mb-4"><span class="w-2 h-2 bg-red-500 rounded-full"></span>🔥 今日热点</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">{{HOT_NEWS}}</div>
        </section>

        <section>
            <h2 class="text-xl font-bold text-white flex items-center gap-2 mb-4"><span class="w-2 h-2 bg-green-500 rounded-full pulse-dot"></span>📋 全量资讯 <span class="text-sm font-normal text-gray-400">{{NEWS_COUNT}} 条</span></h2>
            <div class="space-y-2">{{NEWS_LIST}}</div>
        </section>
    </main>

    <footer class="border-t border-white/10 mt-12 py-6">
        <div class="max-w-7xl mx-auto px-6 text-center text-gray-500 text-sm">Generated by QClaw Deep News • {{TIMESTAMP}}</div>
    </footer>
</body>
</html>'''

def main():
    """主函数"""
    print("=" * 50)
    print("🌐 全球深度资讯抓取器")
    print("=" * 50)
    
    # 获取新闻数据
    print("\n📥 正在抓取新闻数据...")
    news_data = get_sample_news()
    print(f"✅ 获取到 {len(news_data)} 条资讯")
    
    # 统计来源
    sources = {}
    for news in news_data:
        sources[news['source']] = sources.get(news['source'], 0) + 1
    print("\n📊 来源统计:")
    for source, count in sources.items():
        print(f"   {source}: {count} 条")
    
    # 生成HTML
    print("\n🎨 正在生成HTML...")
    os.makedirs(os.path.join(os.path.dirname(__file__), 'public'), exist_ok=True)
    html = generate_html(news_data)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 已生成: {OUTPUT_FILE}")
    print(f"✅ 总资讯: {len(news_data)} 条")
    print("\n" + "=" * 50)
    print("🎉 完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
