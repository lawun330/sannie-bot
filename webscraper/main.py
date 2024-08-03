# import libraries
import pandas as pd
import requests  # this module helps us to download a web page
from bs4 import BeautifulSoup  # this module helps in web scrapping
import os


# [1] function to get soup with URL input
def web_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')
    return soup


# [2] function to get specific elements within a soup
def soup_parser(soup):
    news_headers_soup = soup.find_all("a", {"class":"focusIndicatorDisplayBlock"})
    datetime_soup = soup.find_all("time", {"class":"promo-timestamp"})
    return news_headers_soup, datetime_soup


# [3] function to extract Burmese content from a content url
def content_scraper(content_url, soup):
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
        except AttributeError:
            continue # skip if there is None
    return burmese_content


# [4] function to create lists for a page
'''Lists are to be appended to original ones'''
def list_append_per_page(news_headers_soup, datetime_soup):
    news_headers_per_page = []
    datetime_per_page = []
    contents_per_page = []

    if len(news_headers_soup)==len(datetime_soup): # each header should have a corresponding date

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
            content_soup = web_scraper(content_url) # pass the link to create a new soup
            content_per_header = content_scraper(content_url, content_soup) # this new soup is used for content scraping
            contents_per_page.append(content_per_header)

        if (len(news_headers_per_page)==len(news_headers_soup)) & (len(datetime_per_page)==len(datetime_soup)) & (len(contents_per_page)!=0): # if everything is added to two lists
            return news_headers_per_page, datetime_per_page, contents_per_page


# [5] function to get next page url
def navigate_next_page(web_url, soup):
    next_page_soup = soup.find("a", {"aria-labelledby":"pagination-next-page", "class":"focusIndicatorOutlineBlack", "href":True})
    complete_url = web_url + next_page_soup.attrs['href']
    return complete_url


# [6] function to get the last page index
def get_max_page(soup):
    last_page_soup = soup.find_all("a", {"class":"focusIndicatorOutlineBlack", "href":True})[-2]
    last_page_index = int(last_page_soup.string)
    return last_page_index


# [7] function to produce a spreadsheet
def export_file(first_list, second_list, third_list, file_type="excel"):
    BBC = {}
    BBC['News Header'] = first_list
    BBC['Time'] = second_list
    BBC['Content'] = third_list
    df = pd.DataFrame({key:pd.Series(value) for key, value in BBC.items()})
    output_dir = "./spreadsheets/" # output directory
    if not os.path.exists(output_dir): # if the directory does not exist, create it
        os.makedirs(output_dir)
    if file_type == "excel": # default file type
        df.to_excel(os.path.join(output_dir, 'BBC_webscraped_from_python.xlsx'), index=False)
    elif file_type == "csv":
        df.to_csv(os.path.join(output_dir, 'BBC_webscraped_from_python.csv'), index=False)
    return df


# the main function
def main(web_url):
    news_headers = []
    datetime = []
    contents = []

    # for the first page
    complete_url = web_url # initial url
    soup = web_scraper(complete_url) # get soup
    last_page_index = get_max_page(soup) # get last page index
    news_headers_soup, datetime_soup = soup_parser(soup) # get specific elements in a soup

    # extract data
    news_headers_per_page, datetime_per_page, contents_per_page = list_append_per_page(news_headers_soup, datetime_soup)

    # append data to lists
    news_headers += news_headers_per_page
    datetime += datetime_per_page
    contents += contents_per_page

    # from the second page to the last page
    for _i in range(last_page_index):
        try:
            print(complete_url)
            complete_url = navigate_next_page(web_url, soup) # get next url
            soup = web_scraper(complete_url) # get soup
            news_headers_soup, datetime_soup = soup_parser(soup) # get specific elements in a soup

            # extract data
            news_headers_per_page, datetime_per_page, contents_per_page = list_append_per_page(news_headers_soup, datetime_soup)

            # append data to lists
            news_headers += news_headers_per_page
            datetime += datetime_per_page
            contents += contents_per_page

        except AttributeError: # scraping the page after the last page will cause error
            print("The end of the pages is reached.")

    return export_file(news_headers, datetime, contents, "csv") # export the spreadsheet # return df


# run the main
if __name__ == "__main__":
    df = main("https://www.bbc.com/burmese/topics/c9wpm0en9jdt")
    print(df)
    print("Done")
