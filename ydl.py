# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 20:32:32 2023

@author: en_lo
"""

from pytube import YouTube
from pytube import Playlist
import os
import time
import json
import tkinter as tk


BASE_PATH = os.path.dirname(__file__)
SAVE_FOLDER = "data"
SAVE_PATH = os.path.join(BASE_PATH,SAVE_FOLDER)
if not os.path.exists(os.path.join(BASE_PATH,SAVE_FOLDER)):
    os.mkdir(os.path.join(BASE_PATH,SAVE_FOLDER))

ALREADY_DOWNLOADED = set(os.listdir(SAVE_PATH))

def load_local_library():
    with open("local_library.json","r") as infile:
        return json.load(infile)

def save_local_library(local_library):
    with open("local_library.json","w") as outfile:
        outfile.write(json.dumps(local_library,indent=4))
   
def purge_title_not_found(local_library):
    for key in local_library:
        #TODO remove elements in local library that doesn't have a filename
        pass

def download_audio(link):
    check_link_name(link)
    if LOCAL_LIBRARY[link] not in ALREADY_DOWNLOADED:
        print("downloading")
        stream = YouTube(link).streams.filter(only_audio=True).first()
        return stream.download(SAVE_PATH)
    else:
        return LOCAL_LIBRARY[link]
    
        
def download_playlist_audio(playlist_link):
    pass

def check_link_name(link):
    if link not in LOCAL_LIBRARY:
        print("checking name")
        LOCAL_LIBRARY[link] = YouTube(link).streams.filter(only_audio=True).first().default_filename
        save_local_library(LOCAL_LIBRARY)
        print(link,LOCAL_LIBRARY[link])
        return LOCAL_LIBRARY[link]
    else:
        return False

def get_playlist_names(playlist_link):
    pass


def tk_download_audio():
    entry_link = entry.get()
    button["state"] = "disabled"
    message_var.set("Working...")
    try:
        dl_name = download_audio(entry_link)
        message_var.set("downloaded {}".format(dl_name))
    except Exception as e:
        message_var.set("didn't work {}".format(e))
    button["state"] = "normal"


LOCAL_LIBRARY = load_local_library()


# playlist_link = "https://www.youtube.com/playlist?list=PLnCX3UVVIsLegTE-J3eJnjBuQ5Zu_e1nX"
# yt_playlist = Playlist(playlist_link)

# for link in yt_playlist:
#     try:
#         check_link_name(link)
#         download_audio(link)
#         ALREADY_DOWNLOADED = set(os.listdir(SAVE_PATH))
#     except Exception as e:
#         print("title not found",e)

save_local_library(LOCAL_LIBRARY)        

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("800x200")
    tk.Label(text="Enter/paste youtube link").pack()
    entry = tk.Entry(width=50)
    entry.pack()
    button = tk.Button(
    text="Download Audio",
    width=25,
    height=5,
    bg="red",
    fg="white",
    command=tk_download_audio,
    )
    button.pack()
    message_var = tk.StringVar()
    message_label = tk.Label(textvariable = message_var).pack()
    window.mainloop()
    # link = "https://www.youtube.com/watch?v=BCnJAMkETiU"
    # try:
    #     yt = YouTube(link)
    # except Exception as e:
    #     print("oops",e)
        
    # stream = yt.streams.filter(only_audio=True).first()
    # #stream.download()

