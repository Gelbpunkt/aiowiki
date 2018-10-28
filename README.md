# async-mediawiki
An asynchronous python libary to get mediawiki content

[![BCH compliance](https://bettercodehub.com/edge/badge/Gelbpunkt/async-mediawiki?branch=master)](https://bettercodehub.com/)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FGelbpunkt%2Fasync-mediawiki.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FGelbpunkt%2Fasync-mediawiki?ref=badge_shield)

## Installation

It requires Python 3.6 or above and aiohttp

`pip3 install async-mediawiki`

## Usage
```python
import async_mediawiki as mw

wiki = mw.Wiki("wiki api url here") #make a Wiki object which is the key to the library
await wiki.create_account("test", "pass1234") #create an account in the wiki
await wiki.login("test", "pass1234") #login with the newly made user
await wiki.get_random_pages(3) #get a list of pages

page = await wiki.get_page("Mediawiki") #get a specific page
print(await page.html) #print the pure page html
print(await page.markdown) #print the pure page markdown (wiki code)
print(await page.text) #print the page's text (library handled filtering of the HTML)

await page.edit("That's a nice lib!") #edit the page, automatically uses the logged in user or anonymous
await wiki.close() #the Wiki object also supports a context manager (async with) to close automatically
```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FGelbpunkt%2Fasync-mediawiki.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FGelbpunkt%2Fasync-mediawiki?ref=badge_large)
