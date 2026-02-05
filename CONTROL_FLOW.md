Introduction
============
The structure of BBC Burmese is as follows:
```
main url
│
├── a topic
    ├── a page
        ├── a content/article
        ├── another content/article
        ├── ...
        ├── last content/article
    ├── another page
    ├── ...
    ├── last page
├── another topic
├── ...
├── last topic
```

The application uses a three-tier caching strategy:
1. **Redis** - Fast in-memory cache for frequently accessed data
2. **DynamoDB** - Permanent storage for all scraped data
3. **Web Scraping** - Fresh data retrieval when cache misses occur

Data flow for each endpoint follows this pattern:
- Check Redis cache first (fastest)
- If Redis miss, check DynamoDB (permanent storage)
- If DynamoDB miss, scrape from BBC Burmese website
- Save fresh data to both DynamoDB (permanent) and Redis (cache)

The application uses nine endpoints and six Redis cache keys:

- Endpoints `/set_chosen_topic`, `/get_chosen_topic` work with Redis cache "chosen_topic"
- Endpoints `/set_chosen_page`, `/get_chosen_page` work with Redis cache "chosen_page"
- Endpoints `/set_chosen_content`, `/get_chosen_content` work with Redis cache "chosen_content"
- Endpoint `/pages` works with Redis cache "pages" and DynamoDB table "sannie-pages"
- Endpoint `/contents` works with Redis cache "contents" and DynamoDB table "sannie-contents"
- Endpoint `/article` works with Redis cache "article" and DynamoDB table "sannie-articles"


Choosing Topic
==============
1. User chooses a topic using a dropdown menu and clicks "Get Links" button in **index.html**
2. **index.js** detects the change and sends a POST request to **api.py** with the chosen topic as payload
3. **api.py** stores the chosen topic in Redis cache "chosen_topic"
4. **index.js** redirects to **loading.html**
5. **loading.js** attempts to fetch page links from **api.py** endpoint `/pages`
6. **api.py** checks Redis cache "pages" first
7. If Redis miss, **api.py** checks DynamoDB table "sannie-pages"
8. If DynamoDB hit, data is returned and also saved to Redis cache
9. If DynamoDB miss, **api.py** scrapes page links from BBC Burmese website
10. Fresh scraped data is saved to both DynamoDB (permanent) and Redis (cache)
11. **loading.js** receives the page links and redirects to **pages.html**
12. **pages.html** displays the page links with direct "View" buttons


Choosing Page
=============
1. User clicks "View" button next to a page link in **pages.html**
2. **pages.js** sends a POST request to **api.py** with the chosen page URL
3. **api.py** stores the chosen page in Redis cache "chosen_page"
4. **pages.js** stores the pages list and current index in sessionStorage for navigation
5. **pages.js** redirects to **loading.html**
6. **loading.js** attempts to fetch content/article links from **api.py** endpoint `/contents`
7. **api.py** checks Redis cache "contents" first
8. If Redis miss, **api.py** checks DynamoDB table "sannie-contents"
9. If DynamoDB hit, data is returned and also saved to Redis cache
10. If DynamoDB miss, **api.py** scrapes content/article links from BBC Burmese website
11. Fresh scraped data is saved to both DynamoDB (permanent) and Redis (cache)
12. **loading.js** receives the content/article links and redirects to **contents.html**
13. **contents.html** displays the content/article links with direct "Read" buttons


Navigating Between Pages
=========================
1. User can navigate between pages using Previous (←) and Next (→) buttons in **contents.html**
2. Navigation buttons are displayed when multiple pages are available
3. **contents.js** loads pages list and current index from sessionStorage
4. Clicking Previous/Next updates the current index and fetches new content/article links
5. Page title updates dynamically to reflect the current page number
6. User can return to page selection by clicking "Back to Page Selection" button


Viewing Content/Article
========================
There are two ways to view content/article:

**Method 1: From Contents Page**
1. User clicks "Read" button next to a content/article link in **contents.html**
2. **contents.js** sends a POST request to **api.py** with the chosen content/article URL
3. **api.py** stores the chosen content/article in Redis cache "chosen_content"
4. **contents.js** redirects to **loading.html**
5. **loading.js** attempts to fetch content/article from **api.py** endpoint `/article`
6. **api.py** checks Redis cache "article" first
7. If Redis miss, **api.py** checks DynamoDB table "sannie-articles"
8. If DynamoDB hit, data is returned and also saved to Redis cache
9. If DynamoDB miss, **api.py** scrapes content/article from BBC Burmese website
10. Fresh scraped data is saved to both DynamoDB (permanent) and Redis (cache)
11. **loading.js** receives the content/article and redirects to **article.html**
12. **article.html** displays the content/article

**Method 2: Direct URL Input**
1. User selects "Insert Link" option in **index.html**
2. User enters a content/article URL in the input field
3. User clicks "Read the Link" button
4. **index.js** sends a POST request to **api.py** with the URL
5. **api.py** stores the URL in Redis cache "chosen_content"
6. **index.js** redirects to **loading.html**
7. Same flow as Method 1 (steps 5-12) follows


Saving Content/Article
======================
In **article.html**, user can:
1. Click "Save as Text File" button to download content/article as .txt file
2. Click "Copy" button to copy content/article to clipboard
3. Click "Back to Main Page" button to return to **index.html**