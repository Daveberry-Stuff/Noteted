import customtkinter as ctk
import tkinter as tk
import sys
import os
import tkinter.filedialog as filedialog
import src.backend.settings as settings
import src.main.ui as ui
import src.handler.path as pathHandler

def initializeFirstTimeUI():
    root = ctk.CTk()
    root.title("Noteted - First Time Setup")
    root.geometry("400x300")
    root.minsize(400, 300)

    baseDirectory = pathHandler.mainPath()
    if sys.platform == "win32":
        iconPath = os.path.join(baseDirectory, 'assets', 'NTD.ico')
        if os.path.exists(iconPath):
            root.iconbitmap(iconPath)
    else:
        iconPath = os.path.join(baseDirectory, 'assets', 'NTD.png')
        if os.path.exists(iconPath):
            root.iconphoto(False, tk.PhotoImage(file=iconPath))

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    continue_pressed = False
    defaultSettings = {setting["key"]: setting["default"] for setting in settings.settingsDefinitions}

    def onClosing():
        # this handels the person closing this window
        if continue_pressed:
            return

        print("First time setup closed without completing. Saving default settings.")
        
        notesPath = defaultSettings.get("NotesDirectory")
        if notesPath and not os.path.exists(notesPath):
            os.makedirs(notesPath)
            
        settings.saveSettings(defaultSettings)
        root.destroy()

    def setContinuePressed():
        nonlocal continue_pressed
        continue_pressed = True

    root.protocol("WM_DELETE_WINDOW", onClosing)
    setupWidgets(root, defaultSettings, setContinuePressed)

    root.mainloop()

def setupWidgets(root, defaultSettings, setContinuePressed):
    container = ctk.CTkFrame(root, fg_color="transparent")
    container.pack(pady=20, padx=20, expand=True, fill="both")

    titleLabel = ctk.CTkLabel(container, text="Welcome to Noteted!", font=ctk.CTkFont(size=24, weight="bold"))
    titleLabel.pack(pady=(0, 10))

    infoLabel = ctk.CTkLabel(container, text="Since this is your first time using, let's configure some settings before continuing!", wraplength=340)
    infoLabel.pack(pady=(0, 20))

    # ------------ NOTES PATH DIRECTORY ------------
    notesDirDefault = ""
    for settingDef in settings.settingsDefinitions:
        if settingDef["key"] == "NotesDirectory":
            notesDirDefault = settingDef["default"]
            break

    pathFrame = ctk.CTkFrame(container, fg_color="transparent")
    pathFrame.pack(fill="x", expand=True, pady=(0, 10))

    pathEntry = ctk.CTkEntry(pathFrame, width=250)
    pathEntry.insert(0, notesDirDefault)
    pathEntry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    def browsePath():
        directory = filedialog.askdirectory()
        if directory:
            pathEntry.delete(0, tk.END)
            pathEntry.insert(0, directory)

    browseButton = ctk.CTkButton(pathFrame, text="Browse", width=80, command=browsePath)
    browseButton.pack(side="right")
    
    # ------------ ENABLE DISCORD RPC ------------
    rpcFrame = ctk.CTkFrame(container, fg_color="transparent")
    rpcFrame.pack(pady=(0, 70))
    
    rpcCheckbox = ctk.CTkCheckBox(rpcFrame, text="Enable Discord RPC", onvalue=True, offvalue=False)
    rpcCheckbox.pack()
    
    # ------------ CONTINUE BUTTON ------------
    # deltarune ahh reference
    def proceed():
        setContinuePressed()
        notesPath = pathEntry.get()
        if not os.path.exists(notesPath):
            os.makedirs(notesPath)
        
        finalSettings = defaultSettings.copy()
        finalSettings["NotesDirectory"] = notesPath
        finalSettings["EnableDiscordRPC"] = rpcCheckbox.get()
        settings.saveSettings(finalSettings)
        
        root.destroy()
        ui.initializeUI()

    continueButton = ctk.CTkButton(container, text="Continue", command=proceed)
    continueButton.pack(side="bottom")

if __name__ == "__main__":
    initializeFirstTimeUI()