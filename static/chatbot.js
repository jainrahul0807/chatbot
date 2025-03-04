(function () {
    // API Endpoint (Change if deployed)
    const API_URL = "http://localhost:5000/chat";

    // Create Chatbot Icon
    const chatbotIcon = document.createElement("div");
    chatbotIcon.id = "chatbotIcon";
    chatbotIcon.innerHTML = "💬";
    document.body.appendChild(chatbotIcon);

    // Create Chatbot Container
    const chatbotContainer = document.createElement("div");
    chatbotContainer.id = "chatbotContainer";
    chatbotContainer.innerHTML = `
        <div id="chatbotHeader">
            Chatbot
            <span id="closeChat">✖</span>
        </div>
        <div id="chatMessages"></div>
        <div id="chatInput">
            <input type="text" id="userMessage" placeholder="Type a message..." />
            <button id="sendMessage">Send</button>
        </div>
    `;
    document.body.appendChild(chatbotContainer);

    // Apply Styles
    const style = document.createElement("style");
    style.innerHTML = `
        #chatbotIcon {
            position: fixed; bottom: 20px; right: 20px;
            width: 60px; height: 60px; background: #007bff; color: white;
            border-radius: 50%; display: flex; justify-content: center;
            align-items: center; font-size: 30px; cursor: pointer;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        #chatbotContainer {
            position: fixed; bottom: 90px; right: 20px;
            width: 320px; background: white; border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            display: none; flex-direction: column; overflow: hidden;
        }
        #chatbotHeader {
            background: #007bff; color: white; padding: 10px; text-align: center;
            font-weight: bold; position: relative;
        }
        #closeChat { position: absolute; right: 10px; top: 5px; cursor: pointer; font-size: 18px; }
        #chatMessages { height: 300px; overflow-y: auto; padding: 10px; background: #f7f7f7; }
        #chatInput { display: flex; padding: 5px; border-top: 1px solid #ddd; background: white; }
        #userMessage { flex: 1; padding: 8px; border: none; outline: none; }
        #sendMessage { background: #007bff; color: white; border: none; padding: 8px 12px; cursor: pointer; }
    `;
    document.head.appendChild(style);

    // Show/Hide Chatbot
    chatbotIcon.addEventListener("click", () => {
        chatbotContainer.style.display = chatbotContainer.style.display === "none" ? "flex" : "none";
    });
    document.getElementById("closeChat").addEventListener("click", () => {
        chatbotContainer.style.display = "none";
    });

    // Send Message to API
    async function sendMessage() {
        let userMessage = document.getElementById("userMessage").value.trim();
        if (!userMessage) return;

        displayMessage(userMessage, "user");
        document.getElementById("userMessage").value = "";

        try {
            let response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });

            let data = await response.json();
            displayMessage(data.response, "bot");
        } catch (error) {
            displayMessage("❌ Error: Unable to connect to chatbot.", "bot");
        }
    }

    // Display Message
    function displayMessage(text, sender) {
        let chatMessages = document.getElementById("chatMessages");
        let messageDiv = document.createElement("div");
        messageDiv.textContent = text;
        messageDiv.style.padding = "8px";
        messageDiv.style.margin = "5px";
        messageDiv.style.borderRadius = "5px";
        messageDiv.style.maxWidth = "80%";

        if (sender === "user") {
            messageDiv.style.background = "#007bff";
            messageDiv.style.color = "white";
            messageDiv.style.alignSelf = "flex-end";
        } else {
            messageDiv.style.background = "#ddd";
            messageDiv.style.color = "black";
            messageDiv.style.alignSelf = "flex-start";
        }

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    document.getElementById("sendMessage").addEventListener("click", sendMessage);
})();




//API Integration: <script src="http://localhost:5000/script"></script>