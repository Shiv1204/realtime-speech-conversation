import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import tkinter as tk
from tkinter import scrolledtext, ttk
from conversation import generate_response
import threading
import speech_recognition as sr

class ConversationUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Realtime Speech Conversation")
        self.root.geometry("700x500")
        self.root.configure(bg="#f4f6fb")

        self.history = []

        # Conversation display frame
        conv_frame = tk.Frame(root, bg="#e3eaf2", bd=2, relief=tk.GROOVE)
        conv_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.conversation_display = scrolledtext.ScrolledText(
            conv_frame, width=70, height=18, state='disabled',
            font=("Segoe UI", 12), bg="#f9fbfd", fg="#222"
        )
        self.conversation_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # User input frame
        input_frame = tk.Frame(root, bg="#f4f6fb")
        input_frame.pack(padx=20, pady=(0,10), fill=tk.X)

        self.user_input = tk.Entry(input_frame, width=60, font=("Segoe UI", 12))
        self.user_input.pack(side=tk.LEFT, padx=(0,10), pady=5, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)

        # Buttons frame
        btn_frame = tk.Frame(root, bg="#f4f6fb")
        btn_frame.pack(padx=20, pady=(0,10), fill=tk.X)

        self.start_button = ttk.Button(btn_frame, text="Start", command=self.start_conversation)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = ttk.Button(btn_frame, text="Stop", command=self.stop_conversation, state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.speak_button = ttk.Button(btn_frame, text="🎤 Speak", command=self.speak_message)
        self.speak_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.send_button = ttk.Button(btn_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready.")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e3eaf2", font=("Segoe UI", 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.conversation_active = False

    def start_conversation(self):
        self.conversation_active = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.append_conversation("System", "Conversation started.")
        self.status_var.set("Conversation started.")

    def stop_conversation(self):
        self.conversation_active = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.append_conversation("System", "Conversation stopped.")
        self.status_var.set("Conversation stopped.")

    def send_message(self, event=None):
        if not self.conversation_active:
            self.append_conversation("System", "Start the conversation first.")
            self.status_var.set("Please start the conversation.")
            return
        user_text = self.user_input.get().strip()
        if not user_text:
            self.status_var.set("Please enter your message.")
            return
        self.append_conversation("You", user_text)
        self.user_input.delete(0, tk.END)
        self.status_var.set("Assistant is thinking...")
        threading.Thread(target=self._get_response, args=(user_text,)).start()

    def _get_response(self, user_text):
        response = generate_response(self.history, user_text)
        self.append_conversation("Assistant", response)
        self.history.append(("User", user_text))
        self.history.append(("Assistant", response))
        self.status_var.set("Ready.")

    def speak_message(self):
        threading.Thread(target=self._recognize_speech).start()

    def _recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.status_var.set("Listening...")
            self.append_conversation("System", "Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                user_text = recognizer.recognize_google(audio)
                self.user_input.delete(0, tk.END)
                self.user_input.insert(0, user_text)
                self.append_conversation("You (voice)", user_text)
                self.status_var.set("Assistant is thinking...")
                self._get_response(user_text)
            except sr.WaitTimeoutError:
                self.append_conversation("System", "Listening timed out.")
                self.status_var.set("Listening timed out.")
            except sr.UnknownValueError:
                self.append_conversation("System", "Could not understand audio.")
                self.status_var.set("Could not understand audio.")
            except Exception as e:
                self.append_conversation("System", f"Error: {e}")
                self.status_var.set(f"Error: {e}")

    def append_conversation(self, speaker, text):
        self.conversation_display.config(state='normal')
        self.conversation_display.insert(tk.END, f"{speaker}: {text}\n")
        self.conversation_display.config(state='disabled')
        self.conversation_display.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversationUI(root)
    root.mainloop()