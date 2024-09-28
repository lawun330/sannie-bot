from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import redis

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

## add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# test with test_client_receiving_FastAPI.js
@app.get("/")
def read_root():
    return "Hello World!"


# test with test_client_sending_FastAPI.js
## Store what javascript sends

@app.post("/set_topic")
async def set_topic(request: Request):
    data = await request.json()
    topic_link = data.get('topic')
    redis_client.set("chosen_topic", topic_link)
    return {"message": "Topic set successfully"}

@app.post("/set_page")
async def set_page(request: Request):
    data = await request.json()
    page_link = data.get('page')
    redis_client.set("chosen_page", page_link)
    return {"message": "Page set successfully"}

@app.post("/set_content")
async def set_content(request: Request):
    data = await request.json()
    content_link = data.get('content')
    redis_client.set("chosen_content", content_link)
    return {"message": "Content set successfully"}

## Check what is stored

@app.get("/get_topic")
async def get_topic():
    topic_link = redis_client.get("chosen_topic")
    return topic_link

@app.get("/get_page")
async def get_page():
    page_link = redis_client.get("chosen_page")
    return page_link

@app.get("/get_content")
async def get_content():
    content_link = redis_client.get("chosen_content")
    return content_link
