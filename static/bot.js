function toggleChatWindow() {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.style.display = chatWindow.style.display === 'block' ? 'none' : 'block';
}

function closeChatWindow() {
    document.getElementById('chatWindow').style.display = 'none';
}

function handleKeyPress(event) {
    if (event.key === 'Enter') sendMessage();
}

function sendMessage() {
    const input = document.getElementById('chatInput');
    const messageText = input.value.trim();
    if (!messageText) return;

    const chatBox = document.getElementById('chatBox');
    chatBox.innerHTML += `<div class="user-message"><strong>You:</strong> ${messageText}</div>`;
    input.value = '';

    fetch('/chatbot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ message: messageText })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div class="bot-message"><strong>Bot:</strong> ${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        chatBox.innerHTML += `<div class="bot-message">⚠️ Error occurred.</div>`;
    });
}

function getCSRFToken() {
    const name = 'csrftoken';
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    return parts.length === 2 ? parts.pop().split(';').shift() : '';
}
