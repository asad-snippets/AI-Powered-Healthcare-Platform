let chatHistory = [];

// Function to toggle chat window visibility
function toggleChatWindow() {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'block' : 'none';
}

// Function to close the chat window
function closeChatWindow() {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.style.display = 'none';  // Hides the chat window
}

// Function to send a message
function sendMessage() {
    const messageInput = document.getElementById('chat-input');
    const userMessage = messageInput.value.trim();
    if (userMessage === '') return;

    // Display the user's message
    addMessageToChat(userMessage, 'user');

    // Send the message to the backend
    fetch('/chatbot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = data.response;
        // Display the bot's response
        addMessageToChat(botMessage, 'bot');
    })
    .catch(error => console.error('Error:', error));

    // Clear the input field
    messageInput.value = '';
}

// Function to add a message to the chat window
function addMessageToChat(message, role) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add(role === 'bot' ? 'bot-message' : 'user-message');
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);

    // Scroll to the bottom automatically after adding a new message
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Handle "Enter" key press
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
