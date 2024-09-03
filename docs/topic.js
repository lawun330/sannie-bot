document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const topic = urlParams.get('topic');
    const topicTitle = document.getElementById('topic-title');
    const backButton = document.getElementById('back-button');
    const linksContainer = document.getElementById('links-container');

    // Set the topic title
    topicTitle.textContent = topic;

    // Fetch the URLs for the selected topic
    fetchTopicUrls(topic).then(urls => {
        displayIndividualLinks(urls);
    });

    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
});

function displayIndividualLinks(urls) {
    const linksContainer = document.getElementById('links-container');
    linksContainer.innerHTML = ''; // Clear previous content

    urls.forEach((url, index) => {
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
        
        linkDiv.appendChild(linkText);
        linkDiv.appendChild(copyButton);
        linksContainer.appendChild(linkDiv);
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log('Text copied to clipboard');
    }).catch(err => {
        console.error('Error in copying text: ', err);
    });
}

function updateButtonText(button, text) {
    const originalText = button.textContent;
    button.textContent = text;
    button.disabled = true;
    setTimeout(() => {
        button.textContent = originalText;
        button.disabled = false;
    }, 2000);
}

async function fetchTopicUrls(topic) {
    // Implement the logic to fetch URLs for the selected topic
    // This could involve making an API call to your backend or using pre-fetched data
    // For now, we'll return a dummy array
    return ['https://example.com/1', 'https://example.com/2', 'https://example.com/3'];
}