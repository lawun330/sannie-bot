# Sannie Bot: BBC Burmese News on Telegram

This project is still in the `development` phase. It aims to create a Telegram web app bot called "Sannie." Sannie crawls the BBC Burmese website to display news content, allowing Telegram users to read the news without leaving the app.

## 1. 🚀 User Manual

A Telegram account is required.
- **Direct Link**: Chat the [bot](http://t.me/presenter_sannie_bot) directly
- **Search Method**: Find the bot in Telegram's search bar:
```console
@presenter_sannie_bot
```

### 1.1. Bot Features

- **Inline Button** - Interactive buttons within messages
- **Keyboard Button** - Custom keyboard for easy navigation  
- **Inline Mode** - Search and share content directly from any chat

### 1.2. Available Commands

1. `/start` - greet and return the main web app
2. `/help` - describe how to use this bot
3. `/keyboard` - return the keyboard button

### 1.3. Using the Web App

Once the bot is started, it will automatically greet with a direct link to the website.
The user can then:
- **Enter a single link** to read news content directly
- **Browse by topic**: Choose a topic, then a page, then copy a link of a content to read

***

## 2. 📊 Current Version

The webscraper can
- scrape all topics (all pages of each topic) from BBC Burmese,
- scrape Burmese contents with a filter,
- export scraped data in spreadsheet,
- write spreadsheet data to Local DynamoDB,
- store current URL in redis cache for internet loss recovery.

### 2.1. Future Improvements

- To write spreadsheet data to cloud DynamoDB
- To use a modular approach than a single scraper script
- To make the repository more compact

***

## 3. 📁 Files and Directories

- `/caching prototypes` - Development and testing files for caching system
- `/db` - DynamoDB Local database files and scripts
- `/docs` - Frontend files for GitHub Pages hosting (more info in `flow.md`)
- `/img` - Project images and assets
- `/notebooks` - Jupyter notebooks for webscraper development and documentation
- `/spreadsheets` - Exported data (ignored in version control)
- `/telegram-bot` - Telegram bot scripts (requires `.env` file for tokens)
  - `app.py` - Main bot application
  - `credentials.py` - Environment variable handler
  - `Dockerfile` - Bot container configuration
  - `Procfile` - Bot deployment configuration (Railway / Render)
  - `requirements.txt` - Bot-specific dependencies
- `/webscraper` - Main Python web scraping scripts and modules
  - `/modules` - Modular scraping scripts
- `api.py` - FastAPI server for web scraping endpoints
- `docker-compose.yml` - Orchestrates all Docker services (FastAPI, Redis, Telegram Bot)
- `Dockerfile` - FastAPI app container configuration
- `flow.md` - Control flow documentation
- `Procfile` - FastAPI app deployment configuration (Railway / Render)
- `pyproject.toml` - Project configuration and dependencies
- `requirements.txt` - All dependencies

***

## 4. 📈 Project Development

1. **Web Scraper Development** - Check all notebooks in the `/notebooks` folder for detailed documentation on how the customized web-crawler evolved from scratch
2. **Integration** - The web scraper is combined with two additional components:
   - Frontend (web-hosted with GitHub Pages)
   - Telegram bot (created to use the hosted frontend)
3. **Local Development Setup** - Uses local Redis with manual execution of Python scripts:
   - `api.py` - FastAPI server for web scraping endpoints
   - `telegram-bot/app.py` - Telegram bot application
4. **Deployment Configuration** - The same codebase deploys to Railway or Render; see sections 5.3 and 5.4
5. **Testing and Verification** - Test FastAPI endpoints via `<deployment-URL>/docs` or `<deployment-URL>/redoc` and verify Redis cache

***

## 5. 🖥️ Hosting

### 5.1. Local Server (No Docker)

1. **Start FastAPI Backend**
```console
# Option 1: Direct Python script
python api.py

# Option 2: CLI
uvicorn api:app --reload
```
- FastAPI will run on http://localhost:8000
- API documentation available at http://localhost:8000/docs
2. **Start Redis Cache**: Redis-client must be already installed on the local device
```console
# Open Ubuntu terminal and run:
redis-cli
```
3. **Start Local Frontend Server**
```console
# Navigate to "/docs"
cd docs
# Start HTTP server (port 9000 is arbitrary - any port can be used)
python -m http.server 9000
```
4. **Test Web App**: Test web app locally at http://localhost:9000 by choosing topic → page → content → article
5. **Start/Test Telegram Bot**
```console
# Navigate to "/telegram-bot"
cd telegram-bot
# Start Telegram bot
python app.py
```
6. **Start DynamoDB (Optional)**
```console
DynamoDB_init.bat
```

### 5.2. Local Server (Docker)

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
3. **Test All Services**: Test web app locally at http://localhost:9000 by choosing topic → page → content → article

### 5.3. Cloud Deployment (Railway)

1. **Create Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Connect GitHub Repository**: Link GitHub repo to Railway
3. **Deploy FastAPI**: Railway automatically detects and deploys the FastAPI app
4. **Add Redis Service**: Create a Redis database service in Railway
5. **Deploy Telegram Bot**: Create separate Railway service for the bot
6. **Set Environment Variables**:
   - `REDIS_URL` - Redis connection string from Railway
   - `BOT_TOKEN` - Telegram bot token
   - `BOT_USERNAME` - Bot username

### 5.4. Cloud Deployment (Render)

1. **Create Render Account**: Sign up at [render.com](https://render.com)
2. **Connect GitHub Repository**: Link GitHub repo to Render
3. **Deploy FastAPI**: Create a web service; use Docker and the root `Dockerfile`
4. **Add Redis**: Use [Upstash](https://upstash.com) or another provider; set `REDIS_URL` on the web service
5. **Deploy Telegram Bot**: Create a background worker; use Docker and `telegram-bot/Dockerfile` (build context: repo root)
6. **Set Environment Variables**:
   - `REDIS_URL` - on the web service (e.g. from Upstash)
   - `BOT_TOKEN` - Telegram bot token
   - `BOT_USERNAME` - Bot username

NOTE: The same codebase works on both Railway and Render. Set the production API URL in `docs/functions.js` to match the deployment URL (see 6.4).

***

## 6. 🔧 Setup and Installation

To install DynamoDB locally, check [here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html).

- (Optional Config) If the compressed file is downloaded, extract it and move to "C:".

To run DynamoDB locally, [JDK 17](https://www.oracle.com/java/technologies/downloads/#java17) is recommended.

- (Optional Config) Place it in the specific directory such that **java.exe** can be used as follows: 
```console
"C:\Program Files\Java\jdk-17\bin\java.exe"
```

To install Redis for client, check [here](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).
To install Ubuntu on Windows with WSL, check [here](https://learn.microsoft.com/en-us/windows/wsl/install).

Additional libraries and modules may also need to be installed.

### 6.1. Simple Setup

1. Create a virtual environment
```console
# Option 1: Python
python -m venv <env-name>
# Option 2: Conda
conda create --name <env-name>
```
2. Activate the virtual environment
```console
# Option 1: Python virtual environment
<env-name>\Scripts\activate
# Option 2: Conda virtual environment
conda activate "C:\Users\<pc-username>\anaconda3\envs\<env-name>"
```
3. Install [uv](https://github.com/astral-sh/uv)
```console
pip install uv
```
4. Navigate to the working directory
5. Install dependencies
```console
uv pip install -r requirements.txt
```

### 6.2. Docker Setup

1. Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install dependencies
```console
docker-compose up --build
```

### 6.3. Environment Configuration

1. Get bot credentials from [@BotFather](https://t.me/botfather) on Telegram
2. Create a `.env` file in the root with bot credentials
```console
BOT_TOKEN=actual_bot_token_here
BOT_USERNAME=bot_username_here
```

### 6.4. Production API URL (Railway or Render)

The frontend in `docs/` is served from GitHub Pages and calls the deployed API. In `docs/functions.js`, set the placeholder `DEPLOYED_API_URL` to the actual API base URL:

- **Railway**: Railway web service URL (e.g. `https://app.up.railway.app`)
- **Render**: Render Web Service URL (e.g. `https://app.onrender.com`)

Commit and push so the GitHub Pages site uses the correct API. The same repo works on either platform; only this URL needs to match the deployed API.

***

## License
This project is intended for educational purposes.
