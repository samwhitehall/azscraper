azscraper
=========

Scrapes your Amazon recommendations and picks one item for you at random. Developed to play around 
with web scraping, particularly Selenium. I chose Amazon, for the following challenges:
* pagination
* bad, non-semantic HTML markup
* login required

The tool needs a file called `settings.py` in the `azscrape` directory with the following contents:
    
    EMAIL="amazon email accont here"
    PASSWORD="amazon password"
    NUM_PAGES=2
    NUM_THREADS=3
    
It works by scraping `NUM_PAGES` many pages, storing these URLs in a queue, and letting `NUM_THREADS` many 
worker threads (each with a browser) scrape these URLs for details. A random item is selected and printed
to `stdout`.
