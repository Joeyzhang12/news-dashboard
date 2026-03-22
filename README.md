# 🌐 全球深度资讯自动抓取系统

这是一个自动化新闻抓取+部署系统，每天自动更新并部署到 Vercel。

## 📋 功能

- 🤖 自动抓取多个深度新闻来源
- 🌐 生成静态 HTML 页面
- ☁️ 自动部署到 Vercel
- ⏰ 每天凌晨3点自动更新

## 🏷️ 支持的来源

- ProPublica (调查报道)
- ZeroHedge (金融)
- The Intercept (调查报道)
- The Grayzone (深度调查)
- CoinDesk (加密货币)
- 观察者网 (中文深度)
- BBC (主流财经)

## 🚀 部署步骤

### 1. 创建 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库，命名为 news-dashboard
# 将整个 news-scraper 文件夹内容推送到仓库
```

### 2. 配置 Vercel

1. 登录 [Vercel](https://vercel.com)
2. 导入 GitHub 仓库
3. 配置：
   - Framework Preset: Other
   - Build Command: `python scraper.py` (可选)
   - Output Directory: `public`

### 3. 配置 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

| Secret Name | 说明 |
|-------------|------|
| VERCEL_TOKEN | Vercel API Token |
| VERCEL_ORG_ID | Vercel 组织 ID |
| VERCEL_PROJECT_ID | Vercel 项目 ID |

### 4. 启用 GitHub Actions

推送代码后，GitHub Actions 会自动运行。

可以在仓库的 Actions 标签查看运行状态。

## ⏰ 自动运行时间

当前配置：每天凌晨 3:00 (UTC)

如需修改，编辑 `.github/workflows/daily-update.yml`：

```yaml
schedule:
  - cron: '0 3 * * *'  # 修改这里的数字
```

## �手动手动触发

在 GitHub 仓库页面：
1. 进入 Actions 标签
2. 选择 "Daily News Update"
3. 点击 "Run workflow"

## 📁 文件结构

```
news-scraper/
├── scraper.py              # 主抓取脚本
├── news_data.json         # 新闻数据 (自动生成)
├── public/
│   └── index.html         # 输出的HTML (自动生成)
├── .github/
│   └── workflows/
│       └── daily-update.yml  # GitHub Actions 配置
└── README.md
```

## 🔧 本地运行

```bash
# 安装依赖
pip install requests beautifulsoup4 lxml

# 运行脚本
python scraper.py
```

## 📝 许可证

MIT License
