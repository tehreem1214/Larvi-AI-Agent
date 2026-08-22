const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const chatContainer = document.getElementById("chatContainer");

function addMessage(message, sender) {
    const messageDiv = document.createElement("div");

    messageDiv.className = "message";

    if (sender === "user") {
        messageDiv.classList.add("user");

        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="sender">You</div>
                <div class="bubble">${message}</div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="avatar">L</div>
            <div class="message-content">
                <div class="sender">Larvi</div>
                <div class="bubble">${message}</div>
            </div>
        `;
    }

    chatContainer.appendChild(messageDiv);

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (message === "") {
        return;
    }

    addMessage(message, "user");

    userInput.value = "";

    sendButton.disabled = true;
    sendButton.textContent = "Thinking...";

    try {
        const url = `/agent?request=${encodeURIComponent(message)}`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        if (data.success) {
            addMessage(data.response, "assistant");
        } else {
            addMessage(
                data.error || "Something went wrong.",
                "assistant"
            );
        }
    } catch (error) {
        addMessage(
            "Larvi server se connect nahi ho saka.",
            "assistant"
        );

        console.error(error);
    }

    sendButton.disabled = false;
    sendButton.textContent = "Send";

    userInput.focus();
}

sendButton.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});