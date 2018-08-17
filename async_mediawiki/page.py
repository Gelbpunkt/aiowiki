import asyncio
import re
from html import unescape

class Page:

    def __init__(self, page_title, url, session, csrf):
        self.session = session
        self.base_url = url
        self.title = page_title
        self.csrf = csrf

    async def _html(self):
        """Helper function that downloads the page HTML."""
        url = f"{self.base_url}?action=parse&page={self.title}&format=json"
        async with self.session.get(url) as r:
            data = await r.json()
        html = data["parse"]["text"]["*"]
        unescape(html)
        return html

    async def _markdown(self):
        """Helper function to get page markdown."""
        url = f"{self.base_url}?action=query&titles={self.title}&prop=revisions&rvprop=content&format=json&formatversion=2"
        async with self.session.get(url) as r:
            data = await r.json()
        md = data["query"]["pages"][0]["revisions"][0]["content"]
        unescape(md)
        return md

    async def _summary(self):
        """Helper function to get page summary."""
        url = f"{self.base_url}?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={self.title}"
        async with self.session.get(url) as r:
            data = await r.json()
        summary = data["query"]["pages"][list(data["query"]["pages"].keys())[0]]["extract"]
        unescape(summary)
        return summary

    def _cleanhtml(self, raw_html):
        """Makes the Mediawiki HTML readable text."""

        #remove html tags
        cleantext = re.sub(r'<.*?>', '', raw_html)

        #remove the html comments
        cleantext = re.sub("(<!--.*?-->)", '', cleantext, flags=re.DOTALL)

        #remove lines with multiple spaces on them, happens after the regexes
        cleantext = "\n".join([r.strip() for r in cleantext.split("\n")])

        #remove multiple newlines which appeared after the regexes
        cleantext = re.sub(r"\n\n+", "\n\n", cleantext)

        #remove the edit things after the headings
        cleantext = cleantext.replace("[edit]", "")
        cleantext = cleantext.replace("(edit)", "")

        return cleantext

    @property
    async def html(self):
        return await self._html()

    @property
    async def markdown(self):
        return await self._markdown()

    @property
    async def text(self):
        raw_html = await self._html()
        return self._cleanhtml(raw_html)

    async def _edit(self, content: str):
        """Edits a page."""
        token = self.csrf or "+\\"
        json = {
        "action": "edit",
        "format": "json",
        "title": self.title,
        "text": content,
        "token": token
        }
        async with self.session.post(self.base_url, data=json) as r:
            return await r.json()
