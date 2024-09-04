'''This script is used to get the list of topics urls from the main url of the website.'''

from main import webScraper, getTopicsUrls

# get the main url of the website
main_url = "https://www.bbc.com/burmese"

# test
# execute only if the file is run as the main program
if __name__ == "__main__":
    # get the list of topics urls
    topics_soup = webScraper(main_url)
    list_of_topics_urls = [main_url]
    list_of_topics_urls_from_getTopicsUrls = getTopicsUrls(topics_soup)

    # store the list of topics urls
    for url in list_of_topics_urls_from_getTopicsUrls:
        list_of_topics_urls.append(url)
    print(list_of_topics_urls)


# function implementation
def fetch_topics(main_url):
    topics_soup = webScraper(main_url)
    list_of_topics_urls = [main_url]
    list_of_topics_urls_from_getTopicsUrls = getTopicsUrls(topics_soup)
    for url in list_of_topics_urls_from_getTopicsUrls:
        list_of_topics_urls.append(url)
    return list_of_topics_urls
