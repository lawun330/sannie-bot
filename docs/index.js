// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    // Get references to various DOM elements
    const singleUrlInput = document.getElementById('single-url-input');
    const topicSelect = document.getElementById('topic-select');
    const getLinksContainer = document.getElementById('get-links-container');
    const getLinksButton = document.getElementById('get-links-button');
    const viewButton = document.getElementById('view-button');

    // Add change event listener to radio buttons
    document.querySelectorAll('input[name="option"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'insert-link') {
                if (singleUrlInput) singleUrlInput.style.display = 'block';
                if (topicSelect) topicSelect.style.display = 'none';
                if (getLinksContainer) getLinksContainer.style.display = 'none';
                if (viewButton) viewButton.style.display = 'block';
            } else if (e.target.value === 'topic') {
                if (singleUrlInput) singleUrlInput.style.display = 'none';
                if (topicSelect) topicSelect.style.display = 'block';
                if (getLinksContainer) getLinksContainer.style.display = 'block';
                if (viewButton) viewButton.style.display = 'none';
            }
        });
    });

    // Add click event listener to the "Get Links" button
    if (getLinksButton) {
        getLinksButton.addEventListener('click', async () => {
            console.log('Get Links button clicked');
            
            // Check if topicDropdown exists
            const topicDropdown = document.getElementById('topic-dropdown');
            if (!topicDropdown) {
                console.error('Topic dropdown element not found');
                return;
            }

            console.log('topicDropdown:', topicDropdown);

            const selectedIndex = topicDropdown.selectedIndex;
            console.log('selectedIndex:', selectedIndex);
            
            // Check if a valid option is selected
            if (selectedIndex === -1) {
                console.error('No option selected');
                return;
            }

            const selectedOption = topicDropdown.options[selectedIndex];
            console.log('selectedOption:', selectedOption);

            // Check if the selected option has a data-url attribute
            if (!selectedOption || !selectedOption.dataset || !selectedOption.dataset.url) {
                console.error('Selected option is invalid or does not have a data-url attribute');
                return;
            }

            const topicUrl = selectedOption.dataset.url;
            console.log('Topic URL:', topicUrl);
            
            // Send the selected URL to FastAPI
            await sendDataToFastAPI('/set_chosen_topic', { topic: topicUrl });
            
            // Add a delay before redirecting
            console.log('Redirecting to loading.html in 0 seconds...');
            setTimeout(() => {
                window.location.href = 'loading.html';
            }, 0); // 60000 milliseconds = 60 seconds
        });
    }

    // Add click event listener to the "View Contents" button
    if (viewButton) {
        viewButton.addEventListener('click', () => {
            // Get the manually entered URL
            const urlInput = document.getElementById('url-input').value;
            if (urlInput) {
                // Redirect to the content page with the entered URL
                navigateTo(`content.html?url=${encodeURIComponent(urlInput)}`, 'forward');
            } else {
                // Show an alert if no URL is entered
                alert('Please enter a URL first.');
            }
        });
    }

    // Add this to handle the back button in topic.html and content.html
    if (document.getElementById('back-button')) {
        document.getElementById('back-button').addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo('index.html', 'backward');
        });
    }
});

// Function to navigate to a new page with a smooth transition
function navigateTo(url, direction) {
    const container = document.querySelector('.container');
    container.classList.add(direction === 'forward' ? 'slide-left' : 'slide-right');
    
    setTimeout(() => {
        container.classList.add('instant');
        window.location.href = url;
    }, 300);
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
        
        const result = await response.json();
        console.log('Success:', result);
    } catch (error) {
        console.error('Error:', error);
    }
}
