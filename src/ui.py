import customtkinter as ctk
import tkinter as tk
import os
from tkinter import filedialog, messagebox
from PIL import Image
import src.discord as dcPresence
import markdown2
from tkhtmlview import HTMLLabel

def initialize_ui():
    root = ctk.CTk()
    root.title("Noteted")
    root.geometry("1280x720")
    root.minsize(800, 600)
    root.iconbitmap(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'NTD.ico'))
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    sidebar(root)
    writingBox2 = textbox(root)
    previewBox2 = previewbox(root)
    dcRPC(root)

    # also before you ask, yes I did use ai to make this function
    # now stop fucking bullying me about it
    def updatePreview(event=None):
        markdownText = writingBox2.get("1.0", tk.END)
        HTMLtext = markdown2.markdown(markdownText, extras=["fenced-code-blocks", "strike"])

        # there's like no other way to make it white so this is the most optimal solution
        tags2style = ["<p>", "<h1>", "<h2>", "<h3>", "<h4>", "<h5>", "<h6>", "<li>", "<strong>", "<em>", "<a>", "<s>"]
        for tag in tags2style: 
            HTMLtext = HTMLtext.replace(tag, tag[:-1] + ' style="color:white;">')
        
        HTMLtext = HTMLtext.replace('<pre>', '<pre style="background-color:#2b2b2b; padding:10px; border-radius:4px;">')
        HTMLtext = HTMLtext.replace('<code>', '<code style="color:white;">')

        previewBox2.set_html(HTMLtext)

    writingBox2.bind("<KeyRelease>", updatePreview)
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
    writingbox.pack(pady=10, padx=0, expand=True, fill="both", side="left")
    return writingbox

def previewbox(root):
    preview_container = ctk.CTkFrame(root, corner_radius=10, fg_color="#1e1e1e")
    preview_container.pack(pady=10, padx=10, expand=True, fill="both", side="right")

    previewboxed = HTMLLabel(preview_container, background='#1e1e1e')
    previewboxed.pack(expand=True, fill="both", padx=5, pady=5)

    return previewboxed

def listFiles(part):
    notes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test-notes')
    if os.path.exists(notes_dir):
        for file_name in os.listdir(notes_dir):
            if file_name.endswith((".md", ".td", ".txt")):
                button = ctk.CTkButton(part, text=file_name)
                button.pack(pady=5, padx=10, fill="x")
                print(f"Loaded file: {file_name}")
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