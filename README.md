# async-mediawiki
An asynchronous python libary to get mediawiki content

# Installation

It requires Python 3.5 or above and aiohttp

`pip3 install --user git+https://github.com/Gelbpunkt/async-mediawiki/`

# Usage
```python

import async_mediawiki as mediawiki
w = mediawiki.MediaWiki("https://en.wikipedia.org/w/api.php")
print(await w.get_html("Chemistry")) #page html when rendered 
print(await w.get_markdown("Chemistry")) #markdown, what you see when editing a page
print(await w.get_text("Chemistry")) #pure text without html and markdown
await w.close() #close the session

#you can also use this
w = mediawiki.MediaWiki()
print(await w.get_markdown("https://wiki.guildwars.com/api.php?action=query&titles=Ranger&prop=revisions&rvprop=content&format=json&formatversion=2"))
#the libary handles the URLs automatically when provided a base URL to the API

```
