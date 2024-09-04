'''This script is used to get the list of content links from a particular page link.'''

from main import webScraper, soupParser
from pages_scraper import list_of_page_urls

# get a page
chosen_page_url = list_of_page_urls[1]

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

# execute only if the file is run as the main program
if __name__ == "__main__":
    print(list_of_content_links)
