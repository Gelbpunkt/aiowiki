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
        await page.summary  # should have a page, so it actually fetches there
        await wiki.close()

    async def test_working_by_wikipedia(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        self.assertEqual(wiki.http.url, "https://en.wikipedia.org/w/api.php")
        page = wiki.get_page("Python (programming language)")
        await page.summary  # should have a page, so it actually fetches there
        await wiki.close()

    @asynctest.skipIf(small_test)
    async def test_page_edit(self):
        wiki = aiowiki.Wiki(AIOWIKI_TEST_URL)
        page = wiki.get_page("Spam")
        await page.edit("Eggs & Ham")
        await wiki.close()

    @asynctest.skipIf(small_test)
    async def test_login(self):
        wiki = aiowiki.Wiki(AIOWIKI_TEST_URL)
        with self.assertRaises(aiowiki.LoginFailure):
            await wiki.login("Test1234", "pass1234")
        await wiki.login(AIOWIKI_TEST_USERNAME, AIOWIKI_TEST_PASSWORD)
        await wiki.close()

    @asynctest.skipIf(small_test)
    async def test_create_account(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        with self.assertRaises(aiowiki.CreateAccountError):
            await wiki.create_account("Test1234", "pass1234")
        await wiki.close()
        async with aiowiki.Wiki(AIOWIKI_TEST_URL) as wiki:
            await wiki.create_account(
                f"Test{randint(1, 100000000)}", f"pass{randint(1, 1000000000)}"
            )

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
        self.assertTrue("Nicolas Cage" in await page.text)
        self.assertTrue((await page.markdown).startswith("{{pp-vandalism|small=yes}}"))
        self.assertTrue(
            (await page.summary).startswith(
                "Nicolas Kim Coppola (born January 7, 1964)"
            )
        )
        self.assertTrue((await page.urls).view.startswith("https://en.wikipedia.org"))
        await wiki.close()


asynctest.main()
