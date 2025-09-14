import customtkinter as ctk
import tkinter as tk
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageColor
import src.discord as dcPresence
import markdown2
from tkhtmlview import HTMLLabel
import src.settings as settingsUI
import src.getFromJSON as getJson
import src.NTDwindow as NTDwindow

# ===== guess by the definition =====
def initializeUI():
    root = ctk.CTk()
    root.title("Noteted")
    root.geometry("1280x720")
    root.minsize(800, 600)
    root.iconbitmap(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'NTD.ico'))
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.eval('tk::PlaceWindow . center')

    # say hi to sidebarFrame AND topbarFrame because it's here to fix the FUCKING aligment :333
    topbarFrame = topbar(root)
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
    buttons(topbarFrame)
    root.mainloop()

if __name__ == "__main__":
    initializeUI()

# ===== button functions stuff =====
def optionsFunc():
    settingsUI.initializeSettingsUI()

def newFile():
    NTDwindow.newfile.window()
    
# ===== other ui stuff =====
# thanks gemini code assist! you're great :3
def recolorImage(image_path, color="#FFFFFF"):
    try:
        img = Image.open(image_path).convert("RGBA")
    except FileNotFoundError:
        return None

    color_img = Image.new("RGB", img.size, ImageColor.getrgb(color))
    img.paste(color_img, (0, 0), mask=img.split()[3])
    return img

def topbar(root):
    topbar = ctk.CTkFrame(root, height=50, width=400, corner_radius=0, fg_color="#1e1e1e")
    topbar.pack(side="top", fill="x")
    topbar.pack_propagate(False)

    return topbar

def buttons(frame):
    # icon buttons with text fallback meow :3
    base_path = os.path.dirname(os.path.dirname(__file__))
    icon_size = (20, 20)
    button_size = 30
    
    buttonFrame = ctk.CTkFrame(frame, fg_color="transparent")
    buttonFrame.pack(pady=10, padx=10, fill="x")

    # options
    optionsIconPath = os.path.join(base_path, 'assets', 'icons', 'buttons', 'tool.png')
    if os.path.exists(optionsIconPath):
        optionsIcon = ctk.CTkImage(recolorImage(optionsIconPath, color="#FFFFFF"), size=icon_size)
        optionsButton = ctk.CTkButton(buttonFrame, image=optionsIcon, text="", command=optionsFunc, width=button_size, height=button_size)
    else:
        optionsButton = ctk.CTkButton(buttonFrame, text="Options", command=optionsFunc, width=85)
    optionsButton.pack(side="left", expand=False, padx=20)

    # new file
    newFileIconPath = os.path.join(base_path, 'assets', 'icons', 'buttons', 'file-plus.png')
    if os.path.exists(newFileIconPath):
        newFileIcon = ctk.CTkImage(recolorImage(newFileIconPath, color="#FFFFFF"), size=icon_size)
        newFileButton = ctk.CTkButton(buttonFrame, image=newFileIcon, text="", command=newFile, width=button_size, height=button_size)
    else:
        newFileButton = ctk.CTkButton(buttonFrame, text="New File", command=newFile, width=85)
    newFileButton.pack(side="left", expand=False, padx=0)
    
    return buttons

def sidebar(root):
    sidebar = ctk.CTkFrame(root, width=200, corner_radius=10,
                           fg_color="#1e1e1e")
    sidebar.pack(pady=10, padx=10, side="left", fill="both")
    sidebar.pack_propagate(False)
    
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

# again, gemini because I don't feel like figuring out how to do this myself :3
def listFiles(part, writingBox, updatePreview):
    notesDirectory = getJson.getSetting("NotesDirectory")
    if not os.path.exists(notesDirectory):
        print("Notes directory not found, creating one...")
        os.makedirs(notesDirectory)

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

# ===== el funny discord rpc =====
def dcRPC(root):
    RPCclientID = "1415709453898092692"
    RPCmanager = dcPresence.startRPC(RPCclientID)

    def closing():
        if RPCmanager:
            RPCmanager.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", closing)