/**
 * This file handles the article display interface of the BBC Burmese News application.
 * It manages the display of article content and provides copy/save functionality.
 * 
 * Connected files:
 * - article.html: Contains the DOM elements this script interacts with
 * - functions.js: Provides utility functions like showError(), copyToClipboard(), and fetchItem()
 * - loading.html: Source page that redirects here
 * - api.py: FastAPI backend that provides article data
 */

// Global variable declarations
let contentContainer;
let saveButton;
let backButton;
let copyButton;
let container;

// Main event listener for DOM load
document.addEventListener('DOMContentLoaded', async () => {
    // Remove initial animation classes from the container
    container = document.querySelector('.container');
    container.classList.remove('slide-left', 'slide-right', 'instant');
    
    // Get references to important DOM elements
    contentContainer = document.getElementById('content-container');
    saveButton = document.getElementById('save-button');
    backButton = document.getElementById('back-button');
    copyButton = document.getElementById('article-copy-button');
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize the page
    initializePage();
});


// Function to set up event listeners
function setupEventListeners() {
    // Copy button handler
    copyButton.addEventListener('click', handleCopyContent);

    // Save button handler
    saveButton.addEventListener('click', handleSaveContent);

    // Back button handler
    backButton.addEventListener('click', handleBackNavigation);
}


// Function to handle copy button click
function handleCopyContent() {
    const content = contentContainer.textContent;
    copyToClipboard(content);
    updateButtonText(copyButton, 'Copied!');
}


// Function to handle save button click
function handleSaveContent() {
    const content = contentContainer.textContent;
    downloadTextFile(content, 'bbc_burmese_content.txt');
}


// Function to handle back button click
function handleBackNavigation() {
    window.location.href = 'index.html';
}


// Function to download text as file
function downloadTextFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}


// Function to fetch article content
async function fetchContent() {
    try {
        const data = await fetchItem('article');
        return data;
    } catch (error) {
        showError('Failed to fetch content. Please try again later.');
    }
}


// Function to initialize the page content
async function initializePage() {
    try {
        const content = await fetchContent();
        displayContent(content);
    } catch (error) {
        showError('Error loading content. Please try again.');
    }
}


// Function to display content
function displayContent(content) {
    if (content) {
        contentContainer.textContent = content;
    } else {
        contentContainer.textContent = 'No content available.';
    }
}