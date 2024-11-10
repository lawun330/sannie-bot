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
let backToPagesButton;

// Main event listener for DOM load
document.addEventListener('DOMContentLoaded', async () => {
    // Remove initial animation classes from the container
    const container = document.querySelector('.container');
    container.classList.remove('slide-left', 'slide-right', 'instant');
    
    // Get references to important DOM elements
    pagesContainer = document.getElementById('pages-container');
    contentsContainer = document.getElementById('contents-container');
    backButton = document.getElementById('back-button');
    backToPagesButton = document.getElementById('back-to-pages');

    // Configure container visibility
    setContainerVisibility();

    // Set up page title
    setupPageTitle();

    // Set up navigation buttons
    setupNavigationButtons();

    // Initialize the page
    initializePage();
});


// Function to set container visibility
function setContainerVisibility() {
    if (pagesContainer && contentsContainer && backToPagesButton) {
        pagesContainer.style.display = 'none';
        contentsContainer.style.display = 'block';
        backToPagesButton.style.display = 'block';
    } else {
        showError('Page elements not found. Please refresh the page.');
    }
}


// Function to set up the page title
function setupPageTitle() {
    const urlParams = new URLSearchParams(window.location.search);
    const pageTitle = urlParams.get('pageTitle') || 'Unknown Page';
    
    const titleElement = document.getElementById('title-content');
    titleElement.textContent = 'Contents for ';
    
    const pageTitleSpan = document.createElement('span');
    pageTitleSpan.id = 'page-title';
    pageTitleSpan.textContent = pageTitle;
    titleElement.appendChild(pageTitleSpan);
}


// Function to set up navigation buttons
function setupNavigationButtons() {
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });

    backToPagesButton.addEventListener('click', () => {
        window.location.href = 'pages.html';
    });
}


// Function to initialize the page
async function initializePage() {
    try {
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


// Function to create a content element with its copy button
function createContentElement(content) {
    const contentDiv = document.createElement('div');
    contentDiv.className = 'link-item';
    
    const scrollContainer = document.createElement('div');
    scrollContainer.className = 'scroll-container';
    
    const contentLink = createContentLink(content);
    const copyButton = createCopyButton(content.url);
    
    scrollContainer.appendChild(contentLink);
    contentDiv.appendChild(scrollContainer);
    contentDiv.appendChild(copyButton);
    
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


// Function to create the copy button for a content link
function createCopyButton(content) {
    const copyButton = document.createElement('button');
    copyButton.textContent = 'Copy';
    copyButton.className = 'copy-button';
    
    copyButton.addEventListener('click', () => {
        copyToClipboard(content);
        updateButtonText(copyButton, 'Copied!');
    });
    
    return copyButton;
}
