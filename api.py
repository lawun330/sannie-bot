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
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis
import time
import os
import json

# import custom functions from webscraping modules
from webscraper.modules import fetch_pages  # B_pages_scraper
from webscraper.modules import fetch_content_links  # C_content_links_scraper
from webscraper.modules import get_article  # D_content_or_article_scraper

from db import dynamo_helpers

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
CACHE_EXPIRATION = 3600  # set expiration time for cache entries (1 hour)

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
    # retrieve from Redis -> fail -> retrieve from DynamoDB -> fail -> scrape the pages -> save to both
@app.get("/pages")
def read_pages():
    topic_link = redis_client.get(redis_javascript_cache_keys[0]) # get chosen topic link from cache
    if not topic_link:
        raise HTTPException(status_code=400, detail="No topic chosen")
    redis_key = "pages:" + topic_link # create Redis cache key
    cached = redis_client.get(redis_key) # retrieve from Redis
    if cached:
        return json.loads(cached)
    data = dynamo_helpers.get_pages(topic_link) # if not found, retrieve from DynamoDB
    if data is not None:
        redis_client.setex(redis_key, CACHE_EXPIRATION, json.dumps(data)) # save to Redis
        return data
    while True: # if not found in Redis or DynamoDB, scrape the pages
        try:
            data = fetch_pages(topic_link)
            break
        except Exception:
            print("  - Connection Error. Retrying in 5 seconds...")
            time.sleep(5) # wait 5 seconds
    dynamo_helpers.put_pages(topic_link, data) # save to DynamoDB
    redis_client.setex(redis_key, CACHE_EXPIRATION, json.dumps(data)) # save to Redis
    return data

# B. WORKING WITH CHOSEN PAGE
# /contents contains links of contents of the chosen page
    # retrieve from Redis -> fail -> retrieve from DynamoDB -> fail -> scrape the contents -> save to both
@app.get("/contents")
def read_contents():
    page_link = redis_client.get(redis_javascript_cache_keys[1]) # get chosen page link from cache
    if not page_link:
        raise HTTPException(status_code=400, detail="No page chosen")
    redis_key = "contents:" + page_link # create Redis cache key
    cached = redis_client.get(redis_key) # retrieve from Redis
    if cached:
        return json.loads(cached)
    data = dynamo_helpers.get_contents(page_link) # if not found, retrieve from DynamoDB
    if data is not None:
        redis_client.setex(redis_key, CACHE_EXPIRATION, json.dumps(data)) # save to Redis
        return data
    while True: # if not found in Redis or DynamoDB, scrape the contents
        try:
            data = fetch_content_links(page_link)
            break
        except Exception:
            print("  - Connection Error. Retrying in 5 seconds...")
            time.sleep(5) # wait 5 seconds
    dynamo_helpers.put_contents(page_link, data) # save to DynamoDB
    redis_client.setex(redis_key, CACHE_EXPIRATION, json.dumps(data)) # save to Redis
    return data

# C. WORKING WITH CHOSEN CONTENT/ARTICLE
# /article contains the content/article of the chosen content
    # retrieve from Redis -> fail -> retrieve from DynamoDB -> fail -> scrape the content/article -> save to both
@app.get("/article")
def read_article():
    content_link = redis_client.get(redis_javascript_cache_keys[2]) # get chosen content link from cache
    if not content_link:
        raise HTTPException(status_code=400, detail="No content chosen")
    redis_key = "article:" + content_link # create Redis cache key
    cached = redis_client.get(redis_key) # retrieve from Redis
    if cached:
        return json.loads(cached)
    data = dynamo_helpers.get_article(content_link) # if not found, retrieve from DynamoDB
    if data is not None:
        redis_client.setex(redis_key, CACHE_EXPIRATION, json.dumps(data)) # save to Redis
        return data
    while True: # if not found in Redis or DynamoDB, scrape the content/article
        try:
            data = get_article(content_link)
            break
        except Exception:
            print("  - Connection Error. Retrying in 5 seconds...")
            time.sleep(5) # wait 5 seconds
    dynamo_helpers.put_article(content_link, data) # save to DynamoDB
    redis_client.setex(redis_key, CACHE_EXPIRATION, json.dumps(data)) # save to Redis
    return data


# run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)