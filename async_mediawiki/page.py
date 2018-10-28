import re
from .exceptions import *


class Page:
    def __init__(self, page_title, wiki):
        self.title = page_title
        self.wiki = wiki

    def _cleanhtml(self, raw_html):
        """Makes the Mediawiki HTML readable text."""

        # remove html tags
        cleantext = re.sub(r"<.*?>", "", raw_html)

        # remove the html comments
        cleantext = re.sub("(<!--.*?-->)", "", cleantext, flags=re.DOTALL)

        # remove lines with multiple spaces on them, happens after the regexes
        cleantext = "\n".join([r.strip() for r in cleantext.split("\n")])

        # remove multiple newlines which appeared after the regexes
        cleantext = re.sub(r"\n\n+", "\n\n", cleantext)

        # remove the edit things after the headings
        cleantext = cleantext.replace("[edit]", "")
        cleantext = cleantext.replace("(edit)", "")

        return cleantext

    @property
    async def html(self):
        return await self.wiki.http.get_html(self.title)

    @property
    async def markdown(self):
        return await self.wiki.http.get_markdown(self.title)

    @property
    async def text(self):
        raw_html = await self.html
        return self._cleanhtml(raw_html)

    @property
    async def summary(self):
        return await self.wiki.http.get_summary(self.title)

    async def edit(self, content: str):
        """Edits the page."""
        json = {"title": self.title, "text": content}
        await self.wiki.http.edit_page(json)
        return True
