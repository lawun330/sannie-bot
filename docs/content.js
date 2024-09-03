document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const url = urlParams.get('url');
    const contentContainer = document.getElementById('content-container');
    const backButton = document.getElementById('back-button');

    if (url) {
        fetchContent(url).then(content => {
            displayContent(content);
        });
    } else {
        contentContainer.textContent = 'No URL provided.';
    }

    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
});

async function fetchContent(url) {
    // In a real-world scenario, you would make an API call to your backend
    // to fetch the scraped content. For this example, we'll use dummy content.
    return `This is the scraped content from ${url}. 
    It would typically contain the main text of the article, 
    formatted for easy reading.`;
}

function displayContent(content) {
    const contentContainer = document.getElementById('content-container');
    contentContainer.textContent = content;
}