// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    // Get references to various DOM elements
    const singleUrlInput = document.getElementById('single-url-input');
    const topicSelect = document.getElementById('topic-select');
    const getLinksContainer = document.getElementById('get-links-container');
    const viewButton = document.getElementById('view-button');
    const optionRadios = document.getElementsByName('option');
    const getLinksButton = document.getElementById('get-links-button');

    // Add event listeners to radio buttons
    optionRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            // Show or hide elements based on selected option
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

    // Add click event listener to the "Get Links" button
    getLinksButton.addEventListener('click', () => {
        // Get the selected topic URL from the dropdown
        const selectedTopic = document.getElementById('depth-select');
        const selectedUrl = selectedTopic.options[selectedTopic.selectedIndex].getAttribute('data-url');
        // Redirect to the topic page with the selected URL
        window.location.href = `topic.html?url=${encodeURIComponent(selectedUrl)}`;
    });

    // Add click event listener to the "View Contents" button
    viewButton.addEventListener('click', () => {
        // Get the manually entered URL
        const urlInput = document.getElementById('url-input').value;
        if (urlInput) {
            // Redirect to the content page with the entered URL
            window.location.href = `content.html?url=${encodeURIComponent(urlInput)}`;
        } else {
            // Show an alert if no URL is entered
            alert('Please enter a URL first.');
        }
    });

    // Add change event listener to the depth select dropdown
    document.getElementById('depth-select').addEventListener('change', function() {
        // Get the selected value and URL
        const selectedValue = this.value;
        const selectedUrl = this.options[this.selectedIndex].getAttribute('data-url');
        
        // Use selectedValue (in Burmese) and selectedUrl as needed
    });
});

// Add click event listener to the "Copy URLs" button
document.getElementById('copy-urls-button').addEventListener('click', () => {
    // Get the result box element
    const resultBox = document.getElementById('result-box');
    // Select the text in the result box
    resultBox.select();
    // Copy the selected text to the clipboard
    document.execCommand('copy');

    // Change button text and make it unclickable
    const copyButton = document.getElementById('copy-urls-button');
    copyButton.textContent = 'Copied!';
    copyButton.disabled = true;
    copyButton.classList.add('unclickable');
});
