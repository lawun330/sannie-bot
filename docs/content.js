// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', () => {
    // Get references to DOM elements
    const contentContainer = document.getElementById('content-container');
    const saveButton = document.getElementById('save-button');
    const backButton = document.getElementById('back-button');
    const copyButton = document.getElementById('copy-button');

    // Fetch and display the content (implementation needed)
    fetchContent().then(content => {
        contentContainer.textContent = content;
    });

    // Add click event listener to the copy button
    copyButton.addEventListener('click', () => {
        const content = contentContainer.textContent;
        navigator.clipboard.writeText(content).then(() => {
            alert('Content copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy content: ', err);
        });
    });

    // Add click event listener to the save button
    saveButton.addEventListener('click', () => {
        // Get the content from the container
        const content = contentContainer.textContent;
        // Create a Blob with the content
        const blob = new Blob([content], { type: 'text/plain' });
        // Create a URL for the Blob
        const url = URL.createObjectURL(blob);
        // Create a temporary anchor element
        const a = document.createElement('a');
        
        // Set the download attributes
        a.href = url;
        a.download = 'bbc_burmese_content.txt';
        // Append the anchor to the body, click it, and remove it
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        // Revoke the Blob URL to free up resources
        URL.revokeObjectURL(url);
    });

    // Add click event listener to the back button
    backButton.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
});

// Function to fetch content (implementation needed)
async function fetchContent() {
    // Implement the logic to fetch content
    // This could involve making an API call to your backend or using pre-fetched data
    // For now, we'll return a dummy text
    return "This is where the scraped content from BBC Burmese News will appear. It will be scrollable and copyable.";
}