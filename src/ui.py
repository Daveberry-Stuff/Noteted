import customtkinter as ctk
import tkinter as tk
import git
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
    
    left_container = ctk.CTkFrame(root, fg_color="transparent")
    left_container.pack(side="left", fill="y", padx=10, pady=10)

    sidebar_frame = sidebar(left_container)
    listFiles(sidebar_frame)
    gitCommits(left_container)
    textbox(root)
    dcRPC(root)

    root.mainloop()

if __name__ == "__main__":
    initialize_ui()

def sidebar(parent):
    sidebar = ctk.CTkFrame(parent, width=200, height=400, corner_radius=10,
                           fg_color="#1e1e1e")
    sidebar.pack(pady=0, padx=0, side="top", fill="x")
    sidebar.pack_propagate(False)
    return sidebar

def gitCommits(parent):
    errorMessage = ""
    commits = []

    try:
        repo = git.Repo(os.path.dirname(os.path.dirname(__file__)))
        commits = list(repo.iter_commits('main', max_count=5))
    except Exception as e:
        commits = []
        errorMessage = "Error fetching commits"

    commitFrame = ctk.CTkFrame(parent, width=200, corner_radius=10,
                                fg_color="#1e1e1e")
    commitFrame.pack(pady=10, padx=0, side="top", fill="both", expand=True)

    label = ctk.CTkLabel(commitFrame, text="Recent Commits", font=("Arial", 16))
    label.pack(pady=10)

    if not commits:
        commitMessage = ctk.CTkLabel(commitFrame, text=str(errorMessage), font=("Arial", 12), wraplength=180)
        commitMessage.pack(pady=5)
    else:
        for commit in commits:
            commitFrame = ctk.CTkFrame(commitFrame, fg_color="transparent")
            commitFrame.pack(fill="x", pady=5, padx=10)

            commitMessage = ctk.CTkLabel(commitFrame, text=str(commit.message.strip()), font=("Arial", 12), wraplength=180, justify="left")
            commitMessage.pack(anchor="w")

            dateString = commit.authored_datetime.strftime("%Y-%m-%d %H:%M")
            commitDate = ctk.CTkLabel(commitFrame, text=str(dateString), font=("Arial", 10), text_color="gray")
            commitDate.pack(anchor="w", pady=(0, 5))


def textbox(root):
    writingbox = ctk.CTkTextbox(root, width=400, height=300, corner_radius=10,
                                fg_color="#1e1e1e", font=("Arial", 14))
    writingbox.pack(pady=10, padx=10, expand=True, fill="both")

def listFiles(part):
    notes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notes')
    if os.path.exists(notes_dir):
        for file_name in os.listdir(notes_dir):
            if file_name.endswith((".md", ".td")):
                button = ctk.CTkButton(part, text=file_name)
                button.pack(pady=5, padx=10, fill="x")

def dcRPC(root):
    client_id = "1415709453898092692"
    rpc_manager = dcPresence.startRPC(client_id)

    def closing():
        if rpc_manager:
            rpc_manager.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", closing)