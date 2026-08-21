import aiohttp
import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import logger


class MirahezePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_url = "https://SEWH.miraheze.org/w/api.php"

    async def fetch_page_content(self, title: str) -> str:
        params = {
            "action": "parse",
            "page": title,
            "format": "json",
            "prop": "text",
            "formatversion": "2"
        }
        headers = {
            "User-Agent": "https://github.com/Wqawa/AstrBot-MirahezePlugin"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.get(self.api_url, params=params) as resp:
                    if resp.status != 200:
                        logger.error(f"API 请求失败，状态码: {resp.status}")
                        return f"❌ 请求失败，状态码: {resp.status}"

                    data = await resp.json()
                    if "error" in data:
                        error_msg = data["error"].get("info", "未知错误")
                        logger.error(f"MediaWiki API 错误: {error_msg}")
                        return f"❌ API 错误: {error_msg}"

                    html_content = data.get("parse", {}).get("text", "")
                    if not html_content:
                        return f"⚠️ 未找到页面 '{title}' 的内容，请检查页面名是否正确。"

                    plain_text = re.sub(r'<[^>]+>', '', html_content)
                    plain_text = re.sub(r'\n\s*\n', '\n\n', plain_text).strip()
                    if len(plain_text) > 1500:
                        plain_text = plain_text[:1500] + "...\n(内容过长，已截断)"
                    return plain_text

            except aiohttp.ClientError as e:
                logger.error(f"网络请求异常: {e}")
                return f"❌ 网络请求异常: {e}"
            except Exception as e:
                logger.error(f"解析响应时发生异常: {e}")
                return f"❌ 处理响应时发生异常: {e}"

    @filter.command("wiki")
    async def query_wiki(self, event: AstrMessageEvent):
        message = event.message_str.strip()
        parts = message.split(maxsplit=1)
        if len(parts) < 2:
            yield event.plain_result("❌ 用法: /wiki <页面标题>\n例如: /wiki Main_Page")
            return
        page_title = parts[1].strip()
        if not page_title:
            yield event.plain_result("❌ 请提供要查询的页面标题。")
            return

        yield event.plain_result(f"🔍 正在查询 Wiki 页面: {page_title} ...")
        content = await self.fetch_page_content(page_title)
        yield event.plain_result(f"📄 **{page_title}** 的内容:\n\n{content}")

    async def terminate(self):
        logger.info("Miraheze 插件已卸载")
