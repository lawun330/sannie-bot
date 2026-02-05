/**
 * This file handles the page selection interface of the BBC Burmese News application.
 * It manages the display and interaction with individual page links from a selected topic.
 * 
 * Connected files:
 * - pages.html: Contains the DOM elements this script interacts with
 * - functions.js: Provides utility functions like showError(), sendDataToFastAPI()
 * - loading.html: Destination page after page selection
 * - api.py: FastAPI backend that receives the selected page data
 */

// Global variable declarations
let pagesContainer;

document.addEventListener('DOMContentLoaded', async () => {
    // Remove initial animation classes from the container
    const container = document.querySelector('.container');
    container.classList.remove('slide-left', 'slide-right', 'instant');
    
    // Get references to important DOM elements
    pagesContainer = document.getElementById('pages-container');
    const contentsContainer = document.getElementById('contents-container');
    const backButton = document.getElementById('back-button');
    const backToPagesButton = document.getElementById('back-to-pages');

    // Show/hide containers
    pagesContainer.style.display = 'block';
    contentsContainer.style.display = 'none';
    backToPagesButton.style.display = 'none';

    // Get topic title from URL parameters and update page title
    const urlParams = new URLSearchParams(window.location.search);
    const topicTitle = urlParams.get('topicTitle') || 'မသိရသေးသောအမျိုးအစား';
    updatePageTitle(topicTitle);

    // Add click event listener to the back button to return to index page
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });

    // Initialize the page
    initializePage();
});


// Function to update the page title with topic information
function updatePageTitle(topicTitle) {
    const titleElement = document.getElementById('title-content');
    titleElement.textContent = 'စာမျက်နှာများ - ';
    
    const topicTitleSpan = document.createElement('span');
    topicTitleSpan.id = 'topic-title';
    topicTitleSpan.textContent = topicTitle;
    titleElement.appendChild(topicTitleSpan);
}


// Function to initialize the page
async function initializePage() {
    try {
        const data = await fetchItem('pages');
        displayPages(data);
    } catch (error) {
        showError('Failed to load pages. Please try again.');
    }
}


// Function to display pages
function displayPages(pages) {
    console.group('Pages');
    console.log('Pages to choose from:', pages);    
    pagesContainer.innerHTML = ''; // Clear previous content

    pages.forEach((page, index) => {
        const pageElement = createPageElement(page, index);
        pagesContainer.appendChild(pageElement);
    });
}


// Function to create a page element with its view button
function createPageElement(page, index) {
    const pageDiv = document.createElement('div');
    pageDiv.className = 'link-item';
    
    const pageText = document.createElement('span');
    pageText.textContent = `စာမျက်နှာ ${index + 1}`;
    
    const viewButton = createViewButton(page, `စာမျက်နှာ ${index + 1}`, index);
    
    pageDiv.appendChild(pageText);
    pageDiv.appendChild(viewButton);
    
    return pageDiv;
}


// Function to create and configure the view button for a page
function createViewButton(page, pageTitle, pageIndex) {
    const viewButton = document.createElement('button');
    viewButton.textContent = 'ဝင်ကြည့်မည်';
    viewButton.className = 'button page-view-button';
    
    viewButton.addEventListener('click', async () => {
        await handleViewButtonClick(page, pageTitle, pageIndex);
    });
    
    return viewButton;
}


// Function to handle view button click events
async function handleViewButtonClick(page, pageTitle, pageIndex) {
    try {
        const pageUrl = formatPageUrl(page);
        console.log('Selected Page URL:', pageUrl);

        await sendDataToFastAPI('/set_chosen_page', { page: pageUrl });
        
        // Store pages list and current index for navigation
        const pagesData = await fetchItem('pages');
        sessionStorage.setItem('pagesList', JSON.stringify(pagesData));
        sessionStorage.setItem('currentPageIndex', pageIndex.toString());
        
        console.log('Redirecting to loading.html...');
        redirectToLoading(pageTitle);
        console.groupEnd();
    } catch (error) {
        showError(`Failed to set chosen page: ${error.message}`);
    }
}


// Function to format the page URL
function formatPageUrl(pageUrl) {
    if (typeof pageUrl === 'function') {
        pageUrl = pageUrl();
    }

    if (typeof pageUrl === 'string' && !pageUrl.startsWith('http')) {
        pageUrl = `https://www.bbc.com${pageUrl.startsWith('/') ? '' : '/'}${pageUrl}`;
    }

    return pageUrl;
}


// Function to redirect to the loading page
function redirectToLoading(pageTitle) {
    setTimeout(() => {
        window.location.href = `loading.html?source=pages&pageTitle=${encodeURIComponent(pageTitle)}`;
    }, 0);
}