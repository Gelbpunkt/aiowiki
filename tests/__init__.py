import asynctest
import aiowiki
import os
from random import randint

AIOWIKI_TEST_URL = os.environ.get("AIOWIKI_TEST_URL")
AIOWIKI_TEST_USERNAME = os.environ.get("AIOWIKI_TEST_USERNAME")
AIOWIKI_TEST_PASSWORD = os.environ.get("AIOWIKI_TEST_PASSWORD")

if not AIOWIKI_TEST_URL or not AIOWIKI_TEST_USERNAME or not AIOWIKI_TEST_PASSWORD:
    small_test = True
else:
    small_test = False


@asynctest.lenient
class Test_Aiowiki(asynctest.TestCase):
    async def test_working_by_url(self):
        wiki = aiowiki.Wiki("https://en.wikipedia.org/w/api.php")
        self.assertEqual(wiki.http.url, "https://en.wikipedia.org/w/api.php")
        page = wiki.get_page("Python (programming language)")
        await page.summary()  # should have a page, so it actually fetches there
        await wiki.close()

    async def test_working_by_wikipedia(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        self.assertEqual(wiki.http.url, "https://en.wikipedia.org/w/api.php")
        self.assertEqual(
            repr(wiki), "<aiowiki.wiki.Wiki url=https://en.wikipedia.org/w/api.php>"
        )
        page = wiki.get_page("Python (programming language)")
        await page.summary()  # should have a page, so it actually fetches there
        await wiki.close()

    @asynctest.skipIf(small_test, "No enviroment variables for testing set up")
    async def test_page_edit(self):
        wiki = aiowiki.Wiki(AIOWIKI_TEST_URL)
        page = wiki.get_page("Spam")
        try:
            await page.edit("Eggs & Ham")
        except aiowiki.EditError as e:
            if not "action you have requested is limited to users in the group" in str(
                e
            ):
                raise
            else:
                await wiki.login(AIOWIKI_TEST_USERNAME, AIOWIKI_TEST_PASSWORD)
                await page.edit("Eggs & Ham")
        await wiki.close()

    @asynctest.skipIf(small_test, "No enviroment variables for testing set up")
    async def test_login(self):
        wiki = aiowiki.Wiki(AIOWIKI_TEST_URL)
        with self.assertRaises(aiowiki.LoginFailure):
            await wiki.login("Test1234", "pass1234")
        await wiki.login(AIOWIKI_TEST_USERNAME, AIOWIKI_TEST_PASSWORD)
        await wiki.close()

    @asynctest.skipIf(small_test, "No enviroment variables for testing set up")
    async def test_create_account_and_userrights(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        with self.assertRaises(aiowiki.CreateAccountError):
            await wiki.create_account("Test1234", "pass1234")
        await wiki.close()
        async with aiowiki.Wiki(AIOWIKI_TEST_URL) as wiki:
            name = f"Test{randint(1, 100000000)}"
            await wiki.create_account(name, f"pass{randint(1, 1000000000)}")
            await wiki.userrights(name, "add", "bureaucrat")
            await wiki.userrights(name, "remove", "bureaucrat")

    async def test_random_pages(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        pages = await wiki.get_random_pages(5)
        self.assertTrue(isinstance(pages[0], aiowiki.Page))
        await wiki.close()

    async def test_opensearch(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        pages = await wiki.opensearch("Python")
        self.assertTrue(isinstance(pages[0], aiowiki.Page))
        await wiki.close()

    async def test_page_attrs(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        page = wiki.get_page("Nicolas Cage")
        self.assertTrue("Nicolas Cage" in await page.text())
        self.assertTrue("{{pp-vandalism|small=yes}}" in await page.markdown())
        self.assertTrue(
            "Nicolas Kim Coppola (born January 7, 1964)" in await page.summary()
        )
        self.assertTrue((await page.urls()).view.startswith("https://en.wikipedia.org"))
        self.assertTrue(len(await page.media()) > 0)
        self.assertTrue(repr(page) == "<aiowiki.page.Page title=Nicolas Cage>")
        await wiki.close()


asynctest.main()
