# Custom-Webscraper

This project is currently under development.

This repository contains necessary files to webscrape contents from-
1. BBC Burmese
2. Yangon Khit Thit Media

For demonstration, I have chosen the BBC Burmese website.

The goal is to webscrape and store them in a DynamoDB database for further processing.
To run DynamoDB locally, [JDK 17](https://www.oracle.com/java/technologies/downloads/#java17) is recommended.

There are several folders and files in this repository-
- The _notebooks_ folder contains the jupyter notebooks used to develop and document the progress.
- The _spreadsheets_ folder contains the exported spreadsheets.
- The _db_ folder contains the DynamoDBLocal database and related files.
- The _webscraper_ folder contains the main Python script to perform the webscraping.
    - During development, I recommend you to check _notebooks_ instead because the main script is not always updated. 
- The _pyproject.toml_ file contains the project dependencies and settings for a ruff check.

*Note that you may have to install libraries and modules.*
