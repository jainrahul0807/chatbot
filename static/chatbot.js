(function() {
    // Check if chatbot already exists
    if (document.getElementById("chatbot-icon")) return;

    // Create Chatbot Icon
    var chatbotIcon = document.createElement("div");
    chatbotIcon.id = "chatbot-icon";
    chatbotIcon.innerHTML = '<img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" alt="Chatbot">';
    document.body.appendChild(chatbotIcon);

    // Create Chatbot Box (Initially Hidden)
    var chatbotBox = document.createElement("div");
    chatbotBox.id = "chatbot-box";
    chatbotBox.style.display = "none";
    chatbotBox.innerHTML = `
        <button id="close-chatbot">✖</button>
        <iframe src="https://chatbot-5dsh.onrender.com"></iframe>
    `;
    document.body.appendChild(chatbotBox);

    // Add CSS Styles
    var style = document.createElement("style");
    style.innerHTML = `
        #chatbot-icon {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background-color: #007bff;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 10000;
        }
        #chatbot-icon img {
            width: 40px;
            height: 40px;
        }
        #chatbot-box {
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            z-index: 9999;
        }
        #close-chatbot {
            position: absolute;
            top: 5px;
            right: 10px;
            background: red;
            color: white;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 5px;
        }
        #chatbot-box iframe {
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 10px;
        }
    `;
    document.head.appendChild(style);

    // Add Toggle Functionality
    chatbotIcon.onclick = function() {
        chatbotBox.style.display = chatbotBox.style.display === "none" ? "block" : "none";
    };
    document.getElementById("close-chatbot").onclick = function() {
        chatbotBox.style.display = "none";
    };
})();
