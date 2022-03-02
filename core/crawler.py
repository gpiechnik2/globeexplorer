import re
import requests
from bs4 import BeautifulSoup


pages = []

# TODO: change function to make asynchronous crawling with the threading library
def get_internal_links_and_crawl(domain, url):
    global pages
    html = requests.get(url).text # fstrings require Python 3.6+ 
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.find_all("a"):
        if "href" in link.attrs:
            if domain in link.attrs["href"]:
                if link.attrs["href"] not in pages:
                    new_page = link.attrs["href"]
                    pages.append(new_page)
                    get_links(domain, new_page)
        
def get_links(domain, url):
    get_internal_links_and_crawl(domain, url)
    return pages
