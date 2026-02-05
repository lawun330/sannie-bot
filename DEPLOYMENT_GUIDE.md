# Deployment Guide

This guide explains how to deploy the Sannie Bot application:

- **Backend (FastAPI)**: Railway or Render (using Docker)
- **Telegram Bot**: Railway only (Render has no free tier for background workers)
- **Frontend**: GitHub Pages
- **Redis**: Upstash (for Render) or Railway Redis service
- **DynamoDB**: AWS DynamoDB (cloud)

## Architecture Overview

```text
┌─────────────┐      HTTP/HTTPS       ┌───────────────┐
│ GitHub Pages│ ───────────────────>  │ Railway/Render│
│  (Frontend) │                       │  (FastAPI)    │
│   HTML/JS   │ <───────────────────  │   Backend     │
└─────────────┘      JSON Response    └───────────────┘
     │                                         │
     │                                         │
     v                                         │
  User Browser                                 │
                                               │
                                               ├─────────────────┐
                                               │                 │
                                               │                 │
                                               v                 v
                                    ┌──────────────────┐  ┌──────────────┐
                                    │  AWS DynamoDB    │  │   Upstash/   │
                                    │  (Permanent      │  │   Railway    │
                                    │   Storage)       │  │   Redis      │
                                    └──────────────────┘  └──────────────┘
```

Flow:
1. User visits GitHub Pages frontend URL
2. Frontend calls Railway/Render backend via API_BASE_URL
3. Backend checks Redis cache first (fastest)
4. If Redis miss, backend checks DynamoDB (permanent storage)
5. If DynamoDB hit, data is returned and also saved to Redis cache
6. If DynamoDB miss, backend scrapes from BBC Burmese website
7. Fresh scraped data is saved to both DynamoDB (permanent) and Redis (cache)
8. Backend returns data to frontend
9. Frontend displays the content/article

## Step 1: AWS DynamoDB Setup

### 1.1 Create AWS Account and DynamoDB Tables

- Go to https://aws.amazon.com and sign up/login
- Navigate to DynamoDB service
- Create three tables with on-demand capacity:
  - `sannie-pages` (Primary key: `topic_url` - String)
  - `sannie-contents` (Primary key: `page_url` - String)
  - `sannie-articles` (Primary key: `content_url` - String)

### 1.2 Create IAM User and Access Keys

- Go to IAM service → Users → Create user
- Attach policy: `AmazonDynamoDBFullAccess` (or create custom policy)
- Create access key → Save Access Key ID and Secret Access Key securely
- Note the AWS region where tables are created (e.g., `ap-southeast-1`)

### 1.3 Configure Network Access

- DynamoDB is accessible via AWS SDK with proper credentials
- No additional network configuration needed (unlike MongoDB)

Note: DynamoDB is optional - the application works without it, but data won't be permanently stored. Redis is required.

## Step 2: Setup Redis

Choose one of the following Redis providers:

### 2.A: Railway Redis

#### 2.A.1 Create Railway Account

- Go to https://railway.app and sign up/login

#### 2.A.2 Create New Project

- Click "New Project" → "Deploy from GitHub repo"
- Select the repository

#### 2.A.3 Add Redis Service

- Click "New" → "Database" → "Add Redis"
- Railway creates a Redis instance automatically
- Copy the Redis URL from the service settings (e.g., `redis://default:password@redis.railway.internal:6379`)

Note: Save this Redis URL - it will be needed when deploying FastAPI (Step 3).

### 2.B: Upstash Redis

#### 2.B.1 Create Upstash Account

- Go to https://upstash.com and sign up/login

#### 2.B.2 Create Redis Database

- Click "Create Database"
- Choose the same region as the Render service (if using Render) or closest region
- Copy the Redis URL (e.g., `redis://default:password@region.upstash.io:6379`)

Note: Save this Redis URL - it will be needed when deploying FastAPI (Step 3).

## Step 3: Deploy FastAPI Backend

Choose one of the following platforms to deploy the FastAPI backend:

### 3.A: Railway

#### 3.A.1 Connect GitHub Repository (if not already done)

- In Railway project, click "New" → "Deploy from GitHub repo"
- Select the repository

#### 3.A.2 Deploy FastAPI Web Service

- Railway automatically detects and deploys the FastAPI app
- Or manually create a new service → Select "Deploy from GitHub repo"
- Railway uses the root `Dockerfile` automatically

#### 3.A.3 Set Environment Variables

Go to FastAPI service settings → Environment Variables and add:

```console
REDIS_URL=redis://default:password@redis.railway.internal:6379
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-southeast-1
DYNAMODB_TABLE_PAGES=sannie-pages
DYNAMODB_TABLE_CONTENTS=sannie-contents
DYNAMODB_TABLE_ARTICLES=sannie-articles
```

#### 3.A.4 Get Deployment URL

- Copy the Railway web service URL (e.g., `https://app.up.railway.app`)
- This URL is needed for frontend configuration (Step 4)

### 3.B: Render

#### 3.B.1 Create Render Account

- Go to https://render.com and sign up/login

#### 3.B.2 Connect GitHub Repository

- Click "New +" → "Web Service"
- Connect the GitHub repository
- Select the repository

#### 3.B.3 Deploy FastAPI Web Service

- Name: `sannie-bot-backend-fastapi` (or preferred name)
- Environment: Docker
- Region: Choose closest region (should match Upstash Redis region)
- Branch: `main` (or the deployment branch)
- Root Directory: Leave empty (default root)
- Dockerfile Path: `Dockerfile` (root Dockerfile)
- Click "Create Web Service"

#### 3.B.4 Set Environment Variables

Go to FastAPI service settings → Environment Variables and add:

```console
REDIS_URL=redis://default:password@region.upstash.io:6379
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-southeast-1
DYNAMODB_TABLE_PAGES=sannie-pages
DYNAMODB_TABLE_CONTENTS=sannie-contents
DYNAMODB_TABLE_ARTICLES=sannie-articles
```

#### 3.B.5 Get Deployment URL

- Copy the Render web service URL (e.g., `https://app.onrender.com`)
- This URL is needed for frontend configuration (Step 4)

## Step 4: Deploy Frontend to GitHub Pages

### 4.1 Push Code to GitHub

- Ensure all changes are committed and pushed to the repository

### 4.2 Configure Frontend API URL

The frontend in `docs/` needs to know which backend API to call. In `docs/functions.js`, update the `API_BASE_URL`:

**For Railway:**
```javascript
return 'https://app.up.railway.app';  // Replace with actual Railway URL from Step 3.A.4
```

**For Render:**
```javascript
return 'https://app.onrender.com';  // Replace with actual Render URL from Step 3.B.5
```

Commit and push the change:
```console
git add docs/functions.js
git commit -m "Update API URL for production"
git push
```

### 4.3 Enable GitHub Pages

- Go to repository Settings → Pages
- Source: Deploy from a branch
- Branch: `main` (or the docs branch)
- Folder: `/docs`
- Click "Save"

### 4.4 Get GitHub Pages URL

- Frontend will be available at: `https://<username>.github.io/<repository-name>/`
- Or custom domain if configured
- GitHub Pages will automatically rebuild with the new API URL after pushing changes

## Step 5: Deploy Telegram Bot

The Telegram bot must be deployed on Railway only, as Render does not offer free tier for background workers.

### 5.1 Create Background Worker on Railway

- In the Railway project, click "New" → "Background Worker"
- Set Root Directory to empty (`.`)
- Under Build settings, choose **Dockerfile** instead of Railpack for the builder
- Set Dockerfile Path to `telegram-bot/Dockerfile`
- Railway builds and deploys the bot

### 5.2 Set Environment Variables

Go to Telegram Bot service settings → Environment Variables and add:

```console
BOT_TOKEN=your_telegram_bot_token
BOT_USERNAME=your_bot_username
```

Get bot credentials from [@BotFather](https://t.me/botfather) on Telegram.

***

## Environment Variables Summary

**FastAPI Web Service (Railway/Render):**
- `REDIS_URL` - Redis connection string (from Step 2)
- `AWS_ACCESS_KEY` - AWS access key ID (from Step 1.2)
- `AWS_SECRET_ACCESS_KEY` - AWS secret access key (from Step 1.2)
- `AWS_REGION` - AWS region (e.g., `ap-southeast-1`)
- `DYNAMODB_TABLE_PAGES` - DynamoDB table name for pages
- `DYNAMODB_TABLE_CONTENTS` - DynamoDB table name for contents
- `DYNAMODB_TABLE_ARTICLES` - DynamoDB table name for articles
- `PORT` - Automatically set by Railway/Render

**Telegram Bot Service (Railway only):**
- `BOT_TOKEN` - Telegram bot token from @BotFather
- `BOT_USERNAME` - Telegram bot username

**Frontend (GitHub Pages):**
- No environment variables needed
- API URL is hardcoded in `docs/functions.js` (configured in Step 4.2)

## How Environment Variables Work

**Backend (Python):**
- Checks system environment variables first (`os.getenv()`)
- Falls back to `.env` file if system env vars not found (local development only)
- Required variables must be set in production (Railway/Render)

**Frontend (JavaScript):**
- API URL is set in `docs/functions.js`
- Detects localhost automatically for development
- Uses production URL when deployed to GitHub Pages

***

## Updating Deployment

1. Make changes to code
2. Push changes to GitHub
3. Railway/Render automatically detects changes, rebuilds, and redeploys
4. GitHub Pages automatically rebuilds on push (if enabled)

***

## Verification

1. **Test FastAPI Endpoints**: Visit `<deployment-URL>/docs` or `<deployment-URL>/redoc`
2. **Test Frontend**: Visit GitHub Pages URL and test the full flow
3. **Test Telegram Bot**: Send `/start` command to the bot
4. **Verify Redis Cache**: Check Redis dashboard (Upstash/Railway) for cached data
5. **Verify DynamoDB**: Check AWS DynamoDB console for stored items

***

## Notes

- The same codebase works on both Railway and Render for FastAPI
- Only the API URL in `docs/functions.js` needs to match the deployed backend
- DynamoDB tables must be created in the same AWS region
- Redis connection string format may vary between providers
- Telegram bot must be deployed on Railway (Render has no free tier for background workers)
- Background workers on Render free tier have limitations (may spin down after inactivity)