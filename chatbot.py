import datetime
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from gpt4all import GPT4All

# =========================================================
# LOAD AI MODEL
# =========================================================
# Pro-Tip: Loading large models can freeze the window startup. 
# For an assignment, keep it global or load it behind a loading screen.
try:
    chatbot = GPT4All(
        model_name="orca-mini-3b-gguf2-q4_0.gguf",
        model_path=".",
        allow_download=False,
        device="cpu"
    )
except Exception as e:
    print(f"Model initialization failed: {e}")
    chatbot = None

# =========================================================
# WINDOW SETUP
# =========================================================
root = tk.Tk()
root.title("Offline AI Chatbot")
root.geometry("1000x750")
root.configure(bg="#121212")

dark_mode = True

# =========================================================
# THEME TOGGLE OPTIMIZATION
# =========================================================
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    
    # Using dictionaries keeps styling clean and scalable instead of messy chains of .config()
    theme = {
        "root_bg": "#121212" if dark_mode else "#f0f0f0",
        "title_fg": "#00ffff" if dark_mode else "#0000aa",
        "input_bg": "#2b2b2b" if dark_mode else "white",
        "input_fg": "white" if dark_mode else "black",
        "chat_bg": "#1e1e1e" if dark_mode else "white",
        "chat_fg": "white" if dark_mode else "black",
        "insert_color": "white" if dark_mode else "black"
    }

    root.configure(bg=theme["root_bg"])
    title.config(bg=theme["root_bg"], fg=theme["title_fg"])
    top_frame.config(bg=theme["root_bg"])
    input_frame.config(bg=theme["root_bg"])
    
    user_input.config(bg=theme["input_bg"], fg=theme["input_fg"], insertbackground=theme["insert_color"])
    chat_area.config(bg=theme["chat_bg"], fg=theme["chat_fg"], insertbackground=theme["insert_color"])

# =========================================================
# GUI COMPONENT LAYOUT
# =========================================================
title = tk.Label(root, text="OFFLINE AI CHATBOT", font=("Arial", 24, "bold"), bg="#121212", fg="#00ffff")
title.pack(pady=10)

top_frame = tk.Frame(root, bg="#121212")
top_frame.pack(fill=tk.X, padx=10)

# UI Elements
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 13), bg="#1e1e1e", fg="white", insertbackground="white")
chat_area.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

# Define Custom Text Tags for clean handling of dynamic lines
chat_area.tag_config("typing", foreground="#ffaa00") 
chat_area.insert(tk.END, "🤖 Bot: Hello! I am your Offline AI Assistant.\n\n")

input_frame = tk.Frame(root, bg="#121212")
input_frame.pack(fill=tk.X, padx=10, pady=10)

user_input = tk.Entry(input_frame, font=("Arial", 14), bg="#2b2b2b", fg="white", insertbackground="white")
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)

# =========================================================
# CORE FUNCTIONS (THINK THREAD-SAFETY!)
# =========================================================

def append_to_chat(text, tag=None):
    """Safe helper function to modify Tkinter text space from any thread."""
    chat_area.config(state=tk.NORMAL)
    if tag:
        chat_area.insert(tk.END, text, tag)
    else:
        chat_area.insert(tk.END, text)
    chat_area.config(state=tk.DISABLED) # Prevents user from manually typing inside chat area
    chat_area.yview(tk.END)

def remove_typing_status():
    """Removes the typing status text safely using targeted indexing."""
    chat_area.config(state=tk.NORMAL)
    # Search for our custom tagged string block and drop it out cleanly
    ranges = chat_area.tag_ranges("typing")
    if ranges:
        chat_area.delete(ranges[0], ranges[1])
    chat_area.config(state=tk.DISABLED)

def save_chat():
    content = chat_area.get("1.0", tk.END)
    file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", "Chat saved successfully!")

def clear_chat():
    chat_area.config(state=tk.NORMAL)
    chat_area.delete("1.0", tk.END)
    chat_area.config(state=tk.DISABLED)
    append_to_chat("🤖 Bot: Chat cleared successfully.\n\n")

# =========================================================
# ASYNCHRONOUS BACKEND PROCESSING
# =========================================================

def process_message_worker(message, timestamp):
    """Runs inside background thread. No direct Tkinter manipulation here!"""
    if not chatbot:
        root.after(0, remove_typing_status)
        root.after(0, lambda: append_to_chat("❌ Error: AI Model was not initialized properly.\n\n"))
        return

    try:
        # Generates AI response safely off-screen
        response = chatbot.generate(
            prompt=message,
            max_tokens=200,
            temp=0.7
        )
        
        # Scheduling safely back onto main Tkinter UI thread loops using root.after
        root.after(0, remove_typing_status)
        root.after(0, lambda: append_to_chat(f"🤖 Bot [{timestamp}]: {response}\n\n"))
        
    except Exception as e:
        root.after(0, remove_typing_status)
        root.after(0, lambda: append_to_chat(f"❌ Error during generation:\n{e}\n\n"))

def send_message():
    message = user_input.get().strip()
    if not message: 
        return # Optimization: Instantly drops out before waking up thread cycles unnecessarily
        
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Process immediate GUI updates on main thread
    append_to_chat(f"🧑 You [{timestamp}]: {message}\n\n")
    append_to_chat("🤖 Bot is typing...\n\n", tag="typing")
    user_input.delete(0, tk.END)
    
    # Pass off heavy computational lifting safely to daemon thread
    threading.Thread(
        target=process_message_worker,
        args=(message, timestamp),
        daemon=True
    ).start()

# =========================================================
# BUTTONS & BINDINGS
# =========================================================
theme_button = tk.Button(top_frame, text="Toggle Theme", font=("Arial", 11, "bold"), bg="#444", fg="white", command=toggle_theme)
theme_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(top_frame, text="Clear Chat", font=("Arial", 11, "bold"), bg="#aa0000", fg="white", command=clear_chat)
clear_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(top_frame, text="Save Chat", font=("Arial", 11, "bold"), bg="#0066cc", fg="white", command=save_chat)
save_button.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(input_frame, text="Send", font=("Arial", 12, "bold"), bg="#00aa00", fg="white", width=12, command=send_message)
send_button.pack(side=tk.RIGHT)

root.bind("<Return>", lambda event: send_message())

# Initialize text widget settings
chat_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root.mainloop()