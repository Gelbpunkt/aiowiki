import aiohttp, re, asyncio


class MediaWiki:

    def __init__(self, baseUrl=None):
        self.baseUrl = baseUrl
        self.session = aiohttp.ClientSession()

    async def close(self):
        """Close the connection."""
        await self.session.close()

    def _cleanhtml(self, raw_html):
        """Makes the Mediawiki HTML readable text."""
        cleantext = re.sub(r'<.*?>', '', raw_html)
        cleanr2 = re.compile("<!--.*?-->")
        cleantext = re.sub("(<!--.*?-->)", '', cleantext, flags=re.DOTALL)
        cleantext = "\n".join([r.strip() for r in cleantext.split("\n")])
        cleantext = re.sub(r"\n\n+", "\n\n", cleantext)
        cleantext = cleantext.replace("[edit]", "")
        cleantext = cleantext.replace("(edit)", "")
        return cleantext

    async def get(self, pageTitle:str):
        """Get a page content. Either from URL or a page in the URL from the constructer."""
        if not self.baseUrl:
            url = pageTitle
        else:
            url = f"{self.baseUrl}?action=parse&page={pageTitle}&format=json"
        async with self.session.get(url) as r:
            data = await r.json()

        data = data["parse"]["text"]["*"]
        return self._cleanhtml(data)
