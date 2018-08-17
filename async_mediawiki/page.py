import asyncio
import re
from html import unescape
from .exceptions import *

class Page:

    def __init__(self, page_title, url, session, logged_in):
        self.session = session
        self.base_url = url
        self.title = page_title
        self.logged_in = logged_in

    async def __aexit__(self, exception_type, exception_value, traceback):
        pass

    async def _get_token(self, type="csrf"):
        """Get an API token for actions requiring authorization."""
        url = f"{self.base_url}?action=query&meta=tokens&type={type}&format=json"

        async with self.session.get(url) as r:
            data = await r.json()

        try:
            return data["query"]["tokens"][f"{type}token"]
        except KeyError:
            raise TokenGetError(data["error"]["info"])

    async def _html(self):
        """Helper function that downloads the page HTML."""
        url = f"{self.base_url}?action=parse&page={self.title}&format=json"
        async with self.session.get(url) as r:
            data = await r.json()
        try:
            html = data["parse"]["text"]["*"]
        except KeyError:
            raise PageNotFound("Unknown Page or error when getting html")
        unescape(html)
        return html

    async def _markdown(self):
        """Helper function to get page markdown."""
        url = f"{self.base_url}?action=query&titles={self.title}&prop=revisions&rvprop=content&format=json&formatversion=2"
        async with self.session.get(url) as r:
            data = await r.json()
        try:
            md = data["query"]["pages"][0]["revisions"][0]["content"]
        except KeyError:
            raise PageNotFound("Unknown Page or error when getting markdown")
        unescape(md)
        return md

    async def _summary(self):
        """Helper function to get page summary."""
        url = f"{self.base_url}?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={self.title}"
        async with self.session.get(url) as r:
            data = await r.json()
        try:
            summary = data["query"]["pages"][list(data["query"]["pages"].keys())[0]]["extract"]
        except KeyError:
            raise PageNotFound("Unknown Page or error when getting summary")
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

    async def edit(self, content: str):
        """Edits the page."""
        if self.logged_in:
            token = await self._get_token(type="csrf")
        else:
            token = "+\\"
        json = {
        "action": "edit",
        "format": "json",
        "title": self.title,
        "text": content,
        "token": token
        }
        async with self.session.post(self.base_url, data=json) as r:
            data = await r.json()
        if data.get("error"):
            raise EditError(data["error"]["info"])
        return True
