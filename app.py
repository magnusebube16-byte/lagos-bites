from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import datetime

app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app)


@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("message", "").strip()

    if not question:
        return jsonify({"reply": "Please enter a question."}), 400

    text = question.lower()

    # Menu
    prices = {
        "jollof": 4500,
        "chicken": 5000,
        "pounded": 5500,
        "egusi": 5500
    }

    # Detect quantity: 2, two, 3, three, etc.
    number_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5
    }

    quantity = 1

    match = re.search(r"\b(\d+)\b", text)

    if match:
        quantity = int(match.group(1))
    else:
        for word, number in number_words.items():
            if word in text:
                quantity = number
                break

    # Keep quantity reasonable
    quantity = max(1, min(quantity, 20))

    # Greeting
    if any(word in text for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        reply = "Hi! 👋 Welcome to Lagos Bites. I can help you with our menu, prices, recommendations, opening hours, location, and orders."

    # Budget questions
    elif "5000" in text or "5,000" in text or "₦5000" in text or "₦5,000" in text:
        reply = "With ₦5,000, you can get Jollof Rice for ₦4,500, leaving you ₦500. Grilled Chicken is exactly ₦5,000."

    elif "budget" in text or "afford" in text or "within" in text:
        reply = "Our most affordable meal is Jollof Rice at ₦4,500. Grilled Chicken is ₦5,000, while Pounded Yam & Egusi is ₦5,500."

    # Recommendations
    elif "recommend" in text or "suggest" in text or "best" in text or "what should i eat" in text:
        reply = "I'd recommend our Jollof Rice with chicken 🍗. It's ₦4,500 and is one of our customer favourites!"

    # Jollof
    elif "jollof" in text:
        total = quantity * prices["jollof"]

        if quantity > 1:
            reply = f"{quantity} Jollof Rice meals would cost ₦{total:,}. Each meal is ₦4,500."
        else:
            reply = "Our Jollof Rice is ₦4,500 and is served with chicken."

    # Chicken
    elif "chicken" in text:
        total = quantity * prices["chicken"]

        if quantity > 1:
            reply = f"{quantity} Grilled Chicken meals would cost ₦{total:,}. Each meal is ₦5,000."
        else:
            reply = "Our Grilled Chicken is ₦5,000."

    # Pounded yam / Egusi
    elif "pounded" in text or "egusi" in text:
        total = quantity * prices["pounded"]

        if quantity > 1:
            reply = f"{quantity} Pounded Yam & Egusi meals would cost ₦{total:,}. Each meal is ₦5,500."
        else:
            reply = "Pounded Yam & Egusi is ₦5,500."

    # Menu
    elif "menu" in text or "food" in text or "meals" in text:
        reply = "Our menu includes:\n🍚 Jollof Rice — ₦4,500\n🍗 Grilled Chicken — ₦5,000\n🥘 Pounded Yam & Egusi — ₦5,500"

    # Opening hours
    elif "open" in text or "close" in text or "hour" in text or "time" in text:
        now = datetime.now()
        day = now.strftime("%A")

        if day == "Sunday":
            reply = "Today is Sunday. We're open from 12:00 PM to 8:00 PM."
        else:
            reply = f"Today is {day}. We're open from 10:00 AM to 10:00 PM."

    # Location
    elif "location" in text or "address" in text or "where" in text:
        reply = "We're located at 12 Admiralty Way, Lekki Phase 1, Lagos, Nigeria. 📍"

    # WhatsApp ordering
    elif "whatsapp" in text:
        reply = "Yes! 📱 You can order through WhatsApp using the WhatsApp button on our website."

    # Ordering
    elif "order" in text or "buy" in text:
        reply = "Absolutely! 🛍️ You can place an order using our order form on the website, or contact Lagos Bites through WhatsApp."

    # Delivery
    elif "delivery" in text or "deliver" in text:
        reply = "You can contact Lagos Bites through WhatsApp to ask about delivery options and availability."

    # Contact
    elif "contact" in text or "phone" in text or "call" in text:
        reply = "You can contact Lagos Bites by phone or WhatsApp using the contact buttons on our website."

    # Default
    else:
        reply = "I can help with our menu, prices, meal quantities, recommendations, opening hours, location, delivery, WhatsApp orders, and general ordering. What would you like to know?"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
