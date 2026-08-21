# AstrBot Plugin: Miraheze Wiki 查询

这是一个 [AstrBot](https://github.com/Soulter/AstrBot) 插件，用于查询 [SEWH.miraheze.org](https://SEWH.miraheze.org/wiki/Main_Page) 上的 Wiki 页面内容，并直接返回纯文本结果。

## ✨ 功能

- 通过 `/wiki <页面标题>` 命令，获取指定 Wiki 页面的内容。
- 自动去除 HTML 标签，提取纯文本，适合在聊天环境中阅读。
- 内容过长时会自动截断，避免刷屏。
- 支持所有 Miraheze Wiki（通过修改 API 地址即可适配其他站点）。

## 📦 安装

### 方法一：通过 Git 克隆（推荐）
```bash
cd /path/to/AstrBot/data/plugins
git clone https://github.com/Wqawa/astrbot_plugin_miraheze
