import nltk
import tkinter as tk
from tkinter import scrolledtext

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

faq_data = {
    "What is Ghar Soaps?": "Ghar Soaps is a brand offering handmade, natural, and chemical-free soap products.",
    "Are Ghar Soaps good for sensitive skin?": "Yes, Ghar Soaps are made with gentle, skin-friendly ingredients suitable for sensitive skin.",
    "Do Ghar Soaps contain parabens?": "No, all Ghar Soaps are free from parabens and harmful chemicals.",
    "Where can I buy Ghar Soaps?": "You can purchase Ghar Soaps from their official website or on Amazon.",
    "Are Ghar Soaps vegan and cruelty-free?": "Yes, Ghar Soaps are 100% vegan and never tested on animals.",
    "What ingredients are used in Ghar Soaps?": "Ghar Soaps are made with natural ingredients like coconut oil, turmeric, neem, and essential oils.",
    "Are Ghar Soaps cruelty-free?": "Absolutely! Ghar Soaps are 100% cruelty-free and never tested on animals.",
    "Do Ghar Soaps work for sensitive skin?": "Yes! Ghar Soaps are perfect for sensitive skin and help reduce irritation.",
    "Where can I buy Ghar Soaps?": "You can purchase Ghar Soaps on our official website and on Amazon.",
    "Is the packaging eco-friendly?": "Yes, all our packaging is eco-friendly and plastic-free.",
    "What products do you sell?": "🛍️ We offer a wide range of organic skincare products.",
    "Do you offer free shipping?": "📦 Yes! We offer free standard shipping on all orders above 500.",
    "When will my order arrive?": "🚚 Delivery usually takes 3–5 business days depending on your location.",
    "How can I track my order?": "🔍 You can track your order through the link provided in your confirmation email.",
    "What is your return policy?": "🔁 We accept returns within 10 days of delivery. The item must be unused and in original packaging.",
    "How do I return a product?": "📬 Visit your order history, select the item, and click on 'Request a Return'. Follow the on-screen steps.",
    "Can I cancel my order?": "❌ Yes, orders can be cancelled within 1 hour of placing them. After that, it may already be processed.",
    "What payment methods do you accept?": "💳 We accept credit/debit cards, UPI, PayPal, and wallet services like Google Pay.",
    "Is it safe to enter my card details?": "🔒 Absolutely! We use encrypted and PCI-compliant payment gateways to keep your information safe.",
    "I forgot my password. What do I do?": "🔑 No worries! Click on 'Forgot Password' on the login page to reset your credentials.",
    "How do I create an account?": "👤 Click on 'Sign Up' on the homepage and fill out your details to create a new account.",
    "How do I use a promo code?": "🏷️ You can apply your promo code during checkout on the payment screen.",
    "Do you offer international shipping?": "🌍 Yes! We ship to over 50 countries worldwide. Shipping times and charges may vary.",
    "How can I contact customer support?": "☎️ You can email us at support@example.com or call 1800-123-456 between 9AM to 6PM (Mon – Sat).",
    "Do you have physical stores?": "🏪 We're currently an online-only store, but stay tuned—we're expanding soon!",
}

greeting_inputs = ["hi", "hello", "hey", "greetings", "good morning", "good evening"]
greeting_responses = ["Hello! 😊", "Hi there!", "Hey! How can I help?", "Greetings! What would you like to know?"]

faq_keywords = ["faq", "faqs", "help", "what can i ask", "list questions"]

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if word not in stop_words]
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(lemmatized)

questions = list(faq_data.keys())
answers = list(faq_data.values())
processed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer()
vectorized_questions = vectorizer.fit_transform(processed_questions)

def get_response(user_input):
    user_input_clean = user_input.lower()

    # 1. Greeting detection
    if any(greet in user_input_clean for greet in greeting_inputs):
        return np.random.choice(greeting_responses)

    # 2. FAQ listing
    if any(keyword in user_input_clean for keyword in faq_keywords):
        all_faqs = "\n".join([f"- {q}" for q in questions])
        return f"Here are some things you can ask me:\n{all_faqs}"

    # 3. Regular FAQ match
    processed_input = preprocess(user_input)
    input_vector = vectorizer.transform([processed_input])
    similarities = cosine_similarity(input_vector, vectorized_questions)

    max_sim_index = np.argmax(similarities)
    max_sim_score = similarities[0][max_sim_index]

    if max_sim_score > 0.3:
        return answers[max_sim_index]
    else:
        return "Sorry, I don't have an answer to that. Try asking something else or type 'help' to see what you can ask."

def send_message():
    user_msg = user_input.get()
    if user_msg.strip() == "":
        return

    chat_window.config(state='normal')
    chat_window.insert(tk.END, f"You: {user_msg}\n", "user")
    response = get_response(user_msg)
    chat_window.insert(tk.END, f"GlowBot: {response}\n\n", "bot")
    chat_window.config(state='disabled')
    chat_window.see(tk.END)
    user_input.delete(0, tk.END)

# Window setup
root = tk.Tk()
root.title("GlowBot - Ghar Soaps FAQ Assistant")
root.geometry("500x600")
root.config(bg="#fdf6e3")

# Styles
BROWN = "#8b5e3c"
YELLOW = "#fff8dc"
FONT = ("Arial", 11)

# Chat display
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg=YELLOW, fg=BROWN, font=FONT)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_window.config(state='disabled')
chat_window.tag_config("user", foreground="#6b3e26", font=("Arial", 11, "bold"))
chat_window.tag_config("bot", foreground="#4d3319", font=("Arial", 11))

# Entry + Send button
frame = tk.Frame(root, bg="#fdf6e3")
frame.pack(padx=10, pady=10, fill=tk.X)

user_input = tk.Entry(frame, font=FONT, bg="#fffaf0", fg=BROWN)
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=6)
user_input.bind("<Return>", lambda event: send_message())

send_btn = tk.Button(frame, text="Send", font=("Arial", 11, "bold"), bg=BROWN, fg="white", command=send_message)
send_btn.pack(side=tk.RIGHT)


chat_window.config(state='normal')
chat_window.insert(tk.END, "🧼 GlowBot: Hi! I’m GlowBot, your Ghar Soaps assistant.\nAsk me anything, or type 'help' to see what you can ask!\n\n", "bot")
chat_window.config(state='disabled')

root.mainloop()