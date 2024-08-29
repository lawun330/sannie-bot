# import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from fastapi import FastAPI, HTTPException
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

cache = ""

# fastAPI
app = FastAPI()


@app.get("/")
def read_scrape():
    response = requests.get(f"https://www.bbc.com/burmese")
    global cache
    cache = r.get("bbc")
    if cache:
        print("cache is hit")
    else:
        print("cache is not hit")
        r.set("bbc", response.content)
    return response.content

cache = r.get("bbc")
soup = BeautifulSoup(cache, 'html.parser')
print(soup.title)