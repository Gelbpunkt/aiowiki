import aiohttp

from .page import Page
from .exceptions import *
from .http import HTTPClient


class Wiki:
    def __init__(self, base_url: str, session: aiohttp.ClientSession = None):
        session = session or aiohttp.ClientSession()
        self.http = HTTPClient(url=base_url, session=session, logged_in=False)

    @classmethod
    def wikipedia(cls, language="en", *args, **kwargs):
        return cls(
            f"https://{language.lower()}.wikipedia.org/w/api.php", *args, **kwargs
        )

    async def close(self):
        """Close the aiohttp Session"""
        await self.http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exception_type, exception_value, traceback):
        await self.close()

    async def get_token(self, type: str = "csrf"):
        """Get an API token for a login attempt."""
        return await self.http.get_token(type)

    async def get_random_pages(self, num: int = 1, namespace: str = "*"):
        """Gets a list of random Page objects"""
        data = await self.http.get_random_pages(num, namespace)

        return [self.get_page(page) for page in data]

    async def create_account(
        self, username: str, password: str, email: str = None, real_name: str = None
    ):
        """Creates an account in the wiki. May fail if captchas are required."""
        json = {
            "username": username,
            "password": password,
            "retype": password,
            "email": email,
            "realname": real_name,
        }

        await self.http.create_account(json)
        return True

    async def login(self, username: str, password: str):
        """Logs in to the wiki."""
        json = {"username": username, "password": password}

        await self.http.login(json)
        return True

    def get_page(self, page_title: str):
        """Retrieves a page from the wiki. Returns a Page object."""
        return Page(page_title, wiki=self)
