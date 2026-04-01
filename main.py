import tkinter as tk
from tkinter import scrolledtext
from util import load_faq, ChatEngine, correct_spelling
import datetime

# Load data
questions, answers = load_faq("faq_data.json")
engine = ChatEngine(questions)

greetings = ["hi", "hello", "hey"]
greet_responses = ["Hi! 😊", "Hello!", "Hey there!"]

# Logging
def log_query(user, bot):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | Q: {user} | A: {bot}\n")


def get_bot_response(user_input):
    user_input_lower = user_input.lower()

    # Greeting
    if any(greet in user_input_lower for greet in greetings):
        return greet_responses[0]

    # Spell correction
    corrected = correct_spelling(user_input, questions)

    response = engine.get_response(corrected, questions, answers)

    if response:
        return response
    else:
        return "Sorry, I couldn't understand that. Try asking something else."


def send_message():
    user_msg = entry.get()
    if not user_msg.strip():
        return

    chat.config(state='normal')
    chat.insert(tk.END, f"You: {user_msg}\n", "user")

    bot_reply = get_bot_response(user_msg)

    chat.insert(tk.END, f"GlowBot: {bot_reply}\n\n", "bot")
    chat.config(state='disabled')
    chat.see(tk.END)

    log_query(user_msg, bot_reply)
    entry.delete(0, tk.END)


# UI
root = tk.Tk()
root.title("GlowBot")
root.geometry("500x600")

chat = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat.config(state='disabled')

entry = tk.Entry(root)
entry.pack(fill=tk.X, padx=10, pady=10)
entry.bind("<Return>", lambda e: send_message())

btn = tk.Button(root, text="Send", command=send_message)
btn.pack()

chat.config(state='normal')
chat.insert(tk.END, "GlowBot: Hi! Ask me anything 😊\n\n")
chat.config(state='disabled')

root.mainloop()