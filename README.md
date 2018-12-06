# aiowiki
An asynchronous python libary to get mediawiki content

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f634a400d4ed40ec8f51b1ce0f43fd5e)](https://www.codacy.com/app/Gelbpunkt/aiowiki?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Gelbpunkt/aiowiki&amp;utm_campaign=Badge_Grade)
[![BCH compliance](https://bettercodehub.com/edge/badge/Gelbpunkt/async-mediawiki?branch=master)](https://bettercodehub.com/)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FGelbpunkt%2Fasync-mediawiki.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FGelbpunkt%2Fasync-mediawiki?ref=badge_shield)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![CircleCI](https://img.shields.io/circleci/project/github/Gelbpunkt/aiowiki/master.svg?label=CircleCI)](https://circleci.com/gh/Gelbpunkt/aiowiki)
[![License](https://img.shields.io/pypi/l/aiowiki.svg)](https://github.com/Gelbpunkt/aiowiki/blob/master/LICENSE)

## Installation

It requires Python 3.6 or above and aiohttp

`pip3 install aiowiki`

Development Version:

`pip3 install git+https://github.com/Gelbpunkt/aiowiki`

## Quick start
```python
import aiowiki

wiki = aiowiki.Wiki.wikipedia("en") # We're using the alternate constructor for pre-made Wikipedia Wikis
await wiki.login("test", "pass1234") # Logging in (optional)

pages = await wiki.get_random_pages(3) # get a list of random pages

page = wiki.get_page("aiowiki") # get a specific page

print(await page.html) # print the pure page html
print(await page.markdown) # print the pure page markdown (wiki code)
print(await page.text) # print the page's text (library handles filtering of the HTML)

await page.edit("That's a nice lib!") # edit the page, automatically uses the logged in user or anonymous

await wiki.close() # the Wiki object also supports a context manager (async with) to close automatically
```

## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FGelbpunkt%2Fasync-mediawiki.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FGelbpunkt%2Fasync-mediawiki?ref=badge_large)
