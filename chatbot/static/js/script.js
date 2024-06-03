document.getElementById('send-btn').addEventListener('click', sendMessage);

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const messagesContainer = document.getElementById('chatlogs');

    if (userInput.value.trim() === '') return;

    // Display user's message
    const userMessage = document.createElement('div');
    userMessage.className = 'user-msg';
    userMessage.textContent = userInput.value;
    messagesContainer.appendChild(userMessage);

    try {
        const response = await fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: userInput.value })
        });

        const data = await response.json();
        const botMessage = document.createElement('div');
        botMessage.className = 'bot-msg';
        botMessage.textContent = data.response;
        messagesContainer.appendChild(botMessage);
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = document.createElement('div');
        errorMessage.className = 'bot-msg';
        errorMessage.textContent = "Sorry, there was an error processing your request.";
        messagesContainer.appendChild(errorMessage);
    }

    // Clear input field and scroll to the bottom
    userInput.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
