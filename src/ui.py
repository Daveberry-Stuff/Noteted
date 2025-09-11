import customtkinter as ctk
import tkinter as tk
import os
from tkinter import filedialog, messagebox
from PIL import Image
import src.discord as dcPresence

def initialize_ui():
    root = ctk.CTk()
    root.title("Noteted")
    root.geometry("1280x720")
    root.minsize(800, 600)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    sidebar(root)
    textbox(root)
    dcRPC(root)

    root.mainloop()

if __name__ == "__main__":
    initialize_ui()

def optionsFunc():
    print("Options")

def newFile():
    print("New File")

def sidebar(root):
    sidebar = ctk.CTkFrame(root, width=200, corner_radius=10,
                           fg_color="#1e1e1e")
    sidebar.pack(pady=10, padx=10, side="left", fill="both")
    sidebar.pack_propagate(False)

    button_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    button_frame.pack(pady=10, padx=10, fill="x")

    optionsButton = ctk.CTkButton(button_frame, text="Options", command=optionsFunc, width=85)
    optionsButton.pack(side="left", expand=True, padx=(0, 5))

    newFileButton = ctk.CTkButton(button_frame, text="New File", command=newFile, width=85)
    newFileButton.pack(side="left", expand=True, padx=(5, 0))

    listFiles(sidebar)
    
    return sidebar

def textbox(root):
    writingbox = ctk.CTkTextbox(root, width=400, height=300, corner_radius=10,
                                fg_color="#1e1e1e", font=("Arial", 14))
    writingbox.pack(pady=10, padx=10, expand=True, fill="both")
    return writingbox

def listFiles(part):
    notes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notes')
    if os.path.exists(notes_dir):
        for file_name in os.listdir(notes_dir):
            if file_name.endswith((".md", ".td", ".txt")):
                button = ctk.CTkButton(part, text=file_name)
                button.pack(pady=5, padx=10, fill="x")
    else:
        print("Notes directory not found, creating one...")
        os.makedirs(notes_dir)

def dcRPC(root):
    client_id = "1415709453898092692"
    rpc_manager = dcPresence.startRPC(client_id)

    def closing():
        if rpc_manager:
            rpc_manager.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", closing)