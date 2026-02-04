/**
 * This file contains common utility functions used across the BBC Burmese web scraping application.
 * Core functionalities include:
 * - Error handling and display
 * - Clipboard operations
 * - UI element manipulation
 * - FastAPI backend communication
 * - Data fetching and event handling
 * - Template loading
 * 
 * The functions handle both user interface interactions and server communication,
 * supporting the application's web scraping capabilities while maintaining state
 * through Redis caching and providing feedback through the UI.
 */

// API Configuration (same codebase works with Railway or Render)
const API_BASE_URL = (() => {
    // If running on localhost (development), use local API
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'http://localhost:8000';
    }
    // If running on GitHub Pages (production), set this to the deployed API URL (Railway or Render)
    // e.g. https://app.onrender.com or https://app.up.railway.app
    return 'https://sannie-bot-backend-fastapi.onrender.com';  // ########## UPDATE HERE ##########
})();


// Function to show error - globally accessible
// Used in loading.js and throughout error handling
function showError(message) {
    console.error(message);
}


// Function to copy text to clipboard - globally accessible
// Used in contents.js and article.js
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        console.log('Text copied to clipboard');
    } catch (err) {
        console.error('Error in copying text: ', err);
        showError('Failed to copy text to clipboard');
    }
}


// Function to update button text temporarily - globally accessible
// Used in contents.js and article.js
function updateButtonText(button, text) {
    const originalText = button.textContent;
    button.textContent = text;
    button.disabled = true;
    setTimeout(() => {
        button.textContent = originalText;
        button.disabled = false;
    }, 2000);
}


// Function to send data to FastAPI - globally accessible
// Used in index.js and pages.js
async function sendDataToFastAPI(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}


// Function to fetch pages, contents, or article - globally accessible
// Used in pages.js, contents.js, and loading.js
async function fetchItem(item) {
    try {
        const response = await fetch(`${API_BASE_URL}/${item}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json(); // To parse JSON
        
        // Dispatch event for components that rely on events
        const event = new CustomEvent('dataFetched', { 
            detail: { type: item, data: data } 
        });
        document.dispatchEvent(event);
        
        // Return the data for direct Promise handling
        return data;
    } catch (error) {
        console.error('Error:', error.message);
        showError(`Failed to fetch ${item}: ${error.message}`);
        throw error;
    }
}


// Function to load template - globally accessible
// Used in pages.js and contents.js
async function loadTemplate(containerId) {
    try {
        const response = await fetch('templates/container.html');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Get the template HTML
        const template = await response.text();

        // Parse the template HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(template, 'text/html');

        // Replace the entire body content
        document.body.innerHTML = doc.body.innerHTML;
    } catch (error) {
        console.error('Error loading template:', error);
        showError('Failed to load template');
    }
}