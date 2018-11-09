import asynctest

try:
    import aiowiki
except ImportError:
    import async_mediawiki as aiowiki  # old global install, meh

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

    @asynctest.skip
    async def test_page_edit(self):
        wiki = aiowiki.Wiki("Wiki Spam Url Here")
        page = wiki.get_page("Spam")
        await page.edit("Eggs & Ham")
        await wiki.close()

    @asynctest.skip
    async def test_login(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        with self.assertRaises(aiowiki.LoginFailure):
            await wiki.login("Test1234", "pass1234")
        await wiki.login("myrealuser", "myrealpass")
        await wiki.close()

    async def test_create_account(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        with self.assertRaises(aiowiki.CreateAccountError):
            await wiki.create_account("Test1234", "pass1234")
        await wiki.close()
        #async with aiowiki.Wiki("my spam url") as wiki:
        #    await wiki.create_account("Test1234", "pass1234")

    async def test_page_attrs(self):
        wiki = aiowiki.Wiki.wikipedia("en")
        page = wiki.get_page("Nicolas Cage")
        self.assertTrue("Nicolas Cage" in await page.text)
        self.assertTrue((await page.markdown).startswith("{{pp-vandalism|small=yes}}"))
        self.assertTrue((await page.summary).startswith("Nicolas Kim Coppola (born January 7, 1964)"))
        await wiki.close()

asynctest.main()
