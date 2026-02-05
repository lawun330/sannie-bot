# Development Guide

This guide explains how to set up and run the application locally for development.

## Prerequisites

Ensure the required software is installed:
- Python 3.11+
- Redis (for caching)
- DynamoDB Local (optional, for local database testing)
- Docker Desktop (optional, for containerized development)

See `requirements.txt` for Python dependencies.

***

## Method A: Without Docker
### Step 1: Clone and Setup

Clone the repository:
```console
git clone <repository-url>
cd sannie-bot
```

### Step 2: Create Virtual Environment

Create a virtual environment:
```console
# Option 1: Python
python -m venv <env-name>

# Option 2: Conda
conda create --name <env-name>
```

Activate the virtual environment:
```console
# Option 1: Python virtual environment
<env-name>\Scripts\activate

# Option 2: Conda virtual environment
conda activate "C:\Users\<pc-username>\anaconda3\envs\<env-name>"
```

### Step 3: Install Dependencies

Install [uv](https://github.com/astral-sh/uv) (recommended):
```console
pip install uv
```

Navigate to the working directory and install dependencies:
```console
uv pip install -r requirements.txt
```

For telegram bot dependencies:
```console
cd telegram-bot
uv pip install -r requirements.txt
cd ..
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:
```console
BOT_TOKEN=actual_bot_token_here
BOT_USERNAME=bot_username_here
REDIS_URL=redis://localhost:6379/0
```

Get bot credentials from [@BotFather](https://t.me/botfather) on Telegram.

Optional: For DynamoDB integration, add AWS credentials:
```console
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-southeast-1
DYNAMODB_TABLE_PAGES=sannie-pages
DYNAMODB_TABLE_CONTENTS=sannie-contents
DYNAMODB_TABLE_ARTICLES=sannie-articles
```

Note: The application works without DynamoDB, but data won't be permanently stored. Redis is required for caching.

### Step 5: Start Local Redis Cache

Redis-client must be already installed on the local device.

**Windows (WSL):**
```console
# Open Ubuntu terminal and run:
redis-cli
```

**Linux/Mac:**
```console
redis-server
```

To install Redis, check [here](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).

### Step 6: Start Local DynamoDB (Optional)

To install DynamoDB locally, check [here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html).

If the compressed file is downloaded, extract it and move to "C:".

To run DynamoDB locally, [JDK 17](https://www.oracle.com/java/technologies/downloads/#java17) is recommended.

Place it in the specific directory such that **java.exe** can be used as follows:
```console
"C:\Program Files\Java\jdk-17\bin\java.exe"
```

Start DynamoDB:
```console
DynamoDB_init.bat
```

### Step 7: Run Backend (FastAPI)

**Option A: Direct Python script**
```console
python api.py
```

**Option B: Using uvicorn (Recommended)**
```console
uvicorn api:app --reload
```

The backend starts on http://localhost:8000
- API documentation available at http://localhost:8000/docs

### Step 8: Run Local Frontend Server

```console
# Navigate to "/docs"
cd docs

# Start HTTP server (port 9000 is arbitrary - any port can be used)
python -m http.server 9000
```

The frontend starts on http://localhost:9000

### Step 9: Run Telegram Bot (Optional)

```console
# Navigate to "/telegram-bot"
cd telegram-bot

# Start Telegram bot
python app.py
```

### Step 10: Access the Application

1. Open a browser and go to http://localhost:9000
2. The React app calls the FastAPI backend at http://localhost:8000
3. Test the flow: Choose topic → page → contents → content/article
4. If DynamoDB is configured, check AWS console for stored data
5. Check Redis cache for frequently accessed data

***

## Method B: With Docker (Alternative)

For containerized development:

1. **Start All Services**: Use Docker Compose to start FastAPI, Redis, and Telegram Bot
    ```console
    docker-compose up --build
    ```
- FastAPI will run on http://localhost:8000
- API documentation available at http://localhost:8000/docs

2. **Start Local Frontend Server**
    ```console
    # Navigate to "/docs"
    cd docs
    # Start HTTP server (port 9000 is arbitrary - any port can be used)
    python -m http.server 9000
    ```

3. **Test All Services**: Test web app locally at http://localhost:9000 by choosing topic → page → contents → content/article

***

## Development Workflow

1. Make code changes
2. Backend: Restart `uvicorn api:app --reload` to see changes (or use `--reload` flag for auto-reload)
3. Frontend: Refresh browser to see changes
4. Test locally before pushing to deployment

***

## Local Development URLs

- Frontend: http://localhost:9000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Pages Endpoint: http://localhost:8000/pages
- Contents Endpoint: http://localhost:8000/contents
- Article Endpoint: http://localhost:8000/article

***

## Notes

- The `.env` file is gitignored - never commit it with real credentials
- Backend and frontend must be running simultaneously for full functionality
- Redis is required for the application to work properly
- DynamoDB is optional but recommended for permanent data storage
- The application implements three-tier caching: Redis (fast) -> DynamoDB (permanent) -> Web scraping