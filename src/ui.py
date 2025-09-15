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
import src.render.td as td_renderer

# ===== guess by the definition =====
def initializeUI():
    root = ctk.CTk()
    root.title("Noteted")
    root.geometry("1280x720")
    root.minsize(800, 600)
    root.iconbitmap(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'NTD.ico'))
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # meow this is for the opened file background :3
    openedFileButton = {"button": None}

    # say hi to sidebarFrame AND topbarFrame because it's here to fix the FUCKING aligment :333
    topbarFrame = topbar(root)
    sidebarFrame = sidebar(root)

    mainContentFrame = ctk.CTkFrame(root, fg_color="transparent")
    mainContentFrame.pack(pady=10, padx=0, expand=True, fill="both", side="left")

    writingBox2 = textbox(mainContentFrame)
    previewContainer = previewbox(mainContentFrame)
    previewBox2 = previewContainer.label
    TDrenderFrame = createTDrender(mainContentFrame)

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

    listFiles(sidebarFrame, writingBox2, previewContainer, TDrenderFrame, updatePreview, openedFileButton)
    writingBox2.bind("<KeyRelease>", updatePreview)

    # Pass a callback to the buttons function to allow it to trigger a file list reload
    def reloadCallback():
        reloadFileList(sidebarFrame, writingBox2, previewContainer, TDrenderFrame, updatePreview, openedFileButton)

    buttons(topbarFrame, reloadCallback)
    root.mainloop()

if __name__ == "__main__":
    initializeUI()

# ===== button functions stuff =====
def funcOptionsButton():
    settingsUI.initializeSettingsUI()
    
def funcNewFileButton(reloadList):
    NTDwindow.newFile(reloadList)
    
def funcInfoButton():
    NTDwindow.info()

def funcDeleteButton():
    NTDwindow.delete()
    
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

def buttons(frame, reloadList):
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
        optionsButton = ctk.CTkButton(buttonFrame, image=optionsIcon, text="", command=funcOptionsButton, width=button_size, height=button_size)
    else:
        optionsButton = ctk.CTkButton(buttonFrame, text="Options", command=funcOptionsButton, width=85)
    optionsButton.pack(side="left", expand=False, padx=(20, 0))

    # new file
    newFileIconPath = os.path.join(base_path, 'assets', 'icons', 'buttons', 'file-plus.png')

    if os.path.exists(newFileIconPath):
        newFileIcon = ctk.CTkImage(recolorImage(newFileIconPath, color="#FFFFFF"), size=icon_size)
        newFileButton = ctk.CTkButton(buttonFrame, image=newFileIcon, text="", command=lambda: funcNewFileButton(reloadList), width=button_size, height=button_size)
    else:
        newFileButton = ctk.CTkButton(buttonFrame, text="New File", command=funcNewFileButton, width=85)
    newFileButton.pack(side="left", expand=False, padx=(20, 0))
    
    # new file
    infoIconPath = os.path.join(base_path, 'assets', 'icons', 'buttons', 'info.png')
    if os.path.exists(infoIconPath):
        infoIcon = ctk.CTkImage(recolorImage(infoIconPath, color="#FFFFFF"), size=icon_size)
        iconButton = ctk.CTkButton(buttonFrame, image=infoIcon, text="", command=funcInfoButton, width=button_size, height=button_size)
    else:
        iconButton = ctk.CTkButton(buttonFrame, text="New File", command=funcInfoButton, width=85)
    iconButton.pack(side="left", expand=False, padx=(20, 0))
    
    return buttons

def sidebar(root):
    sidebar = ctk.CTkScrollableFrame(root, width=200, corner_radius=10,
                           fg_color="#1e1e1e")
    sidebar.pack(pady=10, padx=10, side="left", fill="both")
    
    return sidebar

def textbox(parent):
    writingbox = ctk.CTkTextbox(parent, width=400, height=300, corner_radius=10,
                                fg_color="#1e1e1e", font=("Arial", 14))
    writingbox.pack(padx=(0, 10), side="left", fill="both", expand=True)
    return writingbox

def previewbox(parent):
    previewContainer = ctk.CTkFrame(parent, corner_radius=10, fg_color="#1e1e1e")
    previewBox = HTMLLabel(previewContainer, background='#1e1e1e')
    previewBox.pack(expand=True, fill="both", padx=5, pady=5)
    previewContainer.label = previewBox
    return previewContainer

def createTDrender(parent):
    td_renderer_container = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    return td_renderer_container

def reloadFileList(sidebarFrame, writingBox, previewContainer, TDrenderFrame, updatePreview, openedFileButton):
    for widget in sidebarFrame.winfo_children():
        widget.destroy()
    listFiles(sidebarFrame, writingBox, previewContainer, TDrenderFrame, updatePreview, openedFileButton)

# again, gemini because I don't feel like figuring out how to do this myself :3
def listFiles(part, writingBox, previewContainer, TDrenderFrame, updatePreview, openedFileButton):
    notesDirectory = getJson.getSetting("NotesDirectory")
    if not os.path.exists(notesDirectory):
        print("Notes directory not found, creating one...")
        os.makedirs(notesDirectory)

    for fileName in os.listdir(notesDirectory):
        if fileName.endswith((".md", ".td", ".txt")):
            filePath = os.path.join(notesDirectory, fileName)
            button = ctk.CTkButton(part, text=fileName, fg_color="transparent", hover_color="#555555")

            def loadFileContent(path=filePath, btn=button):
                if openedFileButton["button"]:
                    openedFileButton["button"].configure(fg_color="transparent")

                btn.configure(fg_color="#2b2b2b")
                openedFileButton["button"] = btn

                with open(path, "r", encoding='utf-8') as file:
                    content = file.read()
                
                # Always update the textbox content
                writingBox.delete("1.0", tk.END)
                writingBox.insert("1.0", content)

                # Forget all main content widgets before packing new layout
                writingBox.pack_forget()
                previewContainer.pack_forget()
                TDrenderFrame.pack_forget()

                if path.endswith(".md"):
                    # .md: editor | preview
                    writingBox.pack(pady=0, padx=0, expand=True, fill="both", side="left")
                    previewContainer.pack(pady=0, padx=10, expand=True, fill="both", side="right")
                    updatePreview()
                elif path.endswith(".txt"):
                    # .txt: editor only
                    writingBox.pack(pady=0, padx=(0, 10), expand=True, fill="both", side="left")
                elif path.endswith(".td"):
                    # .td: renderer only
                    for widget in TDrenderFrame.winfo_children():
                        widget.destroy()
                    renderer = td_renderer.TodoRenderer(TDrenderFrame, content, path)
                    renderer.pack(expand=True, fill="both")
                    TDrenderFrame.pack(pady=0, padx=(0, 10), expand=True, fill="both", side="left")
                
            button.configure(command=loadFileContent)
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
