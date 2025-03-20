# -*- coding: utf-8 -*-
"""
@author: en_lo
"""
#%%
import yt_dlp
import os
import time
import tkinter as tk
downloaded_file = [""]
def hook(d):
    if d["status"] == "finished":
        downloaded_file[0]=d["filename"]

def download_audio(url, output_folder="audio_data", audio_format="mp3"):
    output_path = os.path.join(output_folder,"%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio",
        "extract_audio": True,
        "merge_output_format":audio_format,
        "outtmpl": output_path,
        "keepvideo":True,
        "postprocessors": [
        {
        "key": "FFmpegExtractAudio",  # Postprocessor to extract audio
        "preferredcodec": audio_format,  # Convert to desired format (e.g., mp3)
        "preferredquality": "192",  # Optionally set the audio bitrate
        }
        ],
        "progress_hooks": [hook]
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_folder

def download_video(url, output_folder="video_data",video_format="mp4"):
    output_path = os.path.join(output_folder,"%(title)s.%(ext)s")
    # "format": "bv*[height<=1080]+ba[ext=m4a]/b[ext=mp4]",
    ydl_opts = {
        "video_format":video_format,
        "format": "bv*[height<=1080]+ba[ext=m4a]/b[ext=mp4]/best",
        "outtmpl": output_path,
        "merge_output_format":video_format,
        "progress_hooks": [hook]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_folder

#%%

BASE_PATH = os.path.dirname(__file__)
AUDIO_SAVE_FOLDER = "audio_data"
AUDIO_SAVE_PATH = os.path.join(BASE_PATH,AUDIO_SAVE_FOLDER)
if not os.path.exists(AUDIO_SAVE_PATH):
    os.mkdir(AUDIO_SAVE_PATH)


VIDEO_SAVE_FOLDER = "video_data"
VIDEO_SAVE_PATH = os.path.join(BASE_PATH,VIDEO_SAVE_FOLDER)
if not os.path.exists(VIDEO_SAVE_PATH):
    os.mkdir(VIDEO_SAVE_PATH)

def open_file_explorer(path=None):
    if path is None:
        path = message_var.get()

    if os.path.exists(path):
        if os.name == "nt":  # Windows
            os.startfile(path)
        elif os.name == "posix":  # Linux, macOS. Don't support this yet, but maybe, someday
            subprocess.run(["xdg-open", path])
    else:
        print(f"The path '{path}' does not exist.")

def tk_open_video_folder():
    open_file_explorer(VIDEO_SAVE_PATH) 

def tk_open_audio_folder():
    open_file_explorer(AUDIO_SAVE_PATH)


def tk_download_audio():
    entry_link = entry.get()
    audio_button["state"] = "disabled"
    video_button["state"] = "disabled"
    message_var.set("Working...")
    try:
        output_path = download_audio(entry_link)
        dl_path = os.path.join(BASE_PATH,output_path) 
        message_var.set(dl_path)
        filename_var.set(os.path.split(downloaded_file[0])[-1].split(".")[:-1])
        print("Finished")
    except Exception as e:
        message_var.set("didn't work {}".format(e))
    audio_button["state"] = "normal"
    video_button["state"] = "normal"


def tk_download_video():
    entry_link = entry.get()
    video_button["state"] = "disabled"
    audio_button["state"] = "disabled"
    message_var.set("Working...")
    try:
        output_path = download_video(entry_link)
        dl_path = os.path.join(BASE_PATH,output_path) 
        message_var.set(dl_path)
        filename_var.set(os.path.split(downloaded_file[0])[-1].split(".")[:-1])
        print("Finished")
    except Exception as e:
        message_var.set("didn't work {}".format(e))
    audio_button["state"] = "normal"
    video_button["state"] = "normal"


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("800x400")
    window.title("YouTube Downloader")
    window.iconbitmap(os.path.join("images","logo.ico"))
    # Styling
    bg_color = "#2E3440"
    fg_color = "white"
    button_bg_color = "#BF616A"
    active_bg_color = "#A54245"
    title_font = ("Arial", 18, "bold")
    label_font = ("Arial", 14)
    entry_font = ("Arial", 12)
    button_font = ("Arial", 12, "bold")

    window.configure(bg=bg_color)  

    header_label = tk.Label(
        window,
        text="Enter/paste YouTube link:",
        font=title_font,
        bg=bg_color,
        fg=fg_color
    )
    header_label.pack(pady=10)

    entry = tk.Entry(window, width=50, font=entry_font)
    entry.pack(pady=5)

    button_frame = tk.Frame(window, bg=bg_color)
    button_frame.pack(pady=10)

    audio_button = tk.Button(
        button_frame,
        text="Download Audio",
        width=20,
        height=2,
        bg=button_bg_color,
        fg=fg_color,
        activebackground=active_bg_color,
        activeforeground=fg_color,
        font=button_font,
        relief="raised",
        bd=3,
        command=tk_download_audio,
    )
    audio_button.grid(row=0, column=0, padx=10, pady=5)

    video_button = tk.Button(
        button_frame,
        text="Download Video",
        width=20,
        height=2,
        bg="#5E81AC",
        fg="white",
        activebackground="#4C6A92",
        activeforeground=fg_color,
        font=button_font,
        relief="raised",
        bd=3,
        command=tk_download_video,
    )
    video_button.grid(row=0, column=1, padx=10, pady=5)

    folder_button_frame = tk.Frame(window, bg=bg_color)
    folder_button_frame.pack(pady=10)

    audio_folder_button = tk.Button(
        folder_button_frame,
        text="Open Audio Folder",
        font=button_font,
        width=20,
        height=2,
        bg="#88C0D0",
        fg="black",
        activebackground="#6A99A0",
        activeforeground="black",
        command=tk_open_audio_folder
    )
    audio_folder_button.grid(row=0, column=0, padx=10, pady=5)

    video_folder_button = tk.Button(
        folder_button_frame,
        text="Open Video Folder",
        font=button_font,
        width=20,
        height=2,
        bg="#88C0D0",
        fg="black",
        activebackground="#6A99A0",
        activeforeground="black",
        command=tk_open_video_folder
    )
    video_folder_button.grid(row=0, column=1, padx=10, pady=5)

    message_var = tk.StringVar()
    filename_var = tk.StringVar()

    message_label = tk.Label(
        window,
        textvariable=message_var,
        font=label_font,
        bg=bg_color,
        fg="#ECEFF4"
    )
    message_label.pack(pady=5)

    filename_label = tk.Label(
        window,
        textvariable=filename_var,
        font=label_font,
        bg=bg_color,
        fg="#ECEFF4"
    )
    filename_label.pack(pady=5)

    window.mainloop()

if __name__ == "__main__1":
    window = tk.Tk()
    window.geometry("800x400")
    window.title("YouTube Downloader")
    
    window.configure(bg="#2E3440")  # Background color

    # Styling
    label_font = ("Arial", 14)
    entry_font = ("Arial", 12)
    button_font = ("Arial", 12, "bold")

    # Title Label
    title_label = tk.Label(window, text="YouTube Downloader", font=("Arial", 18, "bold"), fg="white", bg="#2E3440")
    title_label.pack(pady=20)

    # Entry Label
    entry_label = tk.Label(window, text="Enter/paste YouTube link:", font=label_font, fg="white", bg="#2E3440")
    entry_label.pack(pady=5)

    # Entry Field
    entry = tk.Entry(window, width=50, font=entry_font, justify="center")
    entry.pack(pady=10, ipady=5)

    # Button Frame
    button_frame = tk.Frame(window, bg="#2E3440")
    button_frame.pack(pady=20)

    # Download Audio Button
    audio_button = tk.Button(
        button_frame,
        text="Download Audio",
        font=button_font,
        width=18,
        height=2,
        bg="#BF616A",
        fg="white",
        activebackground="#A54245",
        activeforeground="white",
        command=tk_download_audio,
    )
    audio_button.grid(row=0, column=0, padx=10)

    # Download Video Button
    video_button = tk.Button(
        button_frame,
        text="Download Video",
        font=button_font,
        width=18,
        height=2,
        bg="#5E81AC",
        fg="white",
        activebackground="#4C6A92",
        activeforeground="white",
        command=tk_download_video,
    )
    video_button.grid(row=0, column=1, padx=10)

    # Open Folder Button
    folder_button = tk.Button(
        window,
        text="Open Folder",
        font=button_font,
        width=12,
        height=2,
        bg="#88C0D0",
        fg="black",
        activebackground="#6A99A0",
        activeforeground="black",
        command=open_file_explorer,
    )
    folder_button.pack(pady=10)

    # Message Label
    message_var = tk.StringVar()
    message_label = tk.Label(window, textvariable=message_var, font=label_font, fg="#ECEFF4", bg="#2E3440")
    message_label.pack(pady=10)

    # Filename Label
    filename_var = tk.StringVar()
    filename_label = tk.Label(window, textvariable=filename_var, font=label_font, fg="#ECEFF4", bg="#2E3440")
    filename_label.pack()

    window.mainloop()
