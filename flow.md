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

Therefore, I use nine endpoints and six Redis caching directories.

- Endpoints <code>"/set_chosen_topic"</code>, <code>"/get_chosen_topic"</code> work with Redis cache <code>"chosen_topic"</code>
- Endpoints <code>"/set_chosen_page"</code>, <code>"/get_chosen_page"</code> work with Redis cache <code>"chosen_page"</code>
- Endpoints <code>"/set_chosen_content"</code>, <code>"/get_chosen_content"</code> work with Redis cache <code>"chosen_content"</code>
- Endpoints <code>"/pages"</code> work with Redis cache <code>"pages"</code>
- Endpoints <code>"/contents"</code> work with Redis cache <code>"contents"</code>
- Endpoints <code>"/article"</code> work with Redis cache <code>"article"</code>


Choosing Topic
==============
User chooses a topic using a dropdown menu and clicks "Get Links" button in **index.html**.

- **index.js** detects the change and sends a POST request to **api.py** with the chosen topic as the payload, in endpoint <code>"/set_chosen_topic"</code>
- **api.py** receives the request and stores the chosen topic in Redis cache <code>"chosen_topic"</code>

Developer can check the endpoint <code>"/get_chosen_topic"</code> in the browser to see the user's chosen topic.

- **index.js** redirects to **loading.html**

- **loading.js** fetches the page links from Redis cache <code>"pages"</code> with endpoint <code>"/pages"</code>.

There is none in the cache.

- **api.py** uses the chosen topic to scrape the page links from the BBC Burmese website
- **api.py** stores the page links in Redis cache <code>"pages"</code>

- **loading.js** fetches the page links from the cache in **api.py**, in endpoint <code>"/pages"</code> 
- **loading.js** fetches data successfully
- **loading.js** redirects to **pages.html**

- **pages.html** fetches the page links from the cache in **api.py**, in endpoint <code>"/pages"</code>
- **pages.html** displays the page links


Choosing Page
=============
User chooses a page link with a "Copy" button and a "Get Links" button in **pages.html**.

- **pages.js** detects the change, sends a POST request to **api.py** with the chosen page as the payload, in endpoint <code>"/set_chosen_page"</code>
- **api.py** receives the request and stores the chosen page in Redis cache <code>"chosen_page"</code>

Developer can check the endpoint <code>"/get_chosen_page"</code> in the browser to see the user's chosen page.

- **pages.js** redirects to **loading.html**

- **loading.js** fetches the content links from Redis cache <code>"contents"</code> in endpoint <code>"/contents"</code>

There is none in the cache.

- **api.py** uses the chosen page to scrape the content links from the BBC Burmese website
- **api.py** stores the content links in Redis cache <code>"contents"</code>

- **loading.js** fetches the content links from the cache in **api.py**, in endpoint <code>"/contents"</code>
- **loading.js** fetches successfully
- **loading.js** redirects to **contents.html**

- **contents.html** fetches the content links from the cache in **api.py**, in endpoint <code>"/contents"</code>
- **contents.html** displays the content links


Choosing Content
================
User chooses a content link with a "Copy" button and a "Back to Main Page" button in **contents.html**.
- **contents.js** redirects to **index.html**


Viewing Content
===============
User clicks "View Content" button in **index.html**.

- **index.js** detects the change, sends a GET request to **api.py** with the chosen article/content as the payload, in endpoint <code>"/set_chosen_content"</code>
- **api.py** receives the request and stores the chosen article/content in Redis cache <code>"chosen_content"</code>

Developer can check the endpoint <code>"/get_chosen_content"</code> in the browser to see the user's chosen article/content.

- **index.js** redirects to **loading.html**

- **loading.js** fetches the article/content from Redis cache <code>"article"</code> in endpoint <code>"/article"</code>

There is none in the cache.

- **api.py** uses the chosen article/content to scrape the article from the BBC Burmese website
- **api.py** stores the article/content in Redis cache <code>"article"</code>

- **loading.js** fetches the article/content from the cache in **api.py**, in endpoint <code>"/article"</code>
- **loading.js** fetches successfully
- **loading.js** redirects to **article.html**

- **article.html** fetches the article/content from the cache in **api.py**, in endpoint <code>"/article"</code>
- **article.html** displays the article/content


Saving Content
==============
user clicks "Save as Text File" button in **article.html**
- output text file

user clicks "Copy" button in **article.html**
- copy to clipboard

user clicks "Back to Main Page" button in **article.html**
- redirect to **index.html**
