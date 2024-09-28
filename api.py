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
import json

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
    try:
        data = await request.json()
        topic_link = data.get('topic')
        if not topic_link:
            return {"error": "No topic link provided"}
        
        redis_client.setex(redis_javascript_cache_keys[0], CACHE_EXPIRATION, topic_link)
        return {"message": "Topic set successfully"}
    except redis.RedisError as e:
        return {"error": f"Redis error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.post("/set_chosen_page")
async def set_page(request: Request):
    try:
        data = await request.json()
        page_link = data.get('page')
        if not page_link:
            return {"error": "No page link provided"}
        
        redis_client.setex(redis_javascript_cache_keys[1], CACHE_EXPIRATION, page_link)
        return {"message": "Page set successfully"}
    except redis.RedisError as e:
        return {"error": f"Redis error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.post("/set_chosen_content")
async def set_content(request: Request):
    try:
        data = await request.json()
        content_link = data.get('content')
        if not content_link:
            return {"error": "No content link provided"}
        
        redis_client.setex(redis_javascript_cache_keys[2], CACHE_EXPIRATION, content_link)
        return {"message": "Content set successfully"}
    except redis.RedisError as e:
        return {"error": f"Redis error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

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
    topic_link = redis_client.get(redis_javascript_cache_keys[0]) # get topic link from cache
    try:    # try scraping the page links
        data = fetch_pages(topic_link)
    except:   # if connection error, retry until the connection comes back
        error_found = True
        while(error_found):
            print("  - Connection Error. Retrying in 5 seconds...")
            time.sleep(5) # wait 5 seconds
            data = fetch_pages(topic_link) # try scraping again
    redis_client.set(redis_scraped_cache_keys[0], json.dumps(data))  # Serialize the data to a JSON string
    cache = redis_client.get(redis_scraped_cache_keys[0]) # get pages from cache
    return json.loads(cache)  # Deserialize the JSON string back to a Python object

# WORKING WITH CHOSEN PAGE
# /contents contains the content links of the chosen page
    # cache the content links in Redis
    # retrieve the content links from cache
@app.get("/contents")
def read_content_links():
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
