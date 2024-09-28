const http = require('http');

function fetchHelloWorld() {
    http.get('http://127.0.0.1:8000/', (response) => {
        let data = '';

        response.on('data', (chunk) => {
            data += chunk;
        });

        response.on('end', () => {
            console.log(data); // Should print "Hello World!"
        });
    }).on('error', (error) => {
        console.error('Error:', error.message);
    });
}

fetchHelloWorld();
