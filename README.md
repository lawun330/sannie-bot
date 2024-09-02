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
Once, the bot is started, it will automatically greet you with a direct link to open the web app. 

You can also use other methods to open the app. The bot supports
- inline button
- bot menu button
- keyboard button
- inline mode

## Current Features
At the moment, there are two commands for my bot.
1. [/start]() - return the main web app
2. [/help]() - provide descriptions to use the bot

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
To run DynamoDB locally, [JDK 17](https://www.oracle.com/java/technologies/downloads/#java17) is recommended.

You may also have to install additional libraries and modules with
```console
pip install -r requirements.txt
```
