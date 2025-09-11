import customtkinter as ctk
import tkinter as tk
import pygame
import requests
import git
import pypresence
import os
from tkinter import filedialog, messagebox

def initialize_ui():
    root = ctk.CTk()
    root.title("Noteted")
    root.geometry("1280x720")
    root.minsize(800, 600)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    listFiles(sidebar(root))
    textbox(root)
    root.mainloop()

if __name__ == "__main__":
    initialize_ui()

def sidebar(root):
    sidebar = ctk.CTkFrame(root, width=200, corner_radius=10,
                           fg_color="#1e1e1e")
    sidebar.pack(pady=10, padx=10, side="left", fill="y")
    return sidebar

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