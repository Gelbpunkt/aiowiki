import async_mediawiki as mw
import asyncio

async def test_working():
    wiki = mw.Wiki.wikipedia("en")

    #await wiki.create_account("test", "pass1234")
    #await wiki.login("test", "pass1234")
    print(await wiki.get_random_pages(3))
    async with wiki.get_page("Mediawiki") as page:
        print(dir(page))
        print(await page.summary)

    await wiki.close()

async def test_crash():
    async with mw.Wiki("bad wiki url here if you want") as wiki:
        p = await wiki.get_page("page does not exist")
        print(await p.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(test_working())
loop.run_until_complete(test_crash())
