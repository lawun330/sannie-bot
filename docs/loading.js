/**
 * This file handles the loading interface of the BBC Burmese News application.
 * It manages the loading state and transitions between different content types.
 * 
 * Connected files:
 * - loading.html: Contains the DOM elements this script interacts with
 * - functions.js: Provides utility functions like showError()
 * - article.html: Destination page after successful content fetch
 * - api.py: FastAPI backend that provides content data
*/

// Global variable declarations
let loadingIndicator;
let errorMessage;
let backButton;
let statusText;

// API Configuration
// use the one from functions.js

// Main event listener for DOM load
document.addEventListener('DOMContentLoaded', () => {
    // Get references to important DOM elements
    loadingIndicator = document.getElementById('loading-indicator');
    errorMessage = document.getElementById('error-message');
    backButton = document.getElementById('back-button');
    statusText = document.getElementById('status');

    // Set up event listeners
    backButton.addEventListener('click', handleBackNavigation);
    
    // Initialize the page
    initializePage();
});


// Function to initialize the page
function initializePage() {
    // Get the item to fetch from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const source = urlParams.get('source') || 'index';

    // Determine the endpoint based on the source
    const endpoint = determineEndpoint(source);
    
    if (!endpoint) {
        showError('Invalid source parameter');
        return;
    }

    // Call the function to fetch the appropriate item
    fetchItem(endpoint);
}


// Function to determine the endpoint based on source
function determineEndpoint(source) {
    const endpoints = {
        'index': 'pages',
        'pages': 'contents',
        'contents': 'article'
    };
    
    return endpoints[source];
}


// Function to handle back button navigation
function handleBackNavigation() {
    window.location.href = 'index.html';
}


// Function to show error - different from the global function in functions.js
function showError(message) {
    if (loadingIndicator && errorMessage && statusText) {
        loadingIndicator.classList.add('hidden');
        statusText.classList.add('hidden');
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    } else {
        console.error('Error: DOM elements not found');
    }
}


// Function to update loading status
function updateStatus(message) {
    if (statusText) {
        statusText.textContent = message;
    } else {
        console.error('Error: Status element not found');
    }
}


// Function to fetch pages, contents, or article - different from the global function in functions.js
function fetchItem(endpoint) {
    fetch(`${API_BASE_URL}/${endpoint}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Data is available now!");
            // Store the fetched data and redirect
            localStorage.setItem('fetchedData', JSON.stringify(data));
            
            // Get URL parameters
            const urlParams = new URLSearchParams(window.location.search);
            
            // Redirect based on the endpoint
            if (endpoint === 'pages') {
                const topicTitle = urlParams.get('topicTitle');
                window.location.href = `pages.html${topicTitle ? `?topicTitle=${encodeURIComponent(topicTitle)}` : ''}`;
            } else if (endpoint === 'contents') {
                const pageTitle = urlParams.get('pageTitle');
                window.location.href = `contents.html${pageTitle ? `?pageTitle=${encodeURIComponent(pageTitle)}` : ''}`;
            } else if (endpoint === 'article') {
                window.location.href = 'article.html';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError(`Failed to fetch ${endpoint}: ${error.message}`);
        });
}