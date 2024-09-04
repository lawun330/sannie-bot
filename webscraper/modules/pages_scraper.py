'''This script is used to get the list of page links from a particular topic url.'''

from main import webScraper, getNextPageUrl, getPageLimit
from topics_scraper import list_of_topics_urls

# test
# execute only if the file is run as the main program
if __name__ == "__main__":
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
    print(list_of_page_urls)


# function implementation
def fetch_pages(topic_url):
    list_of_page_urls = []
    list_of_page_urls.append(topic_url)
    soup = webScraper(topic_url)
    total_pages = getPageLimit(soup)
    for i in range(total_pages):
        try:
            url = getNextPageUrl(chosen_topic_url, soup)
            soup = webScraper(url)
            list_of_page_urls.append(url)
        except AttributeError:
            break
    return list_of_page_urls
