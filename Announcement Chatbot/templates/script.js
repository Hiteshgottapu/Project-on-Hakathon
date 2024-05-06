document.addEventListener("DOMContentLoaded", function() {
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    function appendUserMessage(message) {
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-message");
        userMessage.textContent = message;
        chatMessages.appendChild(userMessage);
    }

    function appendChatbotMessage(message) {
        const chatbotMessage = document.createElement("div");
        chatbotMessage.classList.add("chatbot-message");
        chatbotMessage.textContent = message;
        chatMessages.appendChild(chatbotMessage);
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function sendMessage() {
        const userMessageText = userInput.value.trim();
        if (userMessageText === "") return;

        appendUserMessage(userMessageText);
        scrollToBottom();

        // Send user message to the server (Python code) for processing
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: userMessageText }),
        })
            .then((response) => response.json())
            .then((data) => {
                const chatbotResponse = data.chatbot_response;
                appendChatbotMessage(chatbotResponse);
                scrollToBottom();
            })
            .catch((error) => {
                console.error("Error:", error);
            });

        userInput.value = "";
    }

    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendButton.click();
        }
    });

    sendButton.addEventListener("click", sendMessage);
});
