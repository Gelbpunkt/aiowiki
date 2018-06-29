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
    
    async def _html(self, pageTitle:str):
        """Helper function that downloads the page HTML."""
        if not self.baseUrl:
            url = pageTitle
        else:
            url = f"{self.baseUrl}?action=parse&page={pageTitle}&format=json"
        async with self.session.get(url) as r:
            data = await r.json()
        return data["parse"]["text"]["*"]

    async def _markdown(self, pageTitle:str):
        """Helper function to get page markdown."""
        if not self.baseUrl:
            url = pageTitle
        else:
            url = f"{self.baseUrl}?action=query&titles={pageTitle}&prop=revisions&rvprop=content&format=json&formatversion=2"
        async with self.session.get(url) as r:
            data = await r.json()
        return data["query"]["pages"][0]["revisions"][0]["content"]
    
    async def get_text(self, pageTitle:str):
        """Get a page content. Either from URL or a page in the URL from the constructer."""

            



        data = await self._html(pageTitle)


        return self._cleanhtml(data)
    
    async def get_html(self, pageTitle:str):
        """Get the raw page HTML. Either from URL or page in defined wiki."""
        return await self._html(pageTitle)
    
    async def get_markdown(self, pageTitle:str):
        return await self._markdown(pageTitle)
