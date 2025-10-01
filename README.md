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
- To use Docker for local development
- To make a compact repository

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
  - `requirements.txt` - Bot-specific dependencies
  - `Procfile` - Bot deployment configuration for Railway
- `/webscraper` - Main Python web scraping scripts and modules
  - `/modules` - Modular scraping scripts
- `api.py` - FastAPI server for web scraping endpoints
- `flow.md` - Control flow documentation
- `Procfile` - FastAPI deployment configuration for Railway
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
4. **Deployment Configuration** - Railway hosts FastAPI, Telegram bot, and Redis with required environment variables set
5. **Testing and Verification** - Test FastAPI endpoints via `<deployment-URL>/docs` or `<deployment-URL>/redoc` and verify Redis cache

***

## 5. 🖥️ Hosting

### 5.1. Local Servers

- **Local HTTP Server**: Test web app locally (port 9000 is arbitrary - any port can be used)
```console
python -m http.server 9000
```
- **Telegram Bot**: Run from `/telegram-bot` directory
```console
python app.py
```
- **Redis**: Cache for connection recovery
  1. Install Redis-client on the local device
  2. Open Ubuntu Terminal
  3. Run:
```console
redis-cli
```
- **DynamoDB**: Local database storage
```console
DynamoDB_init.bat
```
- **FastAPI**: Backend API server
```console
# Option 1: Direct Python script
python api.py

# Option 2: Using uvicorn command
uvicorn api:app --reload
```

### 5.2. Cloud Deployment (Railway)

1. **Create Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Connect GitHub Repository**: Link GitHub repo to Railway
3. **Deploy FastAPI**: Railway automatically detects and deploys the FastAPI app
4. **Add Redis Service**: Create a Redis database service in Railway
5. **Deploy Telegram Bot**: Create separate Railway service for the bot
6. **Set Environment Variables**:
   - `REDIS_URL` - Redis connection string from Railway
   - `BOT_TOKEN` - Telegram bot token
   - `BOT_USERNAME` - Bot username

NOTE: The Python scripts (`api.py` and `telegram-bot/app.py`) work seamlessly for both local and cloud deployment without requiring endpoint or API URL modifications.

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

### 6.1. Simple but Slow Installation

1. Create a virtual environment with Python
```console
python -m venv <env-name>
```
OR with conda.
```console
conda create --name <env-name>
```
2. Activate the virtual environment.
- For the virtual environment created with Python
```console
<env-name>\Scripts\activate
```
- For the virtual environment created with conda
```console
conda activate "C:\Users\<pc-username>\anaconda3\envs\<env-name>"
```
3. Install dependencies with
```console
pip install -r requirements.txt
```

### 6.2. Fast but Complicated Installation

1. Install [uv](https://github.com/astral-sh/uv): an extremely fast Python package and project manager, written in Rust.
```console
pip install uv
```
2. Navigate to the working directory.
3. Create a virtual environment in the working directory with uv.
```console
uv venv
```
4. Activate the virtual environment.
```console
.venv\Scripts\activate
```
5. Install dependencies with
```console
uv pip install -r requirements.txt
```

***

## License
This project is intended for educational purposes.
