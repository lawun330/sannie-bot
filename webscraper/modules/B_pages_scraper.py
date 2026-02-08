'''This script is used to get the list of page links from a particular topic url.'''

import os
import sys

# add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import modules from parent directory
from core_scraper import getNextPageUrl, getPageLimit, webScraper

# test
# execute only if the file is run as the main program
if __name__ == "__main__":
    # get a topic
    chosen_topic_url = "https://www.bbc.com/burmese/topics/c404v08p1wxt" # example

    # to store all pages of the topic
    list_of_page_urls = []

    # store the first page url
    list_of_page_urls.append(chosen_topic_url)

    # get the number of pages of the topic
    soup = webScraper(chosen_topic_url)
    total_pages = getPageLimit(soup)
    print(total_pages)

    # store the rest of the pages of the topic
    for _i in range(total_pages):
        try:
            url = getNextPageUrl(chosen_topic_url, soup)
            soup = webScraper(url)
            list_of_page_urls.append(url)
        except AttributeError:
            break
    print(list_of_page_urls)


# function implementation
def fetch_pages(topic_url):
    list_of_page_urls = []
    list_of_page_urls.append(topic_url)
    soup = webScraper(topic_url)
    total_pages = getPageLimit(soup)
    for _i in range(total_pages): # for demonstration 'x' is used # use 'total_pages' in actual implementation
        try:
            url = getNextPageUrl(topic_url, soup)
            soup = webScraper(url)
            list_of_page_urls.append(url)
        except AttributeError:
            print("ERROR")
            break
    return list_of_page_urls
