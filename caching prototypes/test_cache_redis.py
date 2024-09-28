'''This script is a test script to implement redis and fastAPI to cache webscraped data which is to be processed later.'''

# import libraries
from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI, HTTPException
import redis

# redis
r = redis.Redis(host='localhost', port=6379, db=0)

# fastAPI
app = FastAPI()

cache = "" # variable to store cache

# function to write and read cache
@app.get("/")
def read_scrape():
    response = requests.get(f"https://www.bbc.com/burmese")
    global cache
    cache = r.get("bbc") # retrieve cache
    if cache:
        print("cache is hit")
    else:
        print("cache is not hit")
        r.set("bbc", response.content)  # store cache
    return response.content

cache = r.get("bbc") # retrieve cache
soup = BeautifulSoup(cache, 'html.parser') # make a soup
print(soup.title) # check a title # if a title return, the work is successful