'''This script loads environment variables and system variables.'''

import os
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv() # load the environment file

# load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

if not BOT_TOKEN or not BOT_USERNAME:
    raise ValueError("Environment variables are not set.")