/**
 * This file contains the main event listener for the index page.
 * It handles the radio button selection, topic selection, and URL input.
 * It also includes helper functions for toggling UI elements and handling errors.
 * 
 * Connected files:
 * - index.html: Contains the DOM elements this script interacts with
 * - functions.js: Provides utility functions like showError() and sendDataToFastAPI()
 * - loading.html: Destination page after form submission
 * - api.py: FastAPI backend that receives the form data
 */

// Global variable declarations
let singleUrlInput;
let singleUrlContainer;
let topicSelect;
let getLinksContainer;
let getLinksButton;
let readLinkButton;

// Main event listener for DOM load
document.addEventListener('DOMContentLoaded', () => {
    console.group('Topics'); // Start console group
    
    // Get references to important DOM elements
    singleUrlContainer = document.getElementById('single-url-container');
    singleUrlInput = document.getElementById('single-url-input');
    topicSelect = document.getElementById('topic-select');
    const actionButton = document.getElementById('action-button');

    // Log available topics
    const topicDropdown = document.getElementById('topic-dropdown');
    if (topicDropdown) {
        const topics = Array.from(topicDropdown.options).map(option => ({
            name: option.value,
            url: option.getAttribute('data-url')
        }));
        console.log('Topics to choose from:', topics);
    }

    // Radio button event handlers for UI toggling
    document.querySelectorAll('input[name="option"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            handleRadioChange(e.target.value);
        });
    });

    // Set initial button state (Topic is selected by default)
    updateActionButton('topic');

    // Event handler for action button (toggles between Get Links and Read the Link)
    if (actionButton) {
        actionButton.addEventListener('click', () => {
            const selectedOption = document.querySelector('input[name="option"]:checked').value;
            if (selectedOption === 'topic') {
                handleGetLinks();
            } else {
                handleReadLink();
            }
        });
    }

    // Back button navigation handler
    if (document.getElementById('back-button')) {
        document.getElementById('back-button').addEventListener('click', handleBackNavigation);
    }

    console.groupEnd(); // End console group
});


// Helper function to handle radio button changes
function handleRadioChange(value) {
    // Toggle UI elements based on the selected radio button
    if (value === 'insert-link') {
        toggleElements(true, singleUrlContainer);
        toggleElements(false, topicSelect);
    } else if (value === 'topic') {
        toggleElements(false, singleUrlContainer);
        toggleElements(true, topicSelect);
    }
    // Update action button text and functionality
    updateActionButton(value);
}

// Function to update action button text based on selected option
function updateActionButton(selectedValue) {
    const actionButton = document.getElementById('action-button');
    if (actionButton) {
        if (selectedValue === 'topic') {
            actionButton.textContent = 'ရွေးမည်';
        } else {
            actionButton.textContent = 'ဖတ်မည်';
        }
    }
}


// Helper function to toggle element visibility
function toggleElements(show, ...elements) {
    elements.forEach(element => {
        if (element) element.style.display = show ? 'block' : 'none'; // block shows, none hides
    });
}


// Handler for getting links from selected topic
async function handleGetLinks() {    
    // Check if a topic is selected
    const topicSelect = document.getElementById('topic-dropdown');
    if (!topicSelect || !topicSelect.value) {
        showError('Please select a topic');
        return;
    }

    // Get the selected topic and its URL
    const selectedTopic = topicSelect.value;
    const selectedOption = topicSelect.options[topicSelect.selectedIndex];
    const topicUrl = selectedOption.getAttribute('data-url');
    console.log("The chosen topic is: ", topicUrl);

    // Check if the URL is valid
    if (!topicUrl) {
        showError('Invalid topic URL');
        return;
    }
    
    try {
        // Use sendDataToFastAPI instead of direct fetch
        await sendDataToFastAPI('/set_chosen_topic', { topic: topicUrl });
        
        // Navigate to loading page with topic title
        window.location.href = `loading.html?source=index&topicTitle=${encodeURIComponent(selectedTopic)}`;
    } catch (error) {
        showError(`Failed to set topic: ${error.message}`);
    }
}


// Handler for reading content from a single URL
async function handleReadLink() {
    // Get the URL from the input field
    const url = singleUrlInput.value;
    if (!url) {
        showError('Please enter a URL');
        return;
    }
    
    try {
        // Use sendDataToFastAPI instead of direct fetch
        await sendDataToFastAPI('/set_chosen_content', { content: url });
        
        // Navigate to loading page for article
        window.location.href = `loading.html?source=contents`;
    } catch (error) {
        showError(`Failed to fetch content: ${error.message}`);
    }
}


// Handler for back button navigation
function handleBackNavigation() {
    // Add slide-right animation class
    const container = document.querySelector('.container');
    container.classList.add('slide-right');
    
    // Navigate back to main page after animation
    setTimeout(() => {
        window.location.href = '/';
    }, 300); // Match this with the CSS transition duration
}