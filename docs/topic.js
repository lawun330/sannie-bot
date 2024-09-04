// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    // Get URL parameters and DOM elements
    const urlParams = new URLSearchParams(window.location.search);
    const topicUrl = urlParams.get('url');
    const backButton = document.getElementById('back-button');
    const pagesContainer = document.getElementById('pages-container');
    const linksContainer = document.getElementById('links-container');

    // Object containing Burmese titles and their corresponding URLs
    const topicTitles = {
        'https://www.bbc.com/burmese': 'ပင်မစာမျက်နှာ',
        'https://www.bbc.com/burmese/topics/c404v027pd4t': 'မြန်မာ့ရေးရာ',
        'https://www.bbc.com/burmese/topics/c9wpm0en9jdt': 'နိုင်ငံတကာ',
        'https://www.bbc.com/burmese/topics/cg726y2k82dt': 'ဆောင်းပါး',
        'https://www.bbc.com/burmese/topics/c404v44epsdt': 'အင်တာဗျူး',
        'https://www.bbc.com/burmese/topics/cyz8kl2e1rqt': 'ကုန်သွယ်စီးပွား',
        'https://www.bbc.com/burmese/topics/c404v44epsdt': 'ဗီဒီယိုများ'
    };

    // Get the Burmese title for the current topic URL
    const topicTitle = topicTitles[topicUrl] || 'Unknown Topic';
    document.getElementById('topic-title').textContent = topicTitle;

    // Fetch and display pages for the selected topic
    fetchTopicPages(topicUrl).then(pages => {
        displayPages(pages);
    });

    // Add click event listener to the back button
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });

    // Add click event listener to the "Back to Pages" button
    const backToPagesButton = document.getElementById('back-to-pages');
    backToPagesButton.addEventListener('click', () => {
        document.getElementById('pages-container').style.display = 'block';
        document.getElementById('links-container').style.display = 'none';
        backToPagesButton.style.display = 'none';
        document.getElementById('title-content').textContent = 'Pages for ';
    });
});

// Function to display pages
function displayPages(pages) {
    const pagesContainer = document.getElementById('pages-container');
    pagesContainer.innerHTML = ''; // Clear previous content

    pages.forEach((page, index) => {
        // Create elements for each page
        const pageDiv = document.createElement('div');
        pageDiv.className = 'link-item';
        
        const pageText = document.createElement('span');
        pageText.textContent = `Page ${index + 1}`;
        
        const viewButton = document.createElement('button');
        viewButton.textContent = 'View Links';
        viewButton.className = 'copy-button';
        viewButton.addEventListener('click', () => {
            // Fetch and display links for the selected page
            fetchPageLinks(page).then(links => {
                displayIndividualLinks(links, index + 1);
            });
        });
        
        // Append elements to the page container
        pageDiv.appendChild(pageText);
        pageDiv.appendChild(viewButton);
        pagesContainer.appendChild(pageDiv);
    });
}

// Function to display individual links
function displayIndividualLinks(urls, pageNumber) {
    const linksContainer = document.getElementById('links-container');
    const pagesContainer = document.getElementById('pages-container');
    const backToPagesButton = document.getElementById('back-to-pages');
    linksContainer.innerHTML = ''; // Clear previous content
    
    // Show/hide containers and update title
    pagesContainer.style.display = 'none';
    linksContainer.style.display = 'block';
    backToPagesButton.style.display = 'block';
    document.getElementById('title-content').textContent = `Links for Page ${pageNumber} of `;

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

// Function to fetch topic pages (dummy implementation)
async function fetchTopicPages(topicUrl) {
    // Implement the logic to fetch pages for the selected topic URL
    // This could involve making an API call to your backend or using pre-fetched data
    // For now, we'll return a dummy array
    return ['https://example.com/page1', 'https://example.com/page2', 'https://example.com/page3'];
}

// Function to fetch page links (dummy implementation)
async function fetchPageLinks(pageUrl) {
    // Implement the logic to fetch links for the selected page URL
    // This could involve making an API call to your backend or using pre-fetched data
    // For now, we'll return a dummy array
    return ['https://example.com/link1', 'https://example.com/link2', 'https://example.com/link3'];
}