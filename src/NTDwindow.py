import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os
import sys
import webbrowser
import datetime
import src.getFromJSON as getJson
import src.settings as Nsettings

def topLevelIcon(toplevel_window):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    if sys.platform == "win32":
        icon_path = os.path.join(base_dir, 'assets', 'NTD.ico')
        if os.path.exists(icon_path):
            toplevel_window.after(200, lambda: toplevel_window.iconbitmap(icon_path))
    else:
        icon_path = os.path.join(base_dir, 'assets', 'NTD.png')
        if os.path.exists(icon_path):
            photo = tk.PhotoImage(file=icon_path)
            toplevel_window.iconphoto(False, photo)

def delete():
    print("Delete window opened!")

def settings():
    root = ctk.CTkToplevel()
    root.title("Noteted - Settings")
    root.geometry("400x600")
    root.minsize(400, 600)
    
    root.transient()
    root.after(10, root.grab_set)

    topLevelIcon(root)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    currentSettings = Nsettings.loadSettings()

    settingContainer = ctk.CTkFrame(root, corner_radius=10, fg_color="#1e1e1e")
    settingContainer.pack(pady=10, padx=10, expand=True, fill="both")

    Nsettings.listAllSettings(settingContainer, currentSettings)

    def onClosed():
        print("Settings window closed!")
        Nsettings.saveSettings(currentSettings)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", onClosed)

def newFile(reload_callback=None):
    newFileWindow = ctk.CTkToplevel()
    newFileWindow.title("Noteted - New File")
    newFileWindow.geometry("450x150")
    newFileWindow.resizable(False, False)

    newFileWindow.transient()
    newFileWindow.after(10, newFileWindow.grab_set)

    topLevelIcon(newFileWindow)

    def createFileWithExtension(extension):
        baseName = fileNameEntry.get()
        if not baseName:
            print("Filename cannot be empty.")
            return

        fileName = f"{baseName}{extension}"
        notesDirectory = getJson.getSetting("NotesDirectory")
        filePath = os.path.join(notesDirectory, fileName) # type: ignore

        if os.path.exists(filePath):
            print(f"File '{fileName}' already exists.")
            return

        try:
            with open(filePath, 'w') as f:
                f.write("")
            print(f"File '{fileName}' created successfully.")
            if reload_callback:
                reload_callback()
            newFileWindow.destroy()
        except Exception as e:
            print(f"Error creating file: {e}")

    container = ctk.CTkFrame(newFileWindow, fg_color="#1e1e1e")
    container.pack(pady=10, padx=10, expand=True, fill="both")

    titleLabel = ctk.CTkLabel(container, text="Cookin' up a new file...", font=ctk.CTkFont(size=24, weight="bold"))
    titleLabel.pack(pady=10, padx=10)

    fileNameEntry = ctk.CTkEntry(container, placeholder_text="Enter filename here...")
    now = datetime.datetime.now()
    defaultFileName = now.strftime("%Y-%m-%d")
    fileNameEntry.insert(0, defaultFileName)
    fileNameEntry.pack(fill="x", padx=10)

    # --- Button Container ---
    buttonFrame = ctk.CTkFrame(container, fg_color="transparent")
    buttonFrame.pack(pady=10, padx=10, expand=True, fill="x")
    
    mdButton = ctk.CTkButton(buttonFrame, text=".md", command=lambda: createFileWithExtension(".md"), width=100)
    mdButton.pack(side="left", expand=True, fill="x", padx=10)

    tdButton = ctk.CTkButton(buttonFrame, text=".td", command=lambda: createFileWithExtension(".td"), width=100)
    tdButton.pack(side="left", expand=True, fill="x", padx=10)

    txtButton = ctk.CTkButton(buttonFrame, text=".txt", command=lambda: createFileWithExtension(".txt"), width=100)
    txtButton.pack(side="left", expand=True, fill="x", padx=10)

    newFileWindow.protocol("WM_DELETE_WINDOW", newFileWindow.destroy)

def info():
    infoWindow = ctk.CTkToplevel()
    infoWindow.title("Noteted - Info")
    infoWindow.geometry("400x325")
    infoWindow.resizable(False, False)

    infoWindow.transient()
    infoWindow.after(10, infoWindow.grab_set)
    
    topLevelIcon(infoWindow)

    def redirectGithub():
        webbrowser.open_new_tab("https://github.com/daveberrys/Noteted")

    container = ctk.CTkFrame(infoWindow, fg_color="#1e1e1e")
    container.pack(pady=10, padx=10, expand=True, fill="both")

    # --- Image ---
    logoPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'NTD.png')
    if os.path.exists(logoPath):
        pilImage = Image.open(logoPath)
        ctkImage = ctk.CTkImage(pilImage, size=(100, 100))
        
        imageLabel = ctk.CTkLabel(container, image=ctkImage, text="")
        imageLabel.image = ctkImage # type: ignore
        imageLabel.pack(pady=10)

    # --- Text ---
    versionPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gitver.txt')
    if os.path.exists(versionPath):
        with open(versionPath, 'r') as f:
            versionContent = f.read().strip()
    
    titleText = ctk.CTkLabel(container, text="Noteted", font=ctk.CTkFont(size=24, weight="bold"))
    infoText = ctk.CTkLabel(container, text="A simple, free and open source note taking app.", wraplength=340)
    maintainerText = ctk.CTkLabel(container, text="Maintained by Daveberry Blueson.", wraplength=340)
    versionText = ctk.CTkLabel(container, text=versionContent, wraplength=340) # type: ignore
    
    titleText.pack(pady=(0, 10))
    infoText.pack()
    maintainerText.pack()
    versionText.pack()

    # --- Buttons ---
    buttonContainer = ctk.CTkFrame(container, fg_color="transparent")
    buttonContainer.pack(pady=10, padx=10, expand=True, fill="x")

    githubButton = ctk.CTkButton(buttonContainer, text="Github", command=redirectGithub)
    githubButton.pack(side="left", expand=True, fill="x", padx=10)

    infoWindow.protocol("WM_DELETE_WINDOW", infoWindow.destroy)
