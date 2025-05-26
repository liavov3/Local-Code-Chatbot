import os
import subprocess
import tkinter as tk
from tkinter import ttk
from langchain_ollama import OllamaLLM

class ChatBotApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Coding Assistant")
        self.geometry("600x500")
        self.minsize(400, 400)
        self.configure(bg="#2b2b2b")

        # Paths for local Ollama and model
        self.OLLAMA_PATH = os.path.join(os.getcwd(), "ollama", "ollama.exe")
        self.MODEL_PATH = os.path.join(os.getcwd(), "models")

        # Start Ollama from local folder
        subprocess.Popen([self.OLLAMA_PATH, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Load the local model
        self.model = OllamaLLM(model="codellama:7b")  # Or "mistral"

        # Apply styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.create_widgets()

    def create_widgets(self):
        """Create the chat UI components"""
        chat_frame = ttk.Frame(self, padding=10)
        chat_frame.pack(expand=True, fill="both")

        self.chat_history = tk.Text(
            chat_frame, wrap=tk.WORD, bg="#3c3f41", fg="white", font=("Arial", 12), state="disabled", height=20
        )
        self.chat_history.pack(expand=True, fill="both", side="left", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(chat_frame, command=self.chat_history.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_history.config(yscrollcommand=scrollbar.set)

        self.entry = ttk.Entry(self, font=("Arial", 12))
        self.entry.pack(fill="x", padx=10, pady=5)
        self.entry.focus()

        send_button = ttk.Button(self, text="Send", command=self.send_message)
        send_button.pack(pady=5)

        self.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        """Handles user input and AI response"""
        user_text = self.entry.get().strip()
        if user_text:
            self.chat_history.config(state="normal")
            self.chat_history.insert(tk.END, f"You: {user_text}\n", "user")
            self.chat_history.config(state="disabled")
            self.chat_history.see(tk.END)

            system_prompt = (
                "You are an expert programming assistant. You only answer coding-related questions."
                " Format all code inside triple backticks (` ``` `). Keep responses short."
            )
            full_prompt = f"{system_prompt}\nUser: {user_text}\nAI:"

            response = self.model.invoke(full_prompt)

            self.chat_history.config(state="normal")
            self.chat_history.insert(tk.END, f"AI: {response}\n\n", "ai")
            self.chat_history.config(state="disabled")
            self.chat_history.see(tk.END)

            self.entry.delete(0, tk.END)
            self.entry.focus()

if __name__ == "__main__":
    app = ChatBotApp()
    app.mainloop()
