'''This script is used to get the list of content links from a particular page link.'''

import sys
import os

# add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import modules from parent directory 
from main import webScraper, soupParser


# test
# execute only if the file is run as the main program
if __name__ == "__main__":
    # get a page
    chosen_page_url = 'https://www.bbc.com/burmese/topics/c404v08p1wxt?page=35' # example

    # to store all content links of the page
    list_of_content_links = []

    # get the relevant part of the soup for the page
    soup = webScraper(chosen_page_url) 
    news_headers_soup, datetime_soup = soupParser(soup)

    # store all content links of the page
    for i in range(len(news_headers_soup)):
        try:
            content_url = news_headers_soup[i].attrs['href']
            list_of_content_links.append(content_url)
        except AttributeError:
            break
    print(list_of_content_links)


# function implementation
def fetch_content_links(chosen_page_url):
    list_of_content_links = []
    soup = webScraper(chosen_page_url) 
    news_headers_soup, datetime_soup = soupParser(soup)
    for i in range(len(news_headers_soup)):
        try:
            content_url = news_headers_soup[i].attrs['href']
            list_of_content_links.append(content_url)
        except AttributeError:
            break
    return list_of_content_links
