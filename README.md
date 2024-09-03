# Custom BBC Burmese Crawler

This project is still in the developing phase. The project aims to create a web app bot in Telegram. The bot crawls the BBC Burmese website to display news contents. This way, Telegram users can now read news without having to leave the app.

Initially, this branch is used to develop the custom crawler to scrape contents from-
1. BBC Burmese
2. Yangon Khit Thit Media

For the specific implementation, I chose the **BBC Burmese**.

## Files and Directories
There are several folders and files in this repository-
- The _notebooks_ folder contains the jupyter notebooks used to develop and document the progress.
- The _spreadsheets_ folder contains the exported spreadsheets. This directory is ignored onwards.
- The _db_ folder contains the DynamoDBLocal database and related files.
- The _webscraper_ folder contains the main Python script to perform the webscraping.
    - During development, I recommend you to check _notebooks_ instead. 
- The _pyproject.toml_ file contains the project dependencies and settings for a ruff check.

## Scraper's Potential
- scrape all topics (all pages of each topic) from BBC Burmese,
- scrape Burmese contents with a filter,
- export scraped data in spreadsheet,
- write spreadsheet data to Local DynamoDB,
- store current URL in redis cache for internet loss recovery.

## Future Improvements for Scraper
- To write spreadsheet data to cloud DynamoDB
- To use a modular approach than a single script

## Requirements
To run DynamoDB locally, [JDK 17](https://www.oracle.com/java/technologies/downloads/#java17) is recommended.

You may also have to install additional libraries and modules.
- numpy
- pandas
- beautifulsoup4
- boto3
- jupyter
- notebook
- redis
- html5lib
