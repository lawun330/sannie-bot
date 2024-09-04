'''This script is used to get the content from a particular content link.'''

from main import webScraper, contentScraper
from content_links_scraper import list_of_content_links

# test
# execute only if the file is run as the main program
if __name__ == "__main__":
    # get a content link
    content_url = list_of_content_links[0]

    # get the content from the content link
    content_soup = webScraper(content_url)
    parsed_content = contentScraper(content_url, content_soup)
    print(parsed_content)


# function implementation
def get_content(content_url):
    content_soup = webScraper(content_url)
    parsed_content = contentScraper(content_url, content_soup)
    return parsed_content
