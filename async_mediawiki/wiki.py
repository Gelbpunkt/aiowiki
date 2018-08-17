import aiohttp
import asyncio

from .page import Page

class Wiki:

    def __init__(self, base_url: str, session=None, loop=None):
        self.base_url = base_url
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)
        self.logged_in = False

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

        async with self.session.get(self.base_url) as r:
            data = await r.json()

        return data["query"]["tokens"][f"{type}token"]

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
            return await r.json()

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
            return await r.json()

    async def get_page(self, page_title: str):
        """Retrieves a page from the wiki. Returns a Page object."""
        if self.logged_in:
            token = await self._get_token("csrf")
        else:
            token = None
        return Page(page_title, self.base_url, self.session, token)
