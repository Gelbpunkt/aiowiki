import async_mediawiki as mw
import asyncio

async def test():
    wiki = mw.Wiki("https://en.wikipedia.org/w/api.php")

    page = await wiki.get_page("Discord")
    print(await page.html) # or get_markdown or get_text
    await asyncio.sleep(1)
    #or this
    async with wiki.get_page("Nicolas Cage") as p:
        print(await p.markdown)

    #async_mediawiki.Exceptions.UnknownPageError

    await wiki.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
