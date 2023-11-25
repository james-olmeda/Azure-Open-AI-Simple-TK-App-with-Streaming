import tkinter as tk  # Import the tkinter library for creating a graphical user interface (GUI)
from tkinter.font import Font  # Import the Font class from tkinter for customizing fonts
import threading  # Import the threading module for running tasks concurrently
from completion import Completion  # Import the Completion class from the mygpt module

# Define a class for the chat application
class Chat:
    def __init__(self):
        # Create the main GUI window
        self.main_window = tk.Tk()
        self.main_window.title("Chat")  # Set the window title to "Chat"
        self.main_window.geometry("600x600")  # Set the window size to 600x600 pixels

        # Define a custom font for the chat text
        self.chat_font = Font(family="Helvetica", size=16)

        # Create a Text widget to display chat messages
        self.chat_window = tk.Text(self.main_window, state=tk.DISABLED, wrap=tk.WORD, font=self.chat_font)
        self.chat_window.tag_configure('right', justify='right')
        self.chat_window.tag_configure('left',  justify='left')
        self.chat_window.pack(padx=10, pady=10, expand=True, fill='both')

        # Create an Entry widget for user input
        self.entry = tk.Entry(self.main_window, width=30)
        self.entry.pack(padx=10, pady=10, fill='x', expand=True)
        self.entry.bind("<Return>", self.send_message)  # Bind the "Return" key to the send_message method

        # Create a "Send" button and associate it with the send_message method
        self.send_button = tk.Button(self.main_window, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10, side='right')

    # Method to fetch GPT responses for user messages
    def fetch_gpt_response(self, user_message):
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"\n\nGPT: ", 'left')
        self.chat_window.config(state=tk.DISABLED)
        for partial_response in Completion.gptResponse(user_message):
            self.main_window.after(0, self.update_chat_window, partial_response, True)

        self.main_window.after(0, self.update_chat_window, "\n\n", True)

    # Method to update the chat window with messages
    def update_chat_window(self, response, append=False):
        self.chat_window.config(state=tk.NORMAL)

        if append:
            self.chat_window.insert(tk.END, response)
        else:
            self.chat_window.insert(tk.END, f"\n\nGPT: {response}\n\n", 'left')
        self.chat_window.config(state=tk.DISABLED)

    # Method to send user messages and trigger GPT response fetching
    def send_message(self, event=None):
        user_message = self.entry.get()
        if user_message:
            self.chat_window.config(state=tk.NORMAL)
            self.chat_window.insert(tk.END, f"\n\nUser: {user_message}  \n\n", 'right')
            self.chat_window.config(state=tk.DISABLED)
            self.entry.delete(0, tk.END)
            threading.Thread(target=self.fetch_gpt_response, args=(user_message,)).start()

    # Method to run the chat application
    def run(self):
        self.main_window.mainloop()
