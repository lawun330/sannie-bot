# Sannie Bot: BBC Burmese News on Telegram

This project is a Telegram web app bot called "Sannie." Sannie crawls the BBC Burmese website to display news content, allowing Telegram users to read the news without leaving the app. The entire user interface is displayed in Burmese language, providing a native experience for Burmese-speaking users.

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
- **Browse by topic**: Choose a topic, then a page, then click "Read" button to view content/article (Topic mode)
- **Enter a single link** to read content/article directly (Insert Link mode)
- Navigate between pages using Previous/Next buttons without returning to page selection

**Note**: All UI elements, buttons, and navigation are displayed in Burmese language for better accessibility.

***

## 2. 📊 Current Version

The webscraper can
- scrape all topics (all pages of each topic) from BBC Burmese,
- scrape Burmese content/article with a filter,
- export scraped data in spreadsheet,
- store scraped data in DynamoDB (permanent storage),
- cache frequently accessed data in Redis (fast cache),

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
- `DEVELOPMENT_GUIDE.md` - Local development setup guide
- `DEPLOYMENT_GUIDE.md` - Production deployment guide
- `Procfile` - FastAPI app deployment configuration (Railway / Render)
- `pyproject.toml` - Project configuration and dependencies
- `requirements.txt` - All dependencies

***

## 4. 📈 Project Development

1. **Web Scraper Development** - Check all notebooks in the `/notebooks` folder for detailed documentation on how the customized web-crawler evolved from scratch
2. **Integration** - The web scraper is combined with multiple components:
   - Frontend (web-hosted with GitHub Pages) with improved navigation and direct view buttons
   - Telegram bot (created to use the hosted frontend)
   - Redis cache (fast in-memory storage for frequently accessed data)
   - DynamoDB (permanent storage for all scraped data)
   - Three-tier caching strategy: Redis -> DynamoDB -> Web scraping

***

## 5. 📚 Documentation

- `flow.md` - Control flow documentation and user journey
- `DEVELOPMENT_GUIDE.md` - Local development setup and commands
- `DEPLOYMENT_GUIDE.md` - Production deployment instructions (Railway/Render)

***

## License
This project is intended for educational purposes.