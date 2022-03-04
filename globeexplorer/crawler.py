import re
import requests
from bs4 import BeautifulSoup
import sys

from globeexplorer.utils import get_https_domain

pages = []
pages_to_crawl = []

# TODO: change to asynchronous
def get_internal_links_and_crawl(domain, url):
    global pages
    html = requests.get(url).text # fstrings require Python 3.6+ 
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        if "href" in link.attrs:
            if domain in link.attrs["href"]:
                if link.attrs["href"] not in pages:
                    new_page = link.attrs["href"]
                    pages_to_crawl.append(new_page)
            elif '.html' in link.attrs["href"]:
                new_page = get_https_domain(domain) + '/' + link.attrs["href"]
                if new_page not in pages:
                    pages_to_crawl.append(new_page)
        
def get_links(domain, url):
    global pages
    global pages_to_crawl
    pages_to_crawl.append(url)

    while len(pages_to_crawl) > 0:
        next_page = pages_to_crawl.pop(0)
        if next_page not in pages:
            pages.append(next_page)
            get_internal_links_and_crawl(domain, next_page)

    return pages
