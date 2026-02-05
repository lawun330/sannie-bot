/**
 * This file handles the content selection interface of the BBC Burmese News application.
 * It manages the display and interaction with individual content links from a selected page.
 * 
 * Connected files:
 * - contents.html: Contains the DOM elements this script interacts with
 * - functions.js: Provides utility functions like showError(), copyToClipboard(), and updateButtonText()
 * - loading.html: Destination page after content selection
 * - api.py: FastAPI backend that provides content data
 */

// Global variable declarations
let contentsContainer;
let pagesContainer;
let backButton;
let prevPageButton;
let nextPageButton;
let backToPagesButton;
let pageNavigation;
let pagesList = [];
let currentPageIndex = -1;

// Main event listener for DOM load
document.addEventListener('DOMContentLoaded', async () => {
    // Remove initial animation classes from the container
    const container = document.querySelector('.container');
    container.classList.remove('slide-left', 'slide-right', 'instant');
    
    // Get references to important DOM elements
    pagesContainer = document.getElementById('pages-container');
    contentsContainer = document.getElementById('contents-container');
    backButton = document.getElementById('back-button');
    prevPageButton = document.getElementById('prev-page-button');
    nextPageButton = document.getElementById('next-page-button');
    backToPagesButton = document.getElementById('back-to-pages-button');
    pageNavigation = document.getElementById('page-navigation');

    // Configure container visibility
    showContentsContainer();

    // Attach event handlers to navigation buttons
    attachNavigationButtonHandlers();

    // Initialize the page
    initializePage();
});


// Function to show contents container and hide pages container
function showContentsContainer() {
    if (pagesContainer && contentsContainer) {
        pagesContainer.style.display = 'none';
        contentsContainer.style.display = 'block';
    } else {
        showError('Page elements not found. Please refresh the page.');
    }
}


// Function to create and initialize the page title element
function createPageTitle() {
    const urlParams = new URLSearchParams(window.location.search);
    let pageTitle = urlParams.get('pageTitle') || 'မသိရသေးသောစာမျက်နှာ';
    
    // If pages list and current index exist, use that for title
    if (pagesList.length > 0 && currentPageIndex >= 0) {
        pageTitle = `စာမျက်နှာ ${currentPageIndex + 1}`;
    }
    
    const titleElement = document.getElementById('title-content');
    titleElement.textContent = 'သတင်းခေါင်းစဉ်များ - ';
    
    const pageTitleSpan = document.createElement('span');
    pageTitleSpan.id = 'page-title';
    pageTitleSpan.textContent = pageTitle;
    titleElement.appendChild(pageTitleSpan);
}


// Function to attach event handlers to navigation buttons
function attachNavigationButtonHandlers() {
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
    
    if (prevPageButton) {
        prevPageButton.addEventListener('click', () => navigateToPage(currentPageIndex - 1));
    }
    
    if (nextPageButton) {
        nextPageButton.addEventListener('click', () => navigateToPage(currentPageIndex + 1));
    }
    
    if (backToPagesButton) {
        backToPagesButton.addEventListener('click', () => {
            window.location.href = 'pages.html';
        });
    }
}


// Function to update page navigation visibility and button states
function updatePageNavigationState() {
    if (!pageNavigation || pagesList.length === 0 || currentPageIndex < 0) {
        if (pageNavigation) {
            pageNavigation.style.display = 'none';
        }
        return;
    }
    
    // Show navigation
    pageNavigation.style.display = 'block';
    
    // Update button disabled states
    if (prevPageButton) {
        prevPageButton.disabled = currentPageIndex <= 0;
    }
    if (nextPageButton) {
        nextPageButton.disabled = currentPageIndex >= pagesList.length - 1;
    }
}


// Function to navigate to a different page
async function navigateToPage(newIndex) {
    if (newIndex < 0 || newIndex >= pagesList.length) {
        return;
    }
    
    try {
        const page = pagesList[newIndex];
        const pageUrl = formatPageUrl(page);
        
        await sendDataToFastAPI('/set_chosen_page', { page: pageUrl });
        
        // Update stored index
        currentPageIndex = newIndex;
        sessionStorage.setItem('currentPageIndex', newIndex.toString());
        
        // Update page title
        updatePageTitle(`စာမျက်နှာ ${newIndex + 1}`);
        
        // Reload contents
        const data = await fetchItem('contents');
        displayContents(data);
        
        // Update navigation button states
        updatePageNavigationState();
    } catch (error) {
        showError(`Failed to navigate to page: ${error.message}`);
    }
}


// Function to update page title
function updatePageTitle(pageTitleText) {
    const pageTitleSpan = document.getElementById('page-title');
    if (pageTitleSpan) {
        pageTitleSpan.textContent = pageTitleText;
    }
}


// Function to format page URL (same as in pages.js)
function formatPageUrl(pageUrl) {
    if (typeof pageUrl === 'function') {
        pageUrl = pageUrl();
    }
    
    if (typeof pageUrl === 'string' && !pageUrl.startsWith('http')) {
        pageUrl = `https://www.bbc.com${pageUrl.startsWith('/') ? '' : '/'}${pageUrl}`;
    }
    
    return pageUrl;
}


// Function to initialize the page
async function initializePage() {
    try {
        // Load pages list and current index from sessionStorage for navigation
        const storedPagesList = sessionStorage.getItem('pagesList');
        const storedPageIndex = sessionStorage.getItem('currentPageIndex');
        
        if (storedPagesList) {
            pagesList = JSON.parse(storedPagesList);
        }
        if (storedPageIndex !== null) {
            currentPageIndex = parseInt(storedPageIndex, 10);
        }
        
        // Create page title (after loading pages list and index)
        createPageTitle();
        
        // Update navigation state if pages list exists
        if (pagesList.length > 0 && currentPageIndex >= 0) {
            updatePageNavigationState();
        }
        
        const data = await fetchItem('contents');
        displayContents(data);
    } catch (error) {
        showError('Failed to load contents. Please try again.');
    }
}


// Function to display content links
function displayContents(contents) {
    console.group('Contents');
    console.log('Contents to choose from:', contents);
    contentsContainer.innerHTML = ''; // Clear previous content

    contents.forEach((content) => {
        const contentElement = createContentElement(content);
        contentsContainer.appendChild(contentElement);
    });
    console.groupEnd();
}


// Function to create a content element with its read button
function createContentElement(content) {
    const contentDiv = document.createElement('div');
    contentDiv.className = 'link-item';
    
    const scrollContainer = document.createElement('div');
    scrollContainer.className = 'scroll-container';
    
    const contentLink = createContentLink(content);
    const viewButton = createViewButton(content.url);
    
    scrollContainer.appendChild(contentLink);
    contentDiv.appendChild(scrollContainer);
    contentDiv.appendChild(viewButton);
    
    return contentDiv;
}


// Function to create the content link element
function createContentLink(content) {
    const contentText = document.createElement('a');
    contentText.href = content.url;
    contentText.textContent = content.header;
    contentText.title = content.url;
    contentText.target = '_blank';
    return contentText;
}


// Function to create the view article button for a content link
function createViewButton(contentUrl) {
    const viewButton = document.createElement('button');
    viewButton.textContent = 'ဖတ်မည်';
    viewButton.className = 'button compact-read-button';
    
    viewButton.addEventListener('click', async () => {
        try {
            await sendDataToFastAPI('/set_chosen_content', { content: contentUrl });
            window.location.href = 'loading.html?source=contents';
        } catch (error) {
            showError(`Failed to set chosen content: ${error.message}`);
        }
    });
    
    return viewButton;
}
