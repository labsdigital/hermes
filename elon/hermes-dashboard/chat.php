<?php
/**
 * Chat Page - Interface untuk chat dengan agent
 */

// Start session
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Check authentication
if (!isset($_SESSION['authenticated']) || $_SESSION['authenticated'] !== true) {
    header('Location: login.php');
    exit;
}

$user = [
    'username' => $_SESSION['username'],
    'name' => $_SESSION['user_name'] ?? 'User'
];

$pageTitle = 'Chat';

include 'includes/header.php';
?>

<div class="dashboard">
    <div class="chat-container">
        <div class="chat-header">
            <h1>💬 Chat with Agent</h1>
            <div class="chat-agent-select">
                <label for="agent-select">Select Agent:</label>
                <select id="agent-select">
                    <option value="zetta">🤖 Zetta (Main)</option>
                    <option value="max">📝 Max (Research)</option>
                    <option value="elon">🎨 Elon (Web Dev)</option>
                    <option value="chalbi">📖 Chalbi (Rumi)</option>
                    <option value="taraka">📋 Taraka (Foundation)</option>
                </select>
            </div>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message system">
                <div class="message-content">
                    Selamat datang di Hermes Chat! Pilih agent dan kirim pesan.
                </div>
            </div>
        </div>
        
        <div class="chat-input">
            <textarea 
                id="chatInput" 
                placeholder="Ketik pesan Anda..." 
                rows="3"
            ></textarea>
            <button id="sendBtn" onclick="sendMessage()">
                <span>Kirim</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
            </button>
        </div>
    </div>
</div>

<style>
.chat-container {
    max-width: 900px;
    margin: 0 auto;
    background: var(--color-white);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: calc(100vh - 140px);
}

.chat-header {
    padding: var(--space-lg);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--color-dark);
    color: var(--color-white);
}

.chat-header h1 {
    font-size: 24px;
    font-weight: 700;
}

.chat-agent-select {
    display: flex;
    align-items: center;
    gap: var(--space-md);
}

.chat-agent-select label {
    font-size: 14px;
    color: var(--color-muted);
}

.chat-agent-select select {
    padding: var(--space-sm) var(--space-md);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    font-family: inherit;
    font-size: 14px;
    background: var(--color-white);
    cursor: pointer;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: var(--space-lg);
    display: flex;
    flex-direction: column;
    gap: var(--space-md);
}

.message {
    display: flex;
    gap: var(--space-md);
    max-width: 80%;
}

.message.user {
    align-self: flex-end;
}

.message.agent {
    align-self: flex-start;
}

.message.system {
    align-self: center;
    max-width: 90%;
}

.message-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.message.user .message-avatar {
    background: var(--color-orange);
}

.message.agent .message-avatar {
    background: var(--color-dark);
}

.message.system .message-avatar {
    background: var(--color-border);
}

.message-content {
    padding: var(--space-md);
    border-radius: var(--radius-md);
    background: var(--color-bg);
    font-size: 14px;
    line-height: 1.6;
}

.message.user .message-content {
    background: var(--color-orange);
    color: var(--color-white);
}

.message.agent .message-content {
    background: var(--color-white);
    border: 1px solid var(--color-border);
}

.message.system .message-content {
    background: transparent;
    color: var(--color-muted);
    font-style: italic;
    text-align: center;
}

.message-time {
    font-size: 11px;
    color: var(--color-muted);
    margin-top: var(--space-sm);
}

.chat-input {
    padding: var(--space-lg);
    border-top: 1px solid var(--color-border);
    display: flex;
    gap: var(--space-md);
    background: var(--color-white);
}

.chat-input textarea {
    flex: 1;
    padding: var(--space-md);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-md);
    font-family: inherit;
    font-size: 14px;
    resize: none;
    transition: border-color var(--transition-fast);
}

.chat-input textarea:focus {
    outline: none;
    border-color: var(--color-orange);
}

.chat-input button {
    padding: var(--space-md) var(--space-xl);
    background: var(--color-orange);
    color: var(--color-white);
    border: none;
    border-radius: var(--radius-md);
    font-family: inherit;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    transition: background var(--transition-fast);
}

.chat-input button:hover {
    background: #ea6c0a;
}

.chat-input button:disabled {
    background: var(--color-muted);
    cursor: not-allowed;
}

.typing-indicator {
    display: flex;
    gap: 4px;
    padding: var(--space-md);
}

.typing-indicator span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--color-muted);
    animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-8px); }
}
</style>

<script>
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const agentSelect = document.getElementById('agent-select');
let sessionId = 'session_' + Date.now();

// Handle Enter key
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const message = chatInput.value.trim();
    const agent = agentSelect.value;
    
    if (!message) return;
    
    // Clear input
    chatInput.value = '';
    
    // Add user message
    addMessage('user', message, agent);
    
    // Show typing indicator
    showTyping();
    
    // Send to API
    try {
        const response = await fetch('api/chat.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                agent: agent,
                message: message,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTyping();
        
        if (data.success) {
            addMessage('agent', data.reply, agent);
        } else {
            addMessage('system', 'Error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        removeTyping();
        addMessage('system', 'Network error: ' + error.message);
    }
}

function addMessage(type, content, agent = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatar = type === 'user' ? '👤' : type === 'agent' ? getAgentEmoji(agent) : '⚙️';
    const time = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div>
            <div class="message-content">${escapeHtml(content)}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getAgentEmoji(agent) {
    const emojis = {
        'zetta': '🤖',
        'max': '📝',
        'elon': '🎨',
        'chalbi': '📖',
        'taraka': '📋'
    };
    return emojis[agent] || '🤖';
}

function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message agent';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById('typing-indicator');
    if (typing) {
        typing.remove();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Focus input on load
chatInput.focus();
</script>

<?php include 'includes/footer.php'; ?>
