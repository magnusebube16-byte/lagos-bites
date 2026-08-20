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

    prices = {
        "jollof": 4500,
        "chicken": 5000,
        "pounded": 5500,
        "egusi": 5500,
    }

    # Greeting - use whole words so "hi" does not match "chicken"
    if any(
        re.search(r"\b" + re.escape(word) + r"\b", text)
        for word in [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
        ]
    ):
        reply = (
            "Hi! 👋 Welcome to Lagos Bites. "
            "I can help with our menu, prices, recommendations, "
            "opening hours, location, and orders."
        )

    # Mixed orders
    elif any(item in text for item in ["jollof", "chicken", "egusi", "pounded"]):
        quantities = {
            "jollof": 0,
            "chicken": 0,
            "pounded": 0
        }

        # Find quantities directly before each food
        for item in quantities:
            match = re.search(r"(\d+)\s*(?:[^\d,]*?)" + item, text)
            if match:
                quantities[item] = int(match.group(1))
            elif item in text:
                quantities[item] = 1

        # Treat egusi as Pounded Yam & Egusi
        if "egusi" in text and quantities["pounded"] == 0:
            egusi_match = re.search(r"(\d+)\s*(?:[^\d,]*?)egusi", text)
            quantities["pounded"] = int(egusi_match.group(1)) if egusi_match else 1

        jollof_total = quantities["jollof"] * prices["jollof"]
        chicken_total = quantities["chicken"] * prices["chicken"]
        pounded_total = quantities["pounded"] * prices["pounded"]

        total = jollof_total + chicken_total + pounded_total

        parts = []

        if quantities["jollof"]:
            parts.append(
                f"{quantities['jollof']} Jollof Rice = ₦{jollof_total:,}"
            )

        if quantities["chicken"]:
            parts.append(
                f"{quantities['chicken']} Grilled Chicken = ₦{chicken_total:,}"
            )

        if quantities["pounded"]:
            parts.append(
                f"{quantities['pounded']} Pounded Yam & Egusi = ₦{pounded_total:,}"
            )

        reply = "\n".join(parts) + f"\nTotal = ₦{total:,}"
    # Budget questions
    elif re.search(r"(?:₦|ngn|n)?\s*10[,.]?000", text):
        reply = (
            "With ₦10,000, you can get:\n"
            "🍚 2 Jollof Rice = ₦9,000, leaving ₦1,000.\n"
            "🍗 2 Grilled Chicken = ₦10,000 exactly.\n"
            "🥘 1 Pounded Yam & Egusi + 1 Jollof Rice = ₦10,000 exactly.\n\n"
            "Best value: 2 Jollof Rice meals for ₦9,000."
        )

    elif "budget" in text or "afford" in text or "within" in text:
        reply = (
            "Our most affordable meal is Jollof Rice at ₦4,500. "
            "Grilled Chicken is ₦5,000, while Pounded Yam & Egusi is ₦5,500."
        )
    # Recommendations
    elif any(
        phrase in text
        for phrase in ["recommend", "suggest", "best", "what should i eat"]
    ):
        reply = (
            "I'd recommend our Jollof Rice with chicken 🍗. "
            "It's ₦4,500 and is one of our customer favourites!"
        )

    # Quantity
    else:
        number_words = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
        }

        quantity = 1

        match = re.search(r"\b(\d+)\b", text)

        if match:
            quantity = int(match.group(1))
        else:
            for word, number in number_words.items():
                if re.search(r"\b" + word + r"\b", text):
                    quantity = number
                    break

        quantity = max(1, min(quantity, 20))

        if "jollof" in text:
            total = quantity * prices["jollof"]

            if quantity > 1:
                reply = (
                    f"{quantity} Jollof Rice meals would cost "
                    f"₦{total:,}. Each meal is ₦4,500."
                )
            else:
                reply = (
                    "Our Jollof Rice is ₦4,500 and is served with chicken."
                )

        elif "chicken" in text:
            total = quantity * prices["chicken"]

            if quantity > 1:
                reply = (
                    f"{quantity} Grilled Chicken meals would cost "
                    f"₦{total:,}. Each meal is ₦5,000."
                )
            else:
                reply = "Our Grilled Chicken is ₦5,000."

        elif "pounded" in text or "egusi" in text:
            total = quantity * prices["pounded"]

            if quantity > 1:
                reply = (
                    f"{quantity} Pounded Yam & Egusi meals would cost "
                    f"₦{total:,}. Each meal is ₦5,500."
                )
            else:
                reply = "Pounded Yam & Egusi is ₦5,500."

        elif "menu" in text or "food" in text or "meal" in text:
            reply = (
                "Our menu includes:\n"
                "🍚 Jollof Rice — ₦4,500\n"
                "🍗 Grilled Chicken — ₦5,000\n"
                "🥘 Pounded Yam & Egusi — ₦5,500"
            )

        elif any(
            word in text for word in ["open", "close", "hour", "time"]
        ):
            day = datetime.now().strftime("%A")

            if day == "Sunday":
                reply = "Today is Sunday. We're open from 12:00 PM to 8:00 PM."
            else:
                reply = (
                    f"Today is {day}. We're open from 10:00 AM to 10:00 PM."
                )

        elif any(
            word in text for word in ["location", "address", "where"]
        ):
            reply = (
                "We're located at 12 Admiralty Way, Lekki Phase 1, "
                "Lagos, Nigeria. 📍"
            )

        elif "whatsapp" in text:
            reply = (
                "Yes! 📱 You can order through WhatsApp using "
                "the WhatsApp button on our website."
            )

        elif "order" in text or "buy" in text:
            reply = (
                "Absolutely! 🛍️ You can place an order using "
                "our order form or contact us through WhatsApp."
            )

        else:
            reply = (
                "I can help with our menu, prices, meal quantities, "
                "recommendations, opening hours, location, delivery, "
                "WhatsApp orders, and general ordering. What would you like to know?"
            )

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
