'''This script is used to get the content from a particular content link.'''

import sys
import os

# add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import modules from parent directory 
from main import webScraper, contentScraper


# test
# execute only if the file is run as the main program
if __name__ == "__main__":
    # get a content link
    content_url = 'https://www.bbc.com/burmese/articles/clldd5j76pno' # example

    # get the content from the content link
    content_soup = webScraper(content_url)
    parsed_content = contentScraper(content_url, content_soup)
    print(parsed_content)


# function implementation
def get_content(content_url):
    content_soup = webScraper(content_url)
    parsed_content = contentScraper(content_url, content_soup)
    return parsed_content
