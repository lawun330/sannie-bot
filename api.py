# impor libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import custom modules
from webscraper.modules.pages_scraper import fetch_pages
from webscraper.modules.content_links_scraper import fetch_content_links
from webscraper.modules.content_scraper import get_content

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/api/topic-pages")
async def get_topic_pages(url: str):
    pages = fetch_pages(url)
    return {"pages": pages}

@app.get("/api/page-links")
async def get_page_links(url: str):
    links = fetch_content_links(url)
    return {"links": links}

@app.get("/api/content")
async def get_content(url: str):
    content = get_content(url)
    return {"content": content}
