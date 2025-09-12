import customtkinter as ctk
import tkinter as tk
import os
from tkinter import filedialog, messagebox
from PIL import Image
import src.discord as dcPresence
import markdown2
from tkhtmlview import HTMLLabel
import src.settings as settingsUI
import src.getFromJSON as getJson

def initializeUI():
    root = ctk.CTk()
    root.title("Noteted")
    root.geometry("1280x720")
    root.minsize(800, 600)
    root.iconbitmap(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'NTD.ico'))
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # say hi to sidebarFrame because it's here to fix the FUCKING aligment :333
    sidebarFrame = sidebar(root)
    writingBox2 = textbox(root)
    previewBox2 = previewbox(root)
    if getJson.getSetting("EnableDiscordRPC"):
        print("Discord RPC is enabled in settings! Initializing...")
        dcRPC(root)
    else:
        print("Discord RPC is disabled in settings")

    # shout out to my boy gemini 2.4 pro and flash for this function!!!
    def updatePreview(event=None):
        markdownText = writingBox2.get("1.0", tk.END)
        HTMLtext = markdown2.markdown(markdownText, extras=["fenced-code-blocks", "strike"])

        # WACKy way to do it since there's no other way to do so--
        tags2style = ["<p>", "<h1>", "<h2>", "<h3>", "<h4>", "<h5>", "<h6>", "<li>", "<strong>", "<em>", "<a>", "<s>"]
        for tag in tags2style: 
            HTMLtext = HTMLtext.replace(tag, tag[:-1] + ' style="color:white;">')
        
        HTMLtext = HTMLtext.replace('<pre>', '<pre style="background-color:#2b2b2b; padding:10px; border-radius:4px;">')
        HTMLtext = HTMLtext.replace('<code>', '<code style="color:white;">')

        previewBox2.set_html(HTMLtext)

    listFiles(sidebarFrame, writingBox2, updatePreview)
    writingBox2.bind("<KeyRelease>", updatePreview)
    root.mainloop()

if __name__ == "__main__":
    initializeUI()

def optionsFunc():
    settingsUI.initializeSettingsUI()

def newFile():
    print("New File")

def sidebar(root):
    sidebar = ctk.CTkFrame(root, width=200, corner_radius=10,
                           fg_color="#1e1e1e")
    sidebar.pack(pady=10, padx=10, side="left", fill="both")
    sidebar.pack_propagate(False)

    buttonFrame = ctk.CTkFrame(sidebar, fg_color="transparent")
    buttonFrame.pack(pady=10, padx=10, fill="x")

    optionsButton = ctk.CTkButton(buttonFrame, text="Options", command=optionsFunc, width=85)
    optionsButton.pack(side="left", expand=True, padx=(0, 5))

    newFileButton = ctk.CTkButton(buttonFrame, text="New File", command=newFile, width=85)
    newFileButton.pack(side="left", expand=True, padx=(5, 0))
    
    return sidebar

def textbox(root):
    writingbox = ctk.CTkTextbox(root, width=400, height=300, corner_radius=10,
                                fg_color="#1e1e1e", font=("Arial", 14))
    writingbox.pack(pady=10, padx=0, expand=True, fill="both", side="left")
    return writingbox

def previewbox(root):
    previewContainer = ctk.CTkFrame(root, corner_radius=10, fg_color="#1e1e1e")
    previewContainer.pack(pady=10, padx=10, expand=True, fill="both", side="right")

    previewBox = HTMLLabel(previewContainer, background='#1e1e1e')
    previewBox.pack(expand=True, fill="both", padx=5, pady=5)

    return previewBox

# again, ai because I don't feel like figuring out how to do this myself :3
def listFiles(part, writingBox, updatePreview):
    notesDirectory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test-notes')
    if os.path.exists(notesDirectory):
        for fileName in os.listdir(notesDirectory):
            if fileName.endswith((".md", ".td", ".txt")):
                filePath = os.path.join(notesDirectory, fileName)
                def load_file_content(path=filePath):
                    with open(path, "r") as file:
                        content = file.read()
                    writingBox.delete("1.0", tk.END)
                    writingBox.insert("1.0", content)
                    updatePreview()
                button = ctk.CTkButton(part, text=fileName, command=load_file_content)
                button.pack(pady=5, padx=10, fill="x")
                print(f"Loaded file: {fileName}")
    else:
        print("Notes directory not found, creating one...")
        os.makedirs(notesDirectory)

def dcRPC(root):
    RPCclientID = "1415709453898092692"
    RPCmanager = dcPresence.startRPC(RPCclientID)

    def closing():
        if RPCmanager:
            RPCmanager.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", closing)