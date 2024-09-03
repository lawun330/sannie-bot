document.addEventListener('DOMContentLoaded', () => {
    const singleUrlInput = document.getElementById('single-url-input');
    const topicSelect = document.getElementById('topic-select');
    const getLinksContainer = document.getElementById('get-links-container');
    const viewButton = document.getElementById('view-button');
    const optionRadios = document.getElementsByName('option');
    const getLinksButton = document.getElementById('get-links-button');

    optionRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'insert-link') {
                singleUrlInput.style.display = 'block';
                topicSelect.style.display = 'none';
                getLinksContainer.style.display = 'none';
                viewButton.style.display = 'block';
            } else {
                singleUrlInput.style.display = 'none';
                topicSelect.style.display = 'block';
                getLinksContainer.style.display = 'block';
                viewButton.style.display = 'none';
            }
        });
    });

    getLinksButton.addEventListener('click', () => {
        const selectedOption = document.querySelector('input[name="option"]:checked').value;
        if (selectedOption === 'single-url') {
            // Handle single URL input (existing functionality)
            const urlInput = document.getElementById('url-input').value;
            // Process the single URL
        } else {
            // Redirect to the topic page with the selected topic
            const selectedTopic = document.getElementById('depth-select').value;
            window.location.href = `topic.html?topic=${selectedTopic}`;
        }
    });

    viewButton.addEventListener('click', () => {
        const urlInput = document.getElementById('url-input').value;
        if (urlInput) {
            window.location.href = `content.html?url=${encodeURIComponent(urlInput)}`;
        } else {
            alert('Please enter a URL first.');
        }
    });
});

document.getElementById('copy-urls-button').addEventListener('click', () => {
    const resultBox = document.getElementById('result-box');
    resultBox.select();
    document.execCommand('copy');

    // Change button to "Copied!" and make it unclickable
    const copyButton = document.getElementById('copy-urls-button');
    copyButton.textContent = 'Copied!';
    copyButton.disabled = true;
    copyButton.classList.add('unclickable');
});

document.getElementById('view-button').addEventListener('click', () => {
    window.location.href = 'another-page.html'; // Link to the new page
});