# import libraries
import pandas as pd
import requests  # this module helps us to download a web page
from bs4 import BeautifulSoup  # this module helps in web scrapping


# function to get soup with URL input
def web_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    return soup


# function to get specific elements within a soup
def soup_parser(soup):
    news_headers_soup = soup.find_all("a", {"class":"focusIndicatorDisplayBlock"})
    datetime_soup = soup.find_all("time", {"class":"promo-timestamp"})
    return news_headers_soup, datetime_soup


# function to create lists that are to be appended to original ones
def list_append(news_headers_soup, datetime_soup):
    news_headers_per_page = []
    datetime_per_page = []
    if len(news_headers_soup)==len(datetime_soup): # if the lengths are the same, start adding them to the lists

        for i in range(len(news_headers_soup)): # get index

            # list 1 for news headers
            try: # for news headers without video tag # video tagged ones will cause errors
                news_headers_per_page.append(news_headers_soup[i].string.strip()) # convert 'BeautifulSoup string' to 'Python string' # add content to list 1
            except AttributeError: # # for news headers with video tag
                # list() is used to convert 'BeautifulSoup tag' object to 'list' to enable iteration
                news_headers_per_page.append(list(news_headers_soup[i].span)[1].strip()) # convert 'BeautifulSoup string' to 'Python string' # add content to list 1

            # list 2 for date and time
            datetime_per_page.append(datetime_soup[i].string.strip()) # convert 'BeautifulSoup string' to 'Python string' # add content to list 2

        if (len(news_headers_per_page)==len(news_headers_soup)) & (len(datetime_per_page)==len(datetime_soup)): # if everything is added to two lists
            return news_headers_per_page, datetime_per_page


# function to get next page url
def navigate_next_page(web_url, soup):
    next_page_soup = soup.find("a", {"aria-labelledby":"pagination-next-page", "class":"focusIndicatorOutlineBlack", "href":True})
    complete_url = web_url + next_page_soup.attrs['href']
    return complete_url


# function to get the last page index
def get_max_page(soup):
    last_page_soup = soup.find_all("a", {"class":"focusIndicatorOutlineBlack", "href":True})[-2]
    last_page_index = int(last_page_soup.string)
    return last_page_index


# function to produce a spreadsheet
def export_excel(first_list, second_list):
    BBC = {}
    BBC['News Header'] = first_list
    BBC['Time'] = second_list
    df = pd.DataFrame({key:pd.Series(value) for key, value in BBC.items()})
    df.to_excel('BBC_webscraped_from_python.xlsx', index=False)
    return df


# the main function
def main(web_url):
    news_headers = []
    datetime = []

    # for the first page
    complete_url = web_url # initial url
    soup = web_scraper(complete_url) # get soup
    last_page_index = get_max_page(soup) # get last page index
    news_headers_soup, datetime_soup = soup_parser(soup) # get specific elements
    news_headers_new_list, datetime_new_list = list_append(news_headers_soup, datetime_soup) # extract data

    # append data to lists
    news_headers += news_headers_new_list
    datetime += datetime_new_list

    # from the second page to the last page
    for _i in range(last_page_index):
        try:
            print(complete_url)
            complete_url = navigate_next_page(web_url, soup) # get next url
            soup = web_scraper(complete_url) # get soup
            news_headers_soup, datetime_soup = soup_parser(soup) # get specific elements
            news_headers_new_list, datetime_new_list = list_append(news_headers_soup, datetime_soup) # extract data

            # append data to lists
            news_headers += news_headers_new_list
            datetime += datetime_new_list

        except AttributeError: # scraping the page after the last page will cause error
            print("The end of the pages is reached.")

    return export_excel(news_headers, datetime) # export the spreadsheet # return df


# run the main
if __name__ == "__main__":
    df = main("https://www.bbc.com/burmese/topics/c9wpm0en9jdt")
    print(df)
    print("Done")
