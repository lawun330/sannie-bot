'''This script is used to get the content from a particular content link.'''

from main import webScraper, contentScraper
from content_links_scraper import list_of_content_links

content_url = list_of_content_links[0]

content_soup = webScraper(content_url)
parsed_content = contentScraper(content_url, content_soup)

if __name__ == "__main__":
    print(parsed_content)