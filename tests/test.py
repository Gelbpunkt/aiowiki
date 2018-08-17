import async_mediawiki as mw
import asyncio

async def test():
    wiki = mw.Wiki("https://wiki.idlerpg.fun/api.php")

    page = await wiki.get_page("Main Page")
    #await wiki.create_account("AdrianBotto2", "pass1234")
    await wiki.login("AdrianBotto2", "pass1234")
    await page.html # no print because it looks ugly...
    await asyncio.sleep(1)
    print(await page.markdown)
    await asyncio.sleep(1)
    print(await page.text)
    await asyncio.sleep(1)
    print(await page.edit("Test 1234 Bois!"))

    await wiki.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
