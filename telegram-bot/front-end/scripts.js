document.getElementById('get-urls-button').addEventListener('click', () => {
    // Placeholder for fetch functionality
    document.getElementById('result-box').value = 'Fetched URLs will appear here...';

    // Reset the copy button state
    const copyButton = document.getElementById('copy-urls-button');
    copyButton.textContent = 'Copy';
    copyButton.disabled = false;
    copyButton.classList.remove('unclickable');
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