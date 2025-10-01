'''
This script is the API for the BBC Burmese News website.
It uses redis to cache the data so that the data is not scraped again.

There is a series of scraping process:
- scrape topic links from the main page (already done)
- scrape links of pages from a topic link
- scrape links of contents from a page link
- scrape content/article from a content link

Topic links are already associated with the dropdown menu in the index page.
The user can select a topic from the dropdown menu to view the pages of the topic.
The user can select a page to view all available contents of the page.
The user can select a content url to copy and return to the index page.
The user can insert a url in the index page to read the content/article in the article page.

The API is used by the following files:
- index.js: to get topic links and display them in the dropdown menu
- loading.js: to test data completion by fetching data from the cache to continue the redirecting process
- pages.js: to get page links and display them in the container
- contents.js: to get content links and display them in the container
- article.js: to get content/article and display it

In each endpoint, the data is serialized to JSON strings to be stored in Redis because Redis can only store strings.
In each endpoint, the data is deserialized back to Python objects before being returned to the client.
'''

# import libraries
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import redis
import time
import os
import json

# import custom functions from webscraping modules
from webscraper.modules import fetch_pages  # B_pages_scraper
from webscraper.modules import fetch_content_links  # C_content_links_scraper
from webscraper.modules import get_article  # D_content_or_article_scraper

# create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]  # Exposes all headers
)

# create Redis client
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0') # get Redis URL from environment variable or use local Redis
redis_client = redis.from_url(redis_url, decode_responses=True) # create Redis client

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

# A. WORKING WITH CHOSEN TOPIC
# /pages contains links of pages of the chosen topic
    # cache the links of pages in Redis
    # retrieve the links of pages from cache
@app.get("/pages")
def read_pages():
    topic_link = redis_client.get(redis_javascript_cache_keys[0]) # get chosen topic link from cache
    try:    # try scraping the links of pages
        data = fetch_pages(topic_link)
    except:   # if connection error, retry until the connection comes back
        error_found = True
        while(error_found):
            print("  - Connection Error. Retrying in 5 seconds...")
            time.sleep(5) # wait 5 seconds
            data = fetch_pages(topic_link) # try scraping again
    redis_client.set(redis_scraped_cache_keys[0], json.dumps(data))  # Serialize data to JSON string to cache links of pages
    cache = redis_client.get(redis_scraped_cache_keys[0]) # get links of pages from cache
    return json.loads(cache)  # Deserialize the JSON string back to a Python object

# B. WORKING WITH CHOSEN PAGE
# /contents contains links of contents of the chosen page
    # cache the links of contents in Redis
    # retrieve the links of contents from cache
@app.get("/contents")
def read_contents():
    page_link = redis_client.get(redis_javascript_cache_keys[1])  # get chosen page link from cache
    try:    # try scraping the links of contents
        data = fetch_content_links(page_link)
    except:   # if connection error, retry until the connection comes back
        error_found = True
        while(error_found):
            print("  - Connection Error. Retrying in 5 seconds...")
            time.sleep(5)  # wait 5 seconds
            data = fetch_content_links(page_link)  # try scraping again
    redis_client.set(redis_scraped_cache_keys[1], json.dumps(data))  # Serialize to JSON string to cache links of contents
    cache = redis_client.get(redis_scraped_cache_keys[1])  # get links of contents from cache
    return json.loads(cache)  # Deserialize back to Python object

# C. WORKING WITH CHOSEN CONTENT/ARTICLE
# /article contains the content/article of the chosen content link
    # cache the content/article in Redis
    # retrieve the content/article from cache
@app.get("/article")
def read_article():
    content_link = redis_client.get(redis_javascript_cache_keys[2]) # get chosen content link from cache 
    try:    # try scraping the content/article
        data = get_article(content_link)
    except:   # if connection error, retry until the connection comes back
        error_found = True
        while(error_found):
            print("  - Connection Error. Retrying in 5 seconds...")
            time.sleep(5) # wait 5 seconds
            data = get_article(content_link) # try scraping again
    redis_client.set(redis_scraped_cache_keys[2], json.dumps(data)) # Serialize to JSON string to cache content/article
    cache = redis_client.get(redis_scraped_cache_keys[2]) # get content/article from cache
    return json.loads(cache) # Deserialize back to Python object


# run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)