(function () {
  let chatbotFrame = document.createElement("iframe");
  chatbotFrame.src = "https://chatbot-5dsh.onrender.com";
  chatbotFrame.style.width = "350px";
  chatbotFrame.style.height = "500px";
  chatbotFrame.style.border = "none";
  chatbotFrame.style.position = "fixed";
  chatbotFrame.style.bottom = "20px";
  chatbotFrame.style.right = "20px";
  chatbotFrame.style.zIndex = "9999";
  chatbotFrame.style.boxShadow = "0px 4px 10px rgba(0,0,0,0.2)";
  chatbotFrame.style.borderRadius = "10px";

  document.body.appendChild(chatbotFrame);
})();
