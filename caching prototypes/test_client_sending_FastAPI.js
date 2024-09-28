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

// Example usage
sendDataToFastAPI('/set_topic', { topic: 'example_topic_link' });
sendDataToFastAPI('/set_page', { page: 'example_page_link' });
sendDataToFastAPI('/set_content', { content: 'example_content_link' });