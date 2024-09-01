# Customized-BBC-Crawler

This project is in the `developing` phase.

Initially, this repository contains necessary files to webscrape contents from-
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


## Current Features
- Scrape all topics (all pages of each topic) from BBC Burmese
- Scrape Burmese contents with a filter
- Export scraped data in spreadsheet
- Write spreadsheet data to Local DynamoDB
- Store current URL in redis cache for internet loss recovery  


## Work Under Development
- To write spreadsheet data to cloud DynamoDB
- To use a modular approach than a single script


## Requirements
To run DynamoDB locally, [JDK 17](https://www.oracle.com/java/technologies/downloads/#java17) is recommended.

You may also have to install libraries and modules such as-
- BeautifulSoup
- pandas
- redis
- requests
