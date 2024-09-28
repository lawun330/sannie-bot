CHOOSING TOPIC
==============
user chooses a topic using a dropdown menu and clicks "Get Links" button in index.html

- **index.js** detects the change and sends a POST request to **api.py** with the chosen topic as the payload, in endpoint <code>"/set_chosen_topic"</code>
- **api.py** receives the request and stores the chosen topic in Redis cache <code>"chosen_topic"</code>
developer can check the endpoint <code>"/get_chosen_topic"</code> in **api.py** to see the user's chosen topic
- **index.js** redirects to **loading.html**

- **loading.js** fetches the page links from the cache in **api.py**, in endpoint <code>"/pages"</code>, in Redis cache <code>"pages"</code>
there is none in the cache
- **api.py** uses the chosen topic to scrape the page links from the BBC Burmese website
- **loading.js** fetches the page links from the cache in **api.py**, in endpoint <code>"/pages"</code>, in Redis cache <code>"pages"</code>
- **loading.js** fetches successfully
- **loading.js** redirects to **pages.html**

- **pages.html** fetches the page links from the cache in **api.py**, in endpoint <code>"/pages"</code>, in Redis cache <code>"pages"</code>
- **pages.html** displays the page links


CHOOSING PAGE
=============
user chooses a page link with a "Copy" button and a "Get Links" button

- **pages.js** detects the change, sends a POST request to **api.py** with the chosen page as the payload, in endpoint **"/set_chosen_page"**
- **api.py** receives the request and stores the chosen page in Redis cache <code>"chosen_page"</code>
developer can check the endpoint <code>"/get_chosen_page"</code> in **api.py** to see the user's chosen page
- **pages.js** redirects to **loading.html**

- **loading.js** fetches the content links from the cache in **api.py**, in endpoint <code>"/content_links"</code>, in Redis cache <code>"content_links"</code>
there is none in the cache
- **api.py** uses the chosen page to scrape the content links from the BBC Burmese website
- **loading.js** fetches the content links from the cache in **api.py**, in endpoint <code>"/content_links"</code>, in Redis cache <code>"content_links"</code>
- **loading.js** fetches successfully
- **loading.js** redirects to **contents.html**

- **contents.html** fetches the content links from the cache in **api.py**, in endpoint <code>"/content_links"</code>, in Redis cache <code>"content_links"</code>
- **contents.html** displays the content links


CHOOSING CONTENT
================
user chooses a content link with a "Copy" button and a "Back to Main Page" button
- **contents.js** redirects to **index.html**


VIEWING CONTENT
==============
user clicks "View Content" button in index.html

- **index.js** detects the change, sends a GET request to **api.py** with the chosen content as the payload, in endpoint <code>"/set_chosen_content"</code>
- **api.py** receives the request and stores the chosen content in Redis cache <code>"chosen_content"</code>
developer can check the endpoint <code>"/get_chosen_content"</code> in **api.py** to see the user's chosen content
- **index.js** redirects to **loading.html**

- **loading.js** fetches the content from the cache in **api.py**, in endpoint <code>"/content"</code>, in Redis cache <code>"content"</code>
there is none in the cache
- **api.py** uses the chosen content to scrape the content from the BBC Burmese website
- **loading.js** fetches the content from the cache in **api.py**, in endpoint <code>"/content"</code>, in Redis cache <code>"content"</code>
- **loading.js** fetches successfully
- **loading.js** redirects to **article.html**

- **article.html** fetches the content from the cache in **api.py**, in endpoint <code>"/content"</code>, in Redis cache <code>"content"</code>
- **article.html** displays the content


SAVING CONTENT
==============
user clicks "Save as Text File" button in **article.html**
- output text file

user clicks "Copy" button in **article.html**
- copy to clipboard

user clicks "Back to Main Page" button in **article.html**
- redirect to **index.html**
