CHOOSING TOPIC
==============
user chooses a topic using a dropdown menu and clicks "Get Links" button in index.html

index.js detects the change and sends a POST request to api.py with the chosen topic as the payload, in endpoint "/set_chosen_topic"
api.py receives the request and stores the chosen topic in Redis cache "chosen_topic"
developer can check the endpoint "/get_chosen_topic" in api.py to see the user's chosen topic
index.js redirects to loading.html

loading.js fetches the page links from the cache in api.py, in endpoint "/pages", in Redis cache "pages"
there is none in the cache
api.py uses the chosen topic to scrape the page links from the BBC Burmese website
loading.js fetches the page links from the cache in api.py, in endpoint "/pages", in Redis cache "pages"
loading.js fetches successfully
loading.js redirects to pages.html

pages.html fetches the page links from the cache in api.py, in endpoint "/pages", in Redis cache "pages"
pages.html displays the page links


CHOOSING PAGE
=============
user chooses a page link with a "Copy" button and a "Get Links" button

pages.js detects the change, sends a POST request to api.py with the chosen page as the payload, in endpoint "/set_chosen_page"
api.py receives the request and stores the chosen page in Redis cache "chosen_page"
developer can check the endpoint "/get_chosen_page" in api.py to see the user's chosen page
pages.js redirects to loading.html

loading.js fetches the content links from the cache in api.py, in endpoint "/content_links", in Redis cache "content_links"
there is none in the cache
api.py uses the chosen page to scrape the content links from the BBC Burmese website
loading.js fetches the content links from the cache in api.py, in endpoint "/content_links", in Redis cache "content_links"
loading.js fetches successfully
loading.js redirects to contents.html

contents.html fetches the content links from the cache in api.py, in endpoint "/content_links", in Redis cache "content_links"
contents.html displays the content links


CHOOSING CONTENT
================
user chooses a content link with a "Copy" button and a "Back to Main Page" button

contents.js redirects to index.html


VIEWING CONTENT
==============
user clicks "View Content" button in index.html

index.js detects the change, sends a GET request to api.py with the chosen content as the payload, in endpoint "/set_chosen_content"
api.py receives the request and stores the chosen content in Redis cache "chosen_content"
developer can check the endpoint "/get_chosen_content" in api.py to see the user's chosen content
index.js redirects to loading.html

loading.js fetches the content from the cache in api.py, in endpoint "/content", in Redis cache "content"
there is none in the cache
api.py uses the chosen content to scrape the content from the BBC Burmese website
loading.js fetches the content from the cache in api.py, in endpoint "/content", in Redis cache "content"
loading.js fetches successfully
loading.js redirects to article.html

article.html fetches the content from the cache in api.py, in endpoint "/content", in Redis cache "content"
article.html displays the content


SAVING CONTENT
==============
user clicks "Save as Text File" button in article.html
- output text file

user clicks "Copy" button in article.html
- copy to clipboard

user clicks "Back to Main Page" button in article.html
- redirect to index.html
