// Select form and elements for greeting and view counter
const form = document.querySelector('#registration-form');
const responseMessage = document.querySelector('#response-message');
const counter = document.querySelector('#view-count');


form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const name = document.querySelector('#name').value;
    const email = document.querySelector('#email').value;
    const eventSelection = document.querySelector('#event').value;

    
    responseMessage.textContent = 'Submitting...';

    try {
        const response = await fetch('https://your-api-gateway-endpoint.amazonaws.com/dev/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, event: eventSelection })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        responseMessage.textContent = `Registration successful! ${result.message}`;
        
        
        updateCounter();
    } catch (error) {
        responseMessage.textContent = `Error: ${error.message}`;
    }
});


async function updateCounter() {
    try {
        const response = await fetch('https://your-api-gateway-endpoint.amazonaws.com/dev/views');
        const data = await response.json();
        counter.textContent = `Views: ${data.count}`;
    } catch (error) {
        counter.textContent = 'Error loading views';
    }
}


updateCounter();
