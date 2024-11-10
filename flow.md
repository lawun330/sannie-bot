Introduction
============
The structure of BBC Burmese is as follows:
```
main url
│
├── a topic
    ├── a page
        ├── a content
            ├── an article (in-depth content)
        ├── another content
        ├── ...
        ├── last content
    ├── another page
    ├── ...
    ├── last page
├── another topic
├── ...
├── last topic
```

The application uses nine endpoints and six Redis caching directories:

- Endpoints `/set_chosen_topic`, `/get_chosen_topic` work with Redis cache "chosen_topic"
- Endpoints `/set_chosen_page`, `/get_chosen_page` work with Redis cache "chosen_page"
- Endpoints `/set_chosen_content`, `/get_chosen_content` work with Redis cache "chosen_content"
- Endpoint `/pages` works with Redis cache "pages"
- Endpoint `/contents` works with Redis cache "contents"
- Endpoint `/article` works with Redis cache "article"


Choosing Topic
==============
1. User chooses a topic using a dropdown menu and clicks "Get Links" button in **index.html**
2. **index.js** detects the change and sends a POST request to **api.py** with the chosen topic as payload
3. **api.py** stores the chosen topic in Redis cache "chosen_topic"
4. **index.js** redirects to **loading.html**
5. **loading.js** attempts to fetch page links from Redis cache "pages"
6. If cache is empty, **api.py** scrapes page links from BBC Burmese website and stores them in cache
7. **loading.js** fetches the cached page links and redirects to **pages.html**
8. **pages.html** displays the page links with copy and view options


Choosing Page
=============
1. User selects a page link in **pages.html** and clicks "View Content" button
2. **pages.js** sends a POST request to **api.py** with the chosen page
3. **api.py** stores the chosen page in Redis cache "chosen_page"
4. **pages.js** redirects to **loading.html**
5. **loading.js** attempts to fetch content links from Redis cache "contents"
6. If cache is empty, **api.py** scrapes content links from BBC Burmese website and stores them in cache
7. **loading.js** fetches the cached content links and redirects to **contents.html**
8. **contents.html** displays the content links with copy options


Choosing Content
================
1. User can return to the page selection interface by clicking "Back to Pages" button in **contents.html** if the page is chosen by mistake
2. User can copy the URL of a content link in **contents.html** if the page is correct
3. User returns to main page using "Back to Main Page" button

Viewing Content
===============
1. User clicks "Read the Link" button in **index.html**
2. **index.js** sends a GET request to **api.py** with the chosen content URL
3. **api.py** stores the chosen content in Redis cache "chosen_content"
4. **index.js** redirects to **loading.html**
5. **loading.js** attempts to fetch article from Redis cache "article"
6. If cache is empty, **api.py** scrapes article from BBC Burmese website and stores it in cache
7. **loading.js** fetches the cached article and redirects to **article.html**
8. **article.html** displays the article content


Saving Content
==============
In **article.html**, user can:
1. Click "Save as Text File" button to download content as .txt file
2. Click "Copy" button to copy content to clipboard
3. Click "Back to Main Page" button to return to **index.html**
