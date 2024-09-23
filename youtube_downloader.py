import tkinter as tk
from tkinter import messagebox
import yt_dlp
import sys
import traceback

# Function to redirect print statements to the text widget
class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Scroll to the end

    def flush(self):
        pass

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Input Error", "Please enter a YouTube URL")
        return

    ydl_opts = {
        'format': 'best[height<=720]',
        'outtmpl': './%(title)s.%(ext)s',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            messagebox.showinfo("Success", f"Video '{video_title}' downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        # Print the traceback to the text widget for debugging
        traceback.print_exc()

# Set up the main application window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create and place the URL input field
url_label = tk.Label(root, text="YouTube URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Create and place the download button
download_button = tk.Button(root, text="Download Video", command=download_video)
download_button.pack(pady=10)

# Create a text widget to display console logs
log_text = tk.Text(root, height=10, width=60)
log_text.pack(pady=5)

# Redirect stdout to the text widget
sys.stdout = RedirectText(log_text)

# Run the application
root.mainloop()
