import async_mediawiki as mw
import asyncio

async def test_working():
    wiki = mw.Wiki("api.php endpoint here")

    await wiki.create_account("test", "pass1234")
    await wiki.login("test", "pass1234")
    print(await wiki.get_random_pages(3))
    page = wiki.get_page("My Fancy Page")
    print(await page.text)

    await page.edit("TEST")

    await wiki.close()

async def test_crash():
    async with mw.Wiki("api.php endpoint here") as wiki:
        p = await wiki.get_page("page does not exist")
        print(await p.text)
        await wiki.login("wronguser", "wrongpass")
        await p.edit("I don't have perms to do so!")

loop = asyncio.get_event_loop()
loop.run_until_complete(test_working())
loop.run_until_complete(test_crash())
