import customtkinter as ctk
from PIL import Image
import os
import webbrowser
import datetime
import src.getFromJSON as getJson
import src.ui as ui

def delete():
    print("Delete window opened!")

def newFile(reload_callback=None):
    newFileWindow = ctk.CTkToplevel()
    newFileWindow.title("Noteted - New File")
    newFileWindow.geometry("450x150")
    newFileWindow.resizable(False, False)

    newFileWindow.transient()
    newFileWindow.grab_set()

    iconPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'NTD.ico')
    if os.path.exists(iconPath):
        newFileWindow.after(200, lambda: newFileWindow.iconbitmap(iconPath))

    def createFileWithExtension(extension):
        baseName = fileNameEntry.get()
        if not baseName:
            print("Filename cannot be empty.")
            return

        fileName = f"{baseName}{extension}"
        notesDirectory = getJson.getSetting("NotesDirectory")
        filePath = os.path.join(notesDirectory, fileName)

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
    infoWindow.geometry("400x300")
    infoWindow.resizable(False, False)

    infoWindow.transient()
    infoWindow.grab_set()
    
    iconPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'NTD.ico')
    if os.path.exists(iconPath):
        infoWindow.after(200, lambda: infoWindow.iconbitmap(iconPath))

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
        imageLabel.image = ctkImage  # Keep a reference
        imageLabel.pack(pady=10)

    # --- Text ---
    titleText = ctk.CTkLabel(container, text="Noteted", font=ctk.CTkFont(size=24, weight="bold"))
    infoText = ctk.CTkLabel(container, text="A simple, free and open source note taking app.", wraplength=340)
    maintainerText = ctk.CTkLabel(container, text="Maintained by Daveberry Blueson.", wraplength=340)
    
    titleText.pack(pady=(0, 10))
    infoText.pack()
    maintainerText.pack()

    # --- Buttons ---
    buttonContainer = ctk.CTkFrame(container, fg_color="transparent")
    buttonContainer.pack(pady=10, padx=10, expand=True, fill="x")

    githubButton = ctk.CTkButton(buttonContainer, text="Github", command=redirectGithub)
    githubButton.pack(side="left", expand=True, fill="x", padx=10)

    infoWindow.protocol("WM_DELETE_WINDOW", infoWindow.destroy)
