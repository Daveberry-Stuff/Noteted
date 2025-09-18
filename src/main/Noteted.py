import customtkinter as ctk
import tkinter as tk
import os
import sys
import time
from tkinter import filedialog, messagebox
from PIL import Image, ImageColor
import src.backend.discord as dcPresence
import src.backend.getFromJSON as getJson
import src.main.NTDwindow as NTDwindow
import src.renderers.todo as tdRenderer
import src.renderers.markdown as markdownRenderer
import src.renderers.text as textRenderer
import src.handler.path as pathHandler
import src.handler.saving as savingHandler
import src.handler.theme as themeHandler

# ===== guess by the definition =====
def initializeUI():
    root = ctk.CTk()
    root.title("Noteted")
    root.geometry("1280x720")
    root.minsize(800, 600)
    root.configure(fg_color=themeHandler.getThemePart("background"))
    ctk.set_appearance_mode(themeHandler.getThemePart("WPM"))
    ctk.set_default_color_theme(themeHandler.getThemePart("DCT"))

    baseDirectory = pathHandler.mainPath()
    if sys.platform == "win32":
        iconPath = os.path.join(baseDirectory, 'assets', 'NTD.ico')
        if os.path.exists(iconPath):
            root.iconbitmap(iconPath)
    else:
        iconPath = os.path.join(baseDirectory, 'assets', 'NTD.png')
        if os.path.exists(iconPath):
            root.iconphoto(False, tk.PhotoImage(file=iconPath))

    # meow this is for the opened file background :3
    openedFileButton = {"button": None}

    # say hi to sidebarFrame AND topbarFrame because it's here to fix the FUCKING aligment :333
    topbarFrame = topbar(root)
    sidebarFrame = sidebar(root)

    mainContentFrame = ctk.CTkFrame(root, fg_color="transparent")
    mainContentFrame.pack(pady=10, padx=0, expand=True, fill="both", side="left")

    writingBox2 = textbox(mainContentFrame)
    previewContainer = markdownRenderer.previewbox(mainContentFrame)
    previewBox2 = previewContainer.label # type: ignore
    TDrenderFrame = createTDrender(mainContentFrame)

    saver = savingHandler.Saver()

    if getJson.getSetting("EnableDiscordRPC"):
        print("Discord RPC is enabled in settings! Initializing...")
        dcRPC(root, saver)
    else:
        print("Discord RPC is disabled in settings")


    def closing():
        if pathHandler.getSetting("EnableDiscordRPC"):
            # hey dw about this it's just to make sure it stops properly
            # don't ask why it actually fuckign works
            for meow in range(15):
                break
        saver.stop()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", closing)

    def updatePreviewWrapper(event=None):
        markdownRenderer.updatePreview(writingBox2, previewBox2)

    listFiles(sidebarFrame, writingBox2, previewContainer, TDrenderFrame, updatePreviewWrapper, openedFileButton, saver)
    writingBox2.bind("<KeyRelease>", updatePreviewWrapper)

    def reloadCallback():
        reloadFileList(sidebarFrame, writingBox2, previewContainer, TDrenderFrame, updatePreviewWrapper, openedFileButton, saver)

    bindKeybinds(root, reloadCallback, updatePreviewWrapper, saver)

    buttons(topbarFrame, reloadCallback, root)
    root.mainloop()    

if __name__ == "__main__":
    initializeUI()

# ===== button functions stuff =====
def funcOptionsButton(root):
    NTDwindow.settings(root)
    
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
    topbar = ctk.CTkFrame(root, height=50, width=400, corner_radius=0, fg_color=themeHandler.getThemePart("frame"))
    topbar.pack(side="top", fill="x")
    topbar.pack_propagate(False)

    return topbar

def buttons(frame, reloadList, root):
    # icon buttons with text fallback meow :3
    iconSize = (20, 20)
    buttonSize = 30
    
    buttonFrame = ctk.CTkFrame(frame, fg_color="transparent")
    buttonFrame.pack(pady=10, padx=10, fill="x")

    # options
    optionsIconPath = pathHandler.iconsPath("buttons", "tool.png")
    if os.path.exists(optionsIconPath): # type: ignore
        optionsIcon = ctk.CTkImage(recolorImage(optionsIconPath, color="#FFFFFF"), size=iconSize) # type: ignore
        optionsButton = ctk.CTkButton(buttonFrame, image=optionsIcon, text="", command=lambda: funcOptionsButton(root), width=buttonSize, height=buttonSize)
    else:
        optionsButton = ctk.CTkButton(buttonFrame, text="Options", command=lambda: funcOptionsButton(root), width=85, text_color=themeHandler.getThemePart("text")) # type: ignore
    optionsButton.pack(side="left", expand=False, padx=(20, 0))

    # new file
    newFileIconPath = pathHandler.iconsPath("buttons", "file-plus.png")
    if os.path.exists(newFileIconPath): # type: ignore
        newFileIcon = ctk.CTkImage(recolorImage(newFileIconPath, color="#FFFFFF"), size=iconSize) # type: ignore
        newFileButton = ctk.CTkButton(buttonFrame, image=newFileIcon, text="", command=lambda: funcNewFileButton(reloadList), width=buttonSize, height=buttonSize)
    else:
        newFileButton = ctk.CTkButton(buttonFrame, text="New File", command=funcNewFileButton, width=85, text_color=themeHandler.getThemePart("text")) # type: ignore
    newFileButton.pack(side="left", expand=False, padx=(20, 0))
    
    # info
    infoIconPath = pathHandler.iconsPath("buttons", "info.png")
    if os.path.exists(infoIconPath): # type: ignore
        infoIcon = ctk.CTkImage(recolorImage(infoIconPath, color="#FFFFFF"), size=iconSize) # type: ignore
        iconButton = ctk.CTkButton(buttonFrame, image=infoIcon, text="", command=funcInfoButton, width=buttonSize, height=buttonSize)
    else:
        iconButton = ctk.CTkButton(buttonFrame, text="Info", command=funcInfoButton, width=85, text_color=themeHandler.getThemePart("text"))
    iconButton.pack(side="left", expand=False, padx=(20, 0))
    
    return buttons

def sidebar(root):
    sidebar = ctk.CTkScrollableFrame(root, width=200, corner_radius=10,
                           fg_color=themeHandler.getThemePart("frame"))
    sidebar.pack(pady=10, padx=10, side="left", fill="both")
    
    return sidebar

def textbox(parent):
    writingbox = ctk.CTkTextbox(parent, width=400, height=300, corner_radius=10,
                                fg_color=themeHandler.getThemePart("frame"), font=("Arial", 14))
    writingbox.pack(padx=(0, 10), side="left", fill="both", expand=True)
    return writingbox

def createTDrender(parent):
    tdRendererContainer = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
    return tdRendererContainer

def reloadFileList(sidebarFrame, writingBox, previewContainer, TDrenderFrame, updatePreview, openedFileButton, saver):
    for widget in sidebarFrame.winfo_children():
        widget.destroy()
    listFiles(sidebarFrame, writingBox, previewContainer, TDrenderFrame, updatePreview, openedFileButton, saver)

# again, gemini because I don't feel like figuring out how to do this myself :3
def listFiles(part, writingBox, previewContainer, TDrenderFrame, updatePreview, openedFileButton, saver):
    notesDirectory = getJson.getSetting("NotesDirectory")
    if not os.path.exists(notesDirectory): # type: ignore
        print("Notes directory not found, creating one...")
        os.makedirs(notesDirectory) # type: ignore

    for fileName in os.listdir(notesDirectory):
        if fileName.endswith((".md", ".td", ".txt")):
            filePath = os.path.join(notesDirectory, fileName) # type: ignore
            button = ctk.CTkButton(part, text=fileName, fg_color="transparent", hover_color=themeHandler.getThemePart("hover"), text_color=themeHandler.getThemePart("text"))

            def loadFileContent(path=filePath, btn=button):
                # Store the currently opened button before changing it
                previousOpenedButton = openedFileButton["button"]

                # Update the openedFileButton to the new button
                openedFileButton["button"] = btn
                btn.configure(fg_color=themeHandler.getThemePart("selected")) # Set color for the newly opened button

                # Now, if there was a previously opened button and it still exists, reset its color
                if previousOpenedButton and previousOpenedButton.winfo_exists():
                    previousOpenedButton.configure(fg_color="transparent")

                with open(path, "r", encoding='utf-8') as file:
                    content = file.read()
                
                # Always update the textbox content
                writingBox.delete("1.0", tk.END)
                writingBox.insert("1.0", content)

                saver.start(path, lambda: writingBox.get("1.0", tk.END))

                # Forget all main content widgets before packing new layout
                writingBox.pack_forget()
                previewContainer.pack_forget()
                TDrenderFrame.pack_forget()

                if path.endswith(".md"):
                    markdownRenderer.renderMarkdown(writingBox, previewContainer, updatePreview)
                elif path.endswith(".txt"):
                    textRenderer.render_text(writingBox)
                elif path.endswith(".td"):
                    saver.stop()
                    # Show todo renderer, hide editor and preview
                    for widget in TDrenderFrame.winfo_children():
                        widget.destroy()

                    renderer = tdRenderer.TodoRenderer(TDrenderFrame, content, path)
                    renderer.pack(expand=True, fill="both")
                    TDrenderFrame.pack(pady=0, padx=(0, 10), expand=True, fill="both", side="left")
                
            button.configure(command=loadFileContent)
            button.pack(pady=5, padx=10, fill="x")
            print(f"Loaded file: {fileName}")

# ===== el funny discord rpc =====
def dcRPC(root, saver):
    RPCclientID = "1415709453898092692"
    RPCmanager = dcPresence.startRPC(RPCclientID)

    def closing():
        if RPCmanager:
            RPCmanager.stop()
        saver.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", closing)
    
# ===== cool funny keybinds =====
def bindKeybinds(widget, reloadList, updatePreview, saver):
    widget.bind("<Control-s>", lambda event: saver.save())
    widget.bind("<Control-S>", lambda event: saver.save())
    widget.bind("<Control-n>", lambda event: NTDwindow.newFile(reloadList))
    widget.bind("<Control-N>", lambda event: NTDwindow.newFile(reloadList))
    widget.bind("<Control-q>", lambda event: widget.destroy())
    widget.bind("<Control-Q>", lambda event: widget.destroy())
    widget.bind("<Control-d>", lambda event: NTDwindow.delete())
    widget.bind("<Control-D>", lambda event: NTDwindow.delete())
    widget.bind("<Control-r>", lambda event: reloadList())
    widget.bind("<Control-R>", lambda event: reloadList())
    widget.bind("<F5>", lambda event: updatePreview())

# ===== refresh ui for theme! =====
def refreshUI(root):
    root.destroy()
    initializeUI()

    if getJson.getSetting("EnableDiscordRPC"):
        RPCclientID = "1415709453898092692"
        RPCmanager = dcPresence.startRPC(RPCclientID)
        if RPCmanager:
            RPCmanager.stop()
        root.destroy()
