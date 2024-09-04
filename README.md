# BBC Burmese Telegram Web App
This project is still in the `developing` phase. The project aims to create a web app bot in Telegram. The bot crawls the **BBC Burmese** website to display news contents. This way, Telegram users can now read news without having to leave the app.

## Manual
You need the Telegram account to use this bot.
- Chat the [bot](http://t.me/presenter_sannie_bot) directly with your account.

OR
- You can also find my bot in the Telegram's search bar as follows.
```console
@presenter_sannie_bot
```
Once, the bot is started, it will automatically greet you with a direct link to the website.

I recommend using other methods to open the app without exiting the Telegram as this is the whole purpose. The bot supports
- inline button
- keyboard button
- inline mode

Once the app is launched, you can enter a single link to read news content. If you do not have a particular link, choose a topic to get more links, copy a link, and then insert it.

## Current Features
At the moment, there are two commands for my bot.
1. [/start]() - greet and return the main web app
2. [/help]() - describe how to use this bot
3. [/keyboard]() - return the keyboard button

## Scraper's Potential
The webscraper can
- scrape all topics (all pages of each topic) from BBC Burmese,
- scrape Burmese contents with a filter,
- export scraped data in spreadsheet,
- write spreadsheet data to Local DynamoDB,
- store current URL in redis cache for internet loss recovery.

## Future Improvements for Scraper
- To write spreadsheet data to cloud DynamoDB
- To use a modular approach than a single scraper script

***

# Building the Web App
## Files and Directories
There are several folders and files in this repository-
- The _notebooks_ folder contains the jupyter notebooks used to develop and document the progress.
- The _spreadsheets_ folder contains the exported spreadsheets. This directory is ignored onwards.
- The _db_ folder contains the DynamoDBLocal database and related files.
- The _webscraper_ folder contains the main Python script to perform the webscraping.
    - During development, I recommend you to check _notebooks_ instead. 
- The _pyproject.toml_ file contains the project dependencies and settings for a ruff check.
- The _doc_ folder contains files related to front-end and the UI design.
    - This folder is essential to host GitHub pages.
- The _img_ folder contains images to use in the project.
- The _telegram-bot_ folder contains scripts to manage and run the telegram bot.

## Project Development
Check all notebooks in the _notebooks_ folder for detailed documentations. You will learn how the customized web-crawler for this project is evolved from scratch.
This crawler is combined with the other two parts: the front-end and the Telegram bot. Necessary scripts can be found in specified folders as above.

## Project Requirements
To install DynamoDB locally, check [here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html).

- (Optional Config) If you download the compressed file, extract it and move to "C:".

To run DynamoDB locally, [JDK 17](https://www.oracle.com/java/technologies/downloads/#java17) is recommended.

- (Optional Config) Place it in the specific directory such that **java.exe** can be used as follows: 
```console
"C:\Program Files\Java\jdk-17\bin\java.exe"
```

To install Redis for client, check [here](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).
To install Ubuntu on Windows with WSL, check [here](https://learn.microsoft.com/en-us/windows/wsl/install).

You may also have to install additional libraries and modules. 
### A. Simple but Slow Installation
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
conda activate "C:\Users\<your-pc-username>\anaconda3\envs\<env-name>"
```
3. Install dependencies with
```console
pip install -r requirements.txt
```
### B. Fast but Complicated Installation
1. Install [uv](https://github.com/astral-sh/uv): an extremely fast Python package and project manager, written in Rust.
```console
pip install uv
```
2. Go to your working directory.
3. Create a virtual environment in your working directory with uv.
```console
uv venv
```
4. Activate the virtual environment.
```console
.venv\Scripts\activate
```
5. Install dependencies with
```console
uv pip install -r requirements
```
## Hosting Servers
- **Telegram**: You have to navigate to the directory `/telegram-bot` and host the Telegram bot with
```console
python app.py
```
- **Redis**: You need the Redis-client installed on your device. It caches the current link to continue fetching if the connection is lost. Open the Ubuntu Terminal and run
```console
redis-cli
```
- **DynamoDB**: You need to host the DynamoDB to store data. Navigate to the directory `/db` and run
```console
DynamoDB_init.bat
```
- **FastAPI**: Run the following to work with the website requests
```console
uvicorn api:app --reload
```
