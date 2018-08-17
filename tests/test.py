import async_mediawiki as mw
import asyncio

async def test():
    wiki = mw.Wiki("https://wiki.idlerpg.fun/api.php")

    page = await wiki.get_page("TEST")
    await wiki.create_account("AdrianBotto", "pass1234")
    await wiki.login("AdrianBotto", "pass1234")
    print(await page.html)
    await asyncio.sleep(1)
    print(await page.markdown)
    await asyncio.sleep(1)
    print(await page.text)
    await asyncio.sleep(1)
    await page.edit("Test 1234 Bois!")

    await wiki.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
