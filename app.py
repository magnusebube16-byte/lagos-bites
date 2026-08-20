from flask import Flask, request, jsonify
from flask_cors import CORS

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

    if "jollof" in text:
        reply = "Our Jollof Rice is ₦4,500 and is served with chicken."

    elif "chicken" in text:
        reply = "Our Grilled Chicken is ₦5,000."

    elif "pounded" in text or "egusi" in text:
        reply = "Pounded Yam & Egusi is ₦5,500."

    elif "menu" in text or "food" in text or "meal" in text:
        reply = "Our menu includes Jollof Rice (₦4,500), Grilled Chicken (₦5,000), and Pounded Yam & Egusi (₦5,500)."

    elif "open" in text or "close" in text or "hour" in text or "time" in text:
        reply = "We're open Monday to Saturday from 10:00 AM to 10:00 PM, and Sunday from 12:00 PM to 8:00 PM."

    elif "location" in text or "address" in text or "where" in text:
        reply = "We're located at 12 Admiralty Way, Lekki Phase 1, Lagos."

    elif "order" in text or "buy" in text:
        reply = "You can place an order using our order form, or contact us through WhatsApp."

    elif "hello" in text or "hi" in text or "hey" in text:
        reply = "Hi! 👋 Welcome to Lagos Bites. What would you like to know?"

    else:
        reply = "I can help with our menu, prices, opening hours, location, and ordering. What would you like to know?"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
