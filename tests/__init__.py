import asynctest

try:
    import aiowiki
except ImportError:
    import async_mediawiki as aiowiki  # old global install, meh


@asynctest.lenient
class Test_Wiki_Object_Initalization(asynctest.TestCase):
    async def test_working_by_url(self):
        wiki = aiowiki.Wiki("https://en.wikipedia.org/w/api.php")
        self.assertEqual(wiki.http.url, "https://en.wikipedia.org/w/api.php")
        page = wiki.get_page("Python (programming language)")
        await page.summary  # should have a page, so it actually fetches there
        await wiki.close()

    async def test_not_working_by_url(self):
        wiki = aiowiki.Wiki("https://does-not-exist.com/invalid-path.php")
        self.assertEqual(wiki.http.url, "https://does-not-exist.com/invalid-path.php")
        with self.assertRaises(aiowiki.PageNotFound):
            page = wiki.get_page("Python (programming language)")
            await page.summary
        await wiki.close()


asynctest.main()
