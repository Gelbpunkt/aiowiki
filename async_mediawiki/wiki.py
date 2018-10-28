import aiohttp

from .page import Page
from .exceptions import *

class Wiki:

    def __init__(self, base_url: str, session=None, loop=None, test=True):
        self.base_url = base_url
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)
        self.logged_in = False
        if test:
            if not base_url.endswith("api.php"):
                raise BadWikiUrl("The wiki URL doesn\'t end with \'api.php\'. Add test=True if you want to skip this warning")

    @classmethod
    def wikipedia(cls, language="en", *args, **kwargs):
        return cls(f"https://{language.lower()}.wikipedia.org/w/api.php", *args, **kwargs)

    async def close(self):
        """Close the aiohttp Session"""
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exception_type, exception_value, traceback):
        await self.close()

    async def _get_token(self, type="csrf"):
        """Get an API token for a login attempt."""
        url = f"{self.base_url}?action=query&meta=tokens&type={type}&format=json"

        async with self.session.get(url) as r:
            data = await r.json()

        try:
            return data["query"]["tokens"][f"{type}token"]
        except KeyError:
            raise TokenGetError(data["error"]["info"])

    async def _rand_pages(self, num: int=1, namespace: str="*"):
        """Gets num random pages in namespace namespace"""
        url = f"{self.base_url}?action=query&list=random&rnlimit={num}&rnnamespace={namespace}&format=json"

        async with self.session.get(url) as r:
            data = await r.json()

        pages = []
        for page in data["query"]["random"]:
            pages.append(await self.get_page(page["title"]))

        return pages

    async def create_account(self, username: str, password: str, email: str=None, real_name: str=None):
        """Creates an account in the wiki. May fail if captchas are required."""
        token = await self._get_token(type="createaccount")
        json = {
        "action": "createaccount",
        "format": "json",
        "username": username,
        "password": password,
        "retype": password,
        "createtoken": token,
        "createreturnurl": self.base_url
         }
        if email:
            json["email"] = email
        if real_name:
            json["realname"] = real_name

        async with self.session.post(self.base_url, data=json) as r:
            json = await r.json()
        if json.get("error"):
            raise CreateAccountError(json["error"]["info"])
        return True

    async def login(self, username: str, password: str):
        """Logs in to the wiki."""
        token = await self._get_token(type="login")
        json = {
        "action": "clientlogin",
        "loginreturnurl": self.base_url,
        "username": username,
        "password": password,
        "format": "json",
        "rememberMe": 1,
        "logintoken": token
        }

        self.logged_in = True #todo: put this only on success

        async with self.session.post(self.base_url, data=json) as r:
            json = await r.json()
        if json.get("error"):
            raise LoginFailure(json["error"]["info"])
        return True

    async def get_page(self, page_title: str):
        """Retrieves a page from the wiki. Returns a Page object."""
        return Page(page_title, self.base_url, self.session, self.logged_in)

    async def get_random_pages(self, num: int=1, namespace: str="*"):
        """Returns a list of Page objects from random wiki pages"""
        return await self._rand_pages(num, namespace)
