'''This script is used to get the list of page links from a particular topic url.'''

from main import webScraper, getNextPageUrl, getPageLimit
from topics_scraper import list_of_topics_urls

# get a topic
chosen_topic_url = list_of_topics_urls[1]

# to store all pages of the topic
list_of_page_urls = []

# store the first page url
list_of_page_urls.append(chosen_topic_url)

# get the number of pages of the topic
soup = webScraper(chosen_topic_url)
total_pages = getPageLimit(soup)

# store the rest of the pages of the topic
for i in range(total_pages):
    try:
        url = getNextPageUrl(chosen_topic_url, soup)
        soup = webScraper(url)
        list_of_page_urls.append(url)
    except AttributeError:
        break

# execute only if the file is run as the main program
if __name__ == "__main__":
    print(list_of_page_urls)
