import async_mediawiki as mw
import asyncio

async def test_working():
    wiki = mw.Wiki("wiki api url here")

    await wiki.create_account("test", "pass1234")
    await wiki.login("test", "pass1234")
    print(await wiki.get_random_pages(3))
    page = await wiki.get_page("Mediawiki")
    await page.html # no print because it looks ugly and is long
    await asyncio.sleep(1)
    print(await page.markdown)
    await asyncio.sleep(1)
    print(await page.text)
    await asyncio.sleep(1)
    print(await page.edit("Test 1234 Bois!"))

    await wiki.close()

async def test_crash():
    async with mw.Wiki("bad wiki url here if you want") as wiki:
        p = await wiki.get_page("page does not exist")
        print(await p.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(test_working())
loop.run_until_complete(test_crash())
