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
    content_data = []

    # get the relevant part of the soup for the page
    soup = webScraper(chosen_page_url) 
    news_headers_soup, datetime_soup = soupParser(soup)

    # store all content links of the page
    for i in range(len(news_headers_soup)):
        try:
            content_url = news_headers_soup[i].attrs['href']
            try:
                header = news_headers_soup[i].string.strip()
            except AttributeError:
                header = list(news_headers_soup[i].span)[1].strip()      
            content_data.append({
                'url': content_url,
                'header': header
            })
        except AttributeError:
            break
    print(content_data)


# function implementation
def fetch_content_links(chosen_page_url):
    content_data = []
    soup = webScraper(chosen_page_url) 
    news_headers_soup, datetime_soup = soupParser(soup)
    for i in range(len(news_headers_soup)):
        try:
            content_url = news_headers_soup[i].attrs['href']

            # Extract header text
            try:
                header = news_headers_soup[i].string.strip()
            except AttributeError:
                # Handle video-tagged headers
                header = list(news_headers_soup[i].span)[1].strip()
            
            content_data.append({
                'url': content_url,
                'header': header
            })
        except AttributeError:
            break
    return content_data