'''
This script is the API for the BBC Burmese News website.
It uses redis to cache the data so that the data is not scraped again.

There is a series of scraping process:
- scrape topic links from the main page (already done)
- scrape page links from a topic link
- scrape content links from a page link
- scrape content from a content link

Topic links are already associated with the dropdown menu in the index page.
'''

# import libraries
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import redis
import time

# import custom functions from webscraping modules
from webscraper.modules import fetch_pages  # B_pages_scraper
from webscraper.modules import fetch_content_links  # C_content_links_scraper
from webscraper.modules import get_content  # D_content_scraper

# create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# create Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# create Redis cache keys
redis_javascript_cache_keys = ["chosen_topic", "chosen_page", "chosen_content"]
redis_scraped_cache_keys = ["pages", "contents", "article"]

# variables
CACHE_EXPIRATION = 3600  # Set expiration time for cache entries (1 hour)
error_found = False

# SETTING CHOSEN TOPIC, PAGE, AND CONTENT
# such data are sent from javascript to the API
# cache them in Redis
@app.post("/set_chosen_topic")
async def set_topic(request: Request):
    data = await request.json()
    topic_link = data.get('topic')
    redis_client.set(redis_javascript_cache_keys[0], topic_link)
    return {"message": "Topic set successfully"}

@app.post("/set_chosen_page")
async def set_page(request: Request):
    data = await request.json()
    page_link = data.get('page')
    redis_client.set(redis_javascript_cache_keys[1], page_link)
    return {"message": "Page set successfully"}

@app.post("/set_chosen_content")
async def set_content(request: Request):
    data = await request.json()
    content_link = data.get('content')
    redis_client.set(redis_javascript_cache_keys[2], content_link)
    return {"message": "Content set successfully"}


# DEBUGGING
# read the chosen topic, page, and content from cache with fastAPI
@app.get("/get_chosen_topic")
def read_topic():
    cache = redis_client.get(redis_javascript_cache_keys[0])
    return cache

@app.get("/get_chosen_page")
def read_page():
    cache = redis_client.get(redis_javascript_cache_keys[1])
    return cache

@app.get("/get_chosen_content")
def read_content():
    cache = redis_client.get(redis_javascript_cache_keys[2])
    return cache


# GETTING CHOSEN TOPIC, PAGE, AND CONTENT

# WORKING WITH CHOSEN TOPIC
# /pages contains the page links of the chosen topic
    # cache the page links in Redis
    # retrieve the page links from cache
@app.get("/pages")
def read_pages():
    cache = redis_client.get(redis_scraped_cache_keys[0]) # get pages from cache
    if cache: # if cache is not empty
        return cache
    else: # if cache is empty
        topic_link = redis_client.get(redis_javascript_cache_keys[0]) # get topic link from cache
        try:    # try scraping the page links
            data = fetch_pages(topic_link)
        except:   # if connection error, retry until the connection comes back
            error_found = True
            while(error_found):
                print("  - Connection Error. Retrying in 5 seconds...")
                time.sleep(5) # wait 5 seconds
                data = fetch_pages(topic_link) # try scraping again
        redis_client.set(redis_scraped_cache_keys[0], data) # set pages in cache
        cache = redis_client.get(redis_scraped_cache_keys[0]) # get pages from cache
        return cache

# WORKING WITH CHOSEN PAGE
# /contents contains the content links of the chosen page
    # cache the content links in Redis
    # retrieve the content links from cache
@app.get("/contents")
def read_content_links():
    cache = redis_client.get(redis_scraped_cache_keys[1]) # get content links from cache
    if cache: # if cache is not empty
        return cache
    else: # if cache is empty
        page_link = redis_client.get(redis_javascript_cache_keys[1]) # get page link from cache
        try:    # try scraping the content links
            data = fetch_content_links(page_link)
        except:   # if connection error, retry until the connection comes back
            error_found = True
            while(error_found):
                print("  - Connection Error. Retrying in 5 seconds...")
                time.sleep(5) # wait 5 seconds
                data = fetch_content_links(page_link) # try scraping again
        redis_client.set(redis_scraped_cache_keys[1], data) # set content links in cache
        cache = redis_client.get(redis_scraped_cache_keys[1]) # get content links from cache
        return cache


# WORKING WITH CHOSEN CONTENT
# /article contains the content of the chosen content link
    # cache the content in Redis
    # retrieve the content from cache
@app.get("/article")
def read_content():
    cache = redis_client.get(redis_scraped_cache_keys[2]) # get content from cache
    if cache: # if cache is not empty
        return cache
    else: # if cache is empty
        content_link = redis_client.get(redis_javascript_cache_keys[2]) # get content link from cache
        try:    # try scraping the content
            data = get_content(content_link)
        except:   # if connection error, retry until the connection comes back
            error_found = True
            while(error_found):
                print("  - Connection Error. Retrying in 5 seconds...")
                time.sleep(5) # wait 5 seconds
                data = get_content(content_link) # try scraping again
        redis_client.set(redis_scraped_cache_keys[2], data) # set content in cache
        cache = redis_client.get(redis_scraped_cache_keys[2]) # get content from cache
        return cache


# run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
