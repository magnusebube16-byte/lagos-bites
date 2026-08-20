document.addEventListener("DOMContentLoaded", function () {
  const orderForm = document.getElementById("orderForm");

  if (orderForm) {
    orderForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const name = document.getElementById("customerName").value.trim();
      const meal = document.getElementById("meal").value;
      const quantity = Number(document.getElementById("quantity").value);
      const phone = document.getElementById("phone").value.trim();

      const prices = {
        "Jollof Rice": 4500,
        "Grilled Chicken": 5000,
        "Pounded Yam & Egusi": 5500
      };

      const price = prices[meal] || 0;
      const total = price * quantity;

      const message =
        `Hello Lagos Bites!%0A%0A` +
        `I'd like to place an order.%0A%0A` +
        `Name: ${encodeURIComponent(name)}%0A` +
        `Meal: ${encodeURIComponent(meal)}%0A` +
        `Quantity: ${encodeURIComponent(quantity)}%0A` +
        `Price: ₦${encodeURIComponent(price.toLocaleString())}%0A` +
        `Total: ₦${encodeURIComponent(total.toLocaleString())}%0A` +
        `Phone: ${encodeURIComponent(phone)}`;

      const whatsappNumber = "2348147752622";

      const whatsappUrl =
        `https://wa.me/${whatsappNumber}?text=${message}`;

      window.open(whatsappUrl, "_blank");
    });
  }

  console.log("Lagos Bites website loaded successfully.");
});

const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", function () {
    navLinks.classList.toggle("active");
  });

  navLinks.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      navLinks.classList.remove("active");
    });
  });
}

const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");

function addChatMessage(message, type) {
  const messageElement = document.createElement("div");
  messageElement.className = `chat-message ${type}`;

  const paragraph = document.createElement("p");
  paragraph.textContent = message;

  messageElement.appendChild(paragraph);
  chatMessages.appendChild(messageElement);

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function getAssistantResponse(question) {
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: question
      })
    });

    if (!response.ok) {
      throw new Error("Backend request failed");
    }

    const data = await response.json();
    return data.reply || "Sorry, I couldn't generate a response.";
  } catch (error) {
    console.error("Chat error:", error);
    return "Sorry, I can't reach the assistant right now.";
  }
}

if (chatForm && chatInput && chatMessages) {
  chatForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const question = chatInput.value.trim();

    if (!question) {
      return;
    }

    addChatMessage(question, "user");

    getAssistantResponse(question).then(function (response) {
      setTimeout(function () {
        addChatMessage(response, "bot");
      }, 400);
    });

    chatInput.value = "";
  });
}
