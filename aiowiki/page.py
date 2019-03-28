import re
from collections import namedtuple


class Page:
    """Represents a Page in the :meth:`~aiowiki.Wiki`.
    This is usually acquired by :meth:`~aiowiki.Wiki.get_page` or other methods, and not created directly.

    :param str page_title: The title of the page.
    :param wiki: The :meth:`~aiowiki.Wiki` object this page belongs to.
    :type wiki: :class:`~aiowiki.Wiki`

    :ivar title: The page title
    :ivar wiki: The :meth:`~aiowiki.Wiki` it belongs to
    """

    def __init__(self, page_title, wiki):
        self.title = page_title
        self.wiki = wiki

    def __repr__(self):
        return f"<aiowiki.page.Page title={self.title}>"

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

    async def html(self):
        """The pure page HTML."""
        return await self.wiki.http.get_html(self.title)

    async def markdown(self):
        """The Markdown version of the page content."""
        return await self.wiki.http.get_markdown(self.title)

    async def text(self):
        """The text of the page without HTML tags."""
        raw_html = await self.html()
        return self._cleanhtml(raw_html)

    async def summary(self):
        """The summary of the page, usually the first paragraph."""
        return await self.wiki.http.get_summary(self.title)

    async def urls(self):
        """A namedtuple representing the view and edit URL for the page."""
        url_tuple = namedtuple("WikiURLs", ["view", "edit"])
        urls = await self.wiki.http.get_urls(self.title)
        return url_tuple(urls[0], urls[1])

    async def media(self):
        """Returns a list of all media used on the page."""
        return await self.wiki.http.get_media(self.title)

    async def edit(self, content: str):
        """Edits the page."""
        json = {"title": self.title, "text": content}
        await self.wiki.http.edit_page(json)
        return True
