import async_mediawiki as mw
import asyncio

async def test_working():
    wiki = mw.Wiki("https://wiki.idlerpg.fun/api.phps")

    #await wiki.create_account("AdrianBotto2", "pass1234")
    print(await wiki.login("AdrianBotto2", "pa"))
    page = await wiki.get_page("Main Page")
    await page.html # no print because it looks ugly...
    await asyncio.sleep(1)
    print(await page.markdown)
    await asyncio.sleep(1)
    print(await page.text)
    await asyncio.sleep(1)
    print(await page.edit("Test 1234 Bois!"))

    await wiki.close()

async def test_crash():
    async with mw.Wiki("https://wiki.idlerpg.fun/api.php") as wiki:
        p = await wiki.get_page("skfjsdklfjkl")
        print(await p.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(test_working())
loop.run_until_complete(test_crash())
