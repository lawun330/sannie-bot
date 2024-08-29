#!/usr/bin/env python

# import libraries
import time  # this module pauses the process

import pandas as pd
import redis  # this module tracks the scraping progress
import requests  # this module helps us to download a web page
from bs4 import BeautifulSoup  # this module helps in web scrapping

# the main website url
main_url = "https://www.bbc.com/burmese"


# ## Initialization For Cache System
# redis
r = redis.Redis(host='localhost', port=6379, db=0)
SCRAPING_KEY = "currently_scraping_url" # the directory name
error_found = False


# ## Necessary Functions to Use Redis
# function to start and track the scraping process
def setCache(url):
    r.set(SCRAPING_KEY, url) # store url in cache

# function to reset scraping
def resetCache():
    r.set(SCRAPING_KEY, main_url) # set cache to main url

# function to resume scraping
def scrapeCache():
    cache_url = r.get(SCRAPING_KEY).decode('utf-8') # retrieve current url
    global error_found # refer to global variable
    try:
        response = requests.get(cache_url) # try scraping
        error_found = False
        return response
    except:
        error_found = True
        return None


# ## Necessary Functions to Scrape One Page of One Topic
# function to get soup with URL input of one topic
def webScraper(url):
    setCache(url) # store url in cache
    response = scrapeCache() # try scraping the url from cache
    while(error_found): # continue scraping until the connection comes back
        print("  - Connection Error. Retrying in 5 seconds...")
        time.sleep(5) # wait 5 seconds
        response = scrapeCache()
    soup = BeautifulSoup(response.content, 'html5lib')
    return soup

# function to get specific elements within a soup of one topic
def soupParser(soup):
    news_headers_soup = soup.find_all("a", {"class":"focusIndicatorDisplayBlock"}) # filter headers
    datetime_soup = soup.find_all("time", {"class":"promo-timestamp"}) # filter datetime
    return news_headers_soup, datetime_soup

# function to extract Burmese content from a content url of one topic
def contentScraper(content_url, soup):
    burmese_content = ""
    alphabets = ['a', 'b', 'c', 'd', 'e',
                'f', 'g', 'h', 'i', 'j',
                'k', 'l', 'm', 'n', 'o',
                'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y',
                'z']

    symbols = ["\'", "(", ")"]

    for p_element in soup.find_all("p"):
        try: # None Type can cause error
            content = p_element.string.strip()
            for char in content:
                if (char.lower() in alphabets) or (char in symbols): # do not add non-Burmese characters or symbols
                    continue
                burmese_content += char # add Burmese characters only
        except:
            pass
    return burmese_content

# function to create lists for a page of one topic
'''Return three lists containing corresponding entries of a page of one topic'''
def appendListPerPage(news_headers_soup, datetime_soup):
    news_headers_per_page = []
    datetime_per_page = []
    contents_per_page = []

    if len(news_headers_soup) == len(datetime_soup): # each header should have a corresponding date

        for i in range(len(news_headers_soup)): # get index of headers for one page

            # list 1 for multiple headers in a page
            try: # for news headers without video tag # video tagged ones will cause errors
                news_headers_per_page.append(news_headers_soup[i].string.strip()) # convert 'BeautifulSoup string' to 'Python string' # add content to list 1
            except AttributeError: # # for news headers with video tag
                '''list() is used to convert 'BeautifulSoup tag' object to 'list' to enable iteration'''
                news_headers_per_page.append(list(news_headers_soup[i].span)[1].strip()) # convert 'BeautifulSoup string' to 'Python string' # add content to list 1

            # list 2 for date and time in a page
            datetime_per_page.append(datetime_soup[i].string.strip()) # convert 'BeautifulSoup string' to 'Python string' # add content to list 2

            # list 3 for contents of all headers in a page (contents of multiple headers)
            content_url = news_headers_soup[i].attrs['href'] # get a link from 'n' element
            content_soup = webScraper(content_url) # pass the link to create a new soup
            content_per_header = contentScraper(content_url, content_soup) # this new soup is used for content scraping
            contents_per_page.append(content_per_header)

        if (len(news_headers_per_page) == len(news_headers_soup)) & (len(datetime_per_page) == len(datetime_soup)) & (len(contents_per_page) != 0): # if everything is added to two lists
            return news_headers_per_page, datetime_per_page, contents_per_page


# ## Necessary Functions to Scrape All Pages of One Topic
# function to get next page url of one topic
def getNextPageUrl(web_url, soup):
    next_page_soup = soup.find("a", {"aria-labelledby":"pagination-next-page", "class":"focusIndicatorOutlineBlack", "href":True})
    complete_url = web_url + next_page_soup.attrs['href']
    return complete_url

# function to get the last page index of one topic
def getPageLimit(soup):
    last_page_soup = soup.find_all("a", {"class":"focusIndicatorOutlineBlack", "href":True})[-2] # filter the second last item # discard last item
    last_page_index = int(last_page_soup.string)
    return last_page_index


# ## Necessary Function to Scrape All Pages of All Topics
# function to get all topics urls
def getTopicsUrls(soup):
    default_page_initial = "https://www.bbc.com"
    list_of_topics_urls = []

    list_of_topics = soup.find_all("a", {"class":"focusIndicatorRemove bbc-qh9e61 e11sm0on3" , "href":True}) # filter topics
    for topic in list_of_topics:
        list_of_topics_urls.append(default_page_initial + topic.attrs['href'])

    return list_of_topics_urls


# ## Necessary Functions to Store Data
# function to create an empty dataframe
def createDF():
    BBC = {}
    BBC['News Header'] = []
    BBC['Time'] = []
    BBC['Content'] = []
    df = pd.DataFrame(BBC)
    return df

# function to add a row to an existing dataframe
def addDF(existing_df, row_list):
    next_index = len(existing_df.index)
    existing_df.loc[next_index] = row_list
    return existing_df

# function to add rows (of one full page) to an existing dataframe
def addDFs(existing_df, news_headers_list, datetime_list, contents_list):
    for i in range(len(news_headers_list)):
        existing_df = addDF(existing_df, [news_headers_list[i], datetime_list[i], contents_list[i]]) # addDF(df, [item1, item2, item3])
    return existing_df

# function to produce a spreadsheet
def exportExcel(df, file_name_string: str):
    parent_directory = '../spreadsheets/'
    extension = '.xlsx'
    full_directory = parent_directory + file_name_string + extension

    try:
        df.to_excel(full_directory, index=False)
        return True
    except:
        print("Error creating a spreadsheet!")
        return False


# ## Functions Integration to Scrape All Pages of One Topic
# function to scrape all pages of one topic
def scrapeTopic(web_url, file_name_string: str):
    news_headers_per_page = []
    datetime_per_page = []
    contents_per_page = []

    # initialize an empty dataframe for each topic
    df = createDF()

    # the first page
    complete_url = web_url # initial url
    soup = webScraper(complete_url) # get soup
    last_page_index = getPageLimit(soup) # get last page index
    news_headers_soup, datetime_soup = soupParser(soup) # get specific elements in a soup
    print("Total pages:", last_page_index)

    '''Add data per page to dataframe'''

    # extract data
    news_headers_per_page, datetime_per_page, contents_per_page = appendListPerPage(news_headers_soup, datetime_soup)

    # write data to df
    df = addDFs(df, news_headers_per_page, datetime_per_page, contents_per_page)

    # from the second page to the last page
    for _i in range(3): # for demonstration 'x' is used # use 'last_page_index' in actual implementation
        # try:
            print(f"- scraping {complete_url}")
            complete_url = getNextPageUrl(web_url, soup) # get next url
            soup = webScraper(complete_url) # get soup
            news_headers_soup, datetime_soup = soupParser(soup) # get specific elements in a soup

            '''Add data per page to dataframe'''

            # extract data
            news_headers_per_page, datetime_per_page, contents_per_page = appendListPerPage(news_headers_soup, datetime_soup)

            # write data to df
            df = addDFs(df, news_headers_per_page, datetime_per_page, contents_per_page)

        # except AttributeError: # scraping the page after the last page will cause error
            # print("All pages of this topic is scraped.")

    exportExcel(df, file_name_string) # export the spreadsheet
    # print(df) # check df of one topic


# ## Functions Integration to Scrape All Pages of All Topics
# function to scrape all pages of all topics
def scrapeAllTopics(main_url):
    topics_soup = webScraper(main_url)
    list_of_topics_urls = getTopicsUrls(topics_soup)

    # iterate all topics
    for topic_url in list_of_topics_urls:
        try:
            file_name_string = 'BBC_Burmese_topic_' + str(list_of_topics_urls.index(topic_url) + 1) # example: BBC_Burmese_topic_1
            print(f'In the process of making "{file_name_string}" spreadsheet ...')
            scrapeTopic(topic_url, file_name_string)
            print("The process completes successfully.")
            print()
        except:
            print(f"Error with the current topic url: {topic_url}")
            continue # continue scraping next topic
    print("Hopefully, everything is scraped!")


# # Main
scrapeAllTopics(main_url)
