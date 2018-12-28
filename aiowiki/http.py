from .exceptions import *
from html import unescape


class HTTPClient:
    """A Proxy object for all API actions"""

    def __init__(self, url, session, logged_in):
        self.url = url
        self.session = session
        self.logged_in = logged_in

    async def close(self):
        """Closes the aiohttp Session"""
        await self.session.close()

    async def get_token(self, type):
        """Gets an API token"""
        url = f"{self.url}?action=query&meta=tokens&type={type}&format=json"
        async with self.session.get(url) as r:
            data = await r.json()

        try:
            return data["query"]["tokens"][f"{type}token"]
        except KeyError:
            raise TokenGetError(data["error"]["info"])

    async def get_random_pages(self, num, namespace):
        """Gets random page names"""
        url = f"{self.url}?action=query&list=random&rnlimit={num}&rnnamespace={namespace}&format=json"
        async with self.session.get(url) as r:
            data = await r.json()

        return [p["title"] for p in data["query"]["random"]]

    async def create_account(self, json):
        """Creates an account"""
        token = await self.get_token("createaccount")
        json["action"] = "createaccount"
        json["format"] = "json"
        json["createreturnurl"] = self.url
        json["createtoken"] = token

        async with self.session.post(self.url, data=json) as r:
            json = await r.json()
        if json["createaccount"]["status"] == "FAIL":
            raise CreateAccountError(json["createaccount"]["messagecode"])
        return True

    async def login(self, json):
        """Logs in to the wiki"""
        token = await self.get_token("login")
        json["action"] = "clientlogin"
        json["loginreturnurl"] = self.url
        json["format"] = "json"
        json["rememberMe"] = 1
        json["logintoken"] = token

        async with self.session.post(self.url, data=json) as r:
            json = await r.json()
        if json["clientlogin"]["status"] == "FAIL":
            raise LoginFailure(json["clientlogin"]["message"])
        self.logged_in = True
        return True

    async def get_html(self, page):
        """Gets Page html"""
        url = f"{self.url}?action=parse&page={page}&format=json"
        async with self.session.get(url) as r:
            data = await r.json()
        try:
            html = data["parse"]["text"]["*"]
        except KeyError:
            raise PageNotFound("Unknown Page or error when getting html")
        unescape(html)
        return html

    async def get_markdown(self, page):
        """Gets Page markdown"""
        url = f"{self.url}?action=query&titles={page}&prop=revisions&rvprop=content&format=json&formatversion=2"
        async with self.session.get(url) as r:
            data = await r.json()
        try:
            md = data["query"]["pages"][0]["revisions"][0]["content"]
        except KeyError:
            raise PageNotFound("Unknown Page or error when getting markdown")
        unescape(md)
        return md

    async def get_summary(self, page):
        """Gets Page summary"""
        url = f"{self.url}?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={page}"
        async with self.session.get(url) as r:
            data = await r.json()
        try:
            pages = data["query"]["pages"]
            summary = pages[list(pages.keys())[0]]["extract"]
        except KeyError:
            raise PageNotFound("Unknown Page or error when getting summary")
        unescape(summary)
        return summary

    async def edit_page(self, json):
        """Edits a page's content"""
        if self.logged_in:
            token = await self.get_token("csrf")
        else:
            token = "+\\"
        json["action"] = "edit"
        json["format"] = "json"
        json["token"] = token
        async with self.session.post(self.url, data=json) as r:
            data = await r.json()
        if data.get("error"):
            raise EditError(data["error"]["info"])
        return True

    async def opensearch(self, title, limit, namespace):
        """Searches for a page title and returns limit results as a list"""
        url = f"{self.url}?action=opensearch&search={title}&limit={limit}&namespace={namespace}&format=json"
        async with self.session.get(url) as r:
            data = await r.json()
        return data[1]

    async def get_urls(self, title):
        """Searches for URLs matching a title and returns edit URL and page URL in a list"""
        url = f"{self.url}?action=query&format=json&prop=info&generator=allpages&inprop=url&gapfrom={title}&gaplimit=1"
        async with self.session.get(url) as r:
            data = await r.json()
        pages = data["query"].get("pages")
        if not pages:
            raise PageNotFound("Unknown Page or error when getting page URLs")
        page = list(pages.items())[0][1]
        return [page["fullurl"], page["editurl"]]

    async def get_media(self, title):
        """Searches for media on a specific page and returns a list of URLs"""
        url = f"{self.url}?action=query&titles={title}&format=json&prop=images"
        async with self.session.get(url) as r:
            data = await r.json()
        pages = data["query"]["pages"]
        images = list(pages.values())[0].get("images")
        if not images:  # either no images or unknown page
            return []
        query = "|".join([i["title"] for i in images])
        url = f"{self.url}?action=query&titles={query}&format=json&prop=imageinfo&iiprop=url"
        async with self.session.get(url) as r:
            data = await r.json()
        pages = data["query"]["pages"]
        urls = [
            i["imageinfo"][0]["url"] for i in pages.values()
        ]  # imageinfo does not exist if file unknown, but these all exist
        return urls
