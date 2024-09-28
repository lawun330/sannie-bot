// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    // Remove initial animation classes from the container
    const container = document.querySelector('.container');
    container.classList.remove('slide-left', 'slide-right', 'instant');
    
    // Get references to important DOM elements
    const backButton = document.getElementById('back-button');
    const pagesContainer = document.getElementById('pages-container');
    const linksContainer = document.getElementById('links-container');

    // Add click event listener to the back button to return to index page
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });

    // Add click event listener to the "Back to Pages" button
    const backToPagesButton = document.getElementById('back-to-pages');
    backToPagesButton.addEventListener('click', () => {
        // Show pages container, hide links container
        pagesContainer.style.display = 'block';
        linksContainer.style.display = 'none';
        backToPagesButton.style.display = 'none';
        // Update the title
        document.getElementById('title-content').textContent = 'Pages for ';
    });

    // Initialize the page when the DOM is loaded
    initializePage();
});

// Function to display pages
function displayPages(pages) {
    console.log('Received pages:', pages);
    const pagesContainer = document.getElementById('pages-container');
    pagesContainer.innerHTML = ''; // Clear previous content

    pages.forEach((page, index) => {
        // Create elements for each page
        const pageDiv = document.createElement('div');
        pageDiv.className = 'link-item';
        
        const pageText = document.createElement('span');
        pageText.textContent = page.title || `Page ${index + 1}`;
        
        const viewButton = document.createElement('button');
        viewButton.textContent = 'View Links';
        viewButton.className = 'copy-button';
        viewButton.addEventListener('click', async () => {
            try {
                console.log('Page object:', page);
                let pageUrl = page;

                // Handle different page URL formats
                if (typeof pageUrl === 'function') {
                    pageUrl = pageUrl();
                }

                if (typeof pageUrl === 'string' && !pageUrl.startsWith('http')) {
                    pageUrl = `https://www.bbc.com${pageUrl.startsWith('/') ? '' : '/'}${pageUrl}`;
                }

                console.log('Page URL:', pageUrl);

                // Only redirect after the API call is complete
                await sendDataToFastAPI('/set_chosen_page', { page: pageUrl });

                console.log('Redirecting to loading.html in 0 seconds...');
                setTimeout(() => {
                    window.location.href = 'loading.html?source=pages';
                }, 0);
            } catch (error) {
                console.error('Error setting chosen page:', error);
                showError(`Failed to set chosen page: ${error.message}`);
            }
        });
        
        // Append elements to the page container
        pageDiv.appendChild(pageText);
        pageDiv.appendChild(viewButton);
        pagesContainer.appendChild(pageDiv);
    });
}

// Function to display individual page links
function displayIndividualLinks(urls) {
    const linksContainer = document.getElementById('links-container');
    const pagesContainer = document.getElementById('pages-container');
    const backToPagesButton = document.getElementById('back-to-pages');
    linksContainer.innerHTML = ''; // Clear previous content
    
    // Show/hide containers and update title
    pagesContainer.style.display = 'none';
    linksContainer.style.display = 'block';
    backToPagesButton.style.display = 'block';
    document.getElementById('title-content').textContent = 'Links for ';

    urls.forEach((url, index) => {
        // Create elements for each link
        const linkDiv = document.createElement('div');
        linkDiv.className = 'link-item';
        
        const linkText = document.createElement('span');
        linkText.textContent = url;
        
        const copyButton = document.createElement('button');
        copyButton.textContent = 'Copy';
        copyButton.className = 'copy-button';
        copyButton.addEventListener('click', () => {
            copyToClipboard(url);
            updateButtonText(copyButton, 'Copied!');
        });
        
        // Append elements to the link container
        linkDiv.appendChild(linkText);
        linkDiv.appendChild(copyButton);
        linksContainer.appendChild(linkDiv);
    });
}

// Function to copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log('Text copied to clipboard');
    }).catch(err => {
        console.error('Error in copying text: ', err);
    });
}

// Function to update button text temporarily
function updateButtonText(button, text) {
    const originalText = button.textContent;
    button.textContent = text;
    button.disabled = true;
    setTimeout(() => {
        button.textContent = originalText;
        button.disabled = false;
    }, 2000);
}

// Function to fetch pages, contents, or article
function fetchItem(item) {
    fetch(`http://127.0.0.1:8000/${item}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json(); // Change this to parse JSON
        })
        .then(data => {
            if (item === 'pages') {
                displayPages(data); // Call displayPages with the fetched data
            }
        })
        .catch(error => {
            console.error('Error:', error.message);
            showError(`Failed to fetch ${item}: ${error.message}`);
        });
}

// Function to initialize the page
function initializePage() {
    fetchItem('pages');
}

// Function to send data to FastAPI
async function sendDataToFastAPI(endpoint, data) {
    try {
        const response = await fetch(`http://localhost:8000${endpoint}`, {
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
