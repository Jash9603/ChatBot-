
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

const API_BASE_URL = 'http://localhost:8000';


document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('welcomeTime').textContent = getCurrentTime();
    
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
    });
    
    messageInput.focus();
});

function getCurrentTime() {
    return new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
    });
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (message === '') return;
    
    messageInput.value = '';
    sendButton.disabled = true;
    
    addUserMessage(message);
    showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: message })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        addBotMessage(data.answer, data.source);
        
    } catch (error) {
        hideTypingIndicator();
        addBotMessage('Sorry, I encountered an error. Please try again.', null);
    } finally {
        sendButton.disabled = false;
        messageInput.focus();
    }
}

function addUserMessage(message) {
    const messageElement = createMessageElement(message, 'user');
    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

function addBotMessage(message, source) {
    const messageElement = createMessageElement(message, 'bot', source);
    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

function createMessageElement(message, sender, source = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    
    if (sender === 'bot') {
        
        textDiv.innerHTML = marked.parse(message);

        if (source) {
            const sourceDiv = document.createElement('div');
            sourceDiv.style.marginTop = '8px';
            sourceDiv.style.paddingTop = '8px';
            sourceDiv.style.borderTop = '1px solid #eee';
            sourceDiv.style.fontSize = '0.85em';
            sourceDiv.style.color = '#666';
            sourceDiv.innerHTML = `<strong>Source:</strong> ${escapeHtml(source)}`;
            textDiv.appendChild(sourceDiv);
        }
    } else {
        textDiv.textContent = message;
    }
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = getCurrentTime();
    
    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(contentDiv);
    
    return messageDiv;
}

function showTypingIndicator() {
    typingIndicator.classList.add('show');
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.classList.remove('show');
}

function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;', '<': '&lt;', '>': '&gt;', 
        '"': '&quot;', "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
