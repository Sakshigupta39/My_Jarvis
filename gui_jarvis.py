import tkinter as tk
import threading
from main import run_jarvis
import sys
import tkinter as tk
from PIL import Image, ImageTk

class StdoutRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass  


def start_jarvis():
    output_box.insert(tk.END, "🎤 Listening...\n")
    output_box.see(tk.END)
    threading.Thread(target=run_jarvis).start()

#UI setup
root = tk.Tk()
root.title("JARVIS - Voice Assistant")
root.geometry("800x600")
root.configure(bg="#000000")


#Header
header = tk.Label(root, text="JARVIS AI", font=("Consolas", 28, "bold"), fg="cyan", bg="#0a0a0a")
header.pack(pady=20)

#Output box
output_box = tk.Text(root, height=20, width=55, bg="#1a1a1a", fg="white", font=("Consolas", 12))
output_box.pack(pady=20)
output_box.insert(tk.END, ">> Welcome! Click the mic to start JARVIS...\n")

sys.stdout = StdoutRedirector(output_box)

#Mic button
mic_button = tk.Button(root, text="🎤 Start Listening", font=("Arial", 14), bg="cyan", fg="black",
                       command=start_jarvis, relief="flat", padx=20, pady=10)
mic_button.pack(pady=10)

#Exit button
exit_button = tk.Button(root, text="❌ Exit", font=("Arial", 12), bg="red", fg="white",
                        command=root.destroy, relief="flat")
exit_button.pack(pady=10)

root.mainloop()
