import aiohttp, re, asyncio


class MediaWiki:

    def __init__(self, baseUrl=None, session=None):
        self.baseUrl = baseUrl
        if not session:
            self.session = aiohttp.ClientSession()
        else:
            self.session = session

    async def close(self):
        """Close the connection."""
        await self.session.close()

    def _cleanhtml(self, raw_html):
        """Makes the Mediawiki HTML readable text."""

	#remove html tags
        cleantext = re.sub(r'<.*?>', '', raw_html)

        #remove the html coments
        cleantext = re.sub("(<!--.*?-->)", '', cleantext, flags=re.DOTALL)

	#remove lines with multiple spaces on them, happens after the regexes
        cleantext = "\n".join([r.strip() for r in cleantext.split("\n")])

	#remove multiple newlines which appeared after the regexes
        cleantext = re.sub(r"\n\n+", "\n\n", cleantext)

	#remove the edit things after the headings
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


    async def _get_token(self, url, type="csrf"):
        """Get an API token for a login attempt."""
        url = f"{url}?action=query&meta=tokens&type={type}&format=json"
        async with self.session.get(url) as r:
            data = await r.json()

        return data["query"]["tokens"][f"{type}token"]

    async def _edit(self, pageTitle:str, content:str, token:str, url=None):
        """Edits a page."""
        if self.baseUrl and not url:
            url = self.baseUrl
        json = {
	"action": "edit",
	"format": "json",
	"title": pageTitle,
	"text": content,
	"token": token
        }
        async with self.session.post(url, data=json) as r:
            return await r.json()

    async def get_text(self, pageTitle:str):
        """Get a page content. Either from URL or a page in the URL from the constructer."""
        data = await self._html(pageTitle)
        return self._cleanhtml(data)

    async def get_html(self, pageTitle:str):
        """Get the raw page HTML. Either from URL or page in defined wiki."""
        return await self._html(pageTitle)

    async def get_markdown(self, pageTitle:str):
        """Get the MediaWiki markdown of a page."""
        return await self._markdown(pageTitle)

    async def edit_page(self, pageTitle:str, content:str, token="+\\", url=None):
        """Edit a page in the wiki."""
        return await self._edit(pageTitle, content=content, token=token, url=url)

    async def create_account(self, userName:str, userPassword:str, userEmail=None, userRealName=None, url=None):
        """Creates an account in the wiki. May fail if captchas are required."""
        url = url or self.baseUrl
        token = await self._get_token(url, type="createaccount")
        json = {
        "action": "createaccount",
        "format": "json",
        "username": userName,
        "password": userPassword,
        "retype": userPassword,
        "email": userEmail,
        "realname": userRealName,
        "createtoken": token,
        "createreturnurl": url
        }
        async with self.session.post(url, data=json) as r:
            return await r.json()
