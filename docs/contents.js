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
    if (pagesContainer && contentsContainer) {
        pagesContainer.style.display = 'none';
        contentsContainer.style.display = 'block';
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
}


// Function to set up page navigation (Previous/Next buttons)
function setupPageNavigation() {
    // Get or create navigation container
    let navContainer = document.getElementById('page-navigation');
    if (!navContainer) {
        navContainer = document.createElement('div');
        navContainer.id = 'page-navigation';
        navContainer.className = 'input-group w-full';
        navContainer.style.marginTop = '1rem';
        
        // Insert after contents container
        const container = document.querySelector('.container');
        const inputGroup = container.querySelector('.input-group');
        container.insertBefore(navContainer, inputGroup);
    } else {
        // Clear existing buttons
        navContainer.innerHTML = '';
    }
    
    const buttonRow = document.createElement('div');
    buttonRow.className = 'button-row';
    buttonRow.style.display = 'flex';
    buttonRow.style.gap = '0.5rem';
    buttonRow.style.justifyContent = 'center';
    
    // Previous button
    const prevButton = document.createElement('button');
    prevButton.textContent = '← Previous';
    prevButton.className = 'button';
    prevButton.style.flex = '1';
    prevButton.style.maxWidth = '150px';
    prevButton.disabled = currentPageIndex <= 0;
    prevButton.addEventListener('click', () => navigateToPage(currentPageIndex - 1));
    
    // Back to Page Selection button
    const backToPagesBtn = document.createElement('button');
    backToPagesBtn.textContent = 'Back to Pages';
    backToPagesBtn.className = 'button';
    backToPagesBtn.style.flex = '1';
    backToPagesBtn.style.maxWidth = '150px';
    backToPagesBtn.addEventListener('click', () => {
        window.location.href = 'pages.html';
    });
    
    // Next button
    const nextButton = document.createElement('button');
    nextButton.textContent = 'Next →';
    nextButton.className = 'button';
    nextButton.style.flex = '1';
    nextButton.style.maxWidth = '150px';
    nextButton.disabled = currentPageIndex >= pagesList.length - 1;
    nextButton.addEventListener('click', () => navigateToPage(currentPageIndex + 1));
    
    buttonRow.appendChild(prevButton);
    buttonRow.appendChild(backToPagesBtn);
    buttonRow.appendChild(nextButton);
    navContainer.appendChild(buttonRow);
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
        
        // Reload contents
        const data = await fetchItem('contents');
        displayContents(data);
        
        // Update navigation buttons
        setupPageNavigation();
    } catch (error) {
        showError(`Failed to navigate to page: ${error.message}`);
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
        
        // Setup navigation buttons if pages list exists
        if (pagesList.length > 0 && currentPageIndex >= 0) {
            setupPageNavigation();
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


// Function to create a content element with its copy button and view button
function createContentElement(content) {
    const contentDiv = document.createElement('div');
    contentDiv.className = 'link-item';
    
    const scrollContainer = document.createElement('div');
    scrollContainer.className = 'scroll-container';
    
    const contentLink = createContentLink(content);
    const copyButton = createCopyButton(content.url);
    const viewButton = createViewButton(content.url);
    
    scrollContainer.appendChild(contentLink);
    contentDiv.appendChild(scrollContainer);
    contentDiv.appendChild(copyButton);
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


// Function to create the view article button for a content link
function createViewButton(contentUrl) {
    const viewButton = document.createElement('button');
    viewButton.textContent = 'View Article';
    viewButton.className = 'viewlinks-button';
    
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
