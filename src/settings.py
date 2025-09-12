import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
import src.ui as ui
import json

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')

def loadSettings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)

def saveSettings(settingsData):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settingsData, f, indent=4)

settingsDefinitions = [
    {
        "name": "Theme",
        "type": "dropdown",
        "dropdown": ["Light", "Dark", "Custom"],
        "default": "Dark",
        "key": "Theme"
    },
    {
        "name": "Enable Discord RPC",
        "type": "bool",
        "default": True,
        "key": "EnableDiscordRPC"
    },
    {
        "name": "Notes Directory",
        "type": "path",
        "default": os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test-notes'),
        "key": "NotesDirectory"
    }
]

def initializeSettingsUI():
    root = ctk.CTk()
    root.title("Noteted - Settings")
    root.geometry("400x600")
    root.minsize(400, 600)
    root.iconbitmap(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'NTD.ico'))
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    currentSettings = loadSettings()
    listAllSettings(root, currentSettings)

    def onClosed():
        print("Settings window closed!")
        saveSettings(currentSettings)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", onClosed)
    root.mainloop()


# once again, i did use ai because I'M TOO LAZY !!!
def listAllSettings(root, currentSettings):
    print("Listing all settings...")
    settingContainer = ctk.CTkFrame(root, corner_radius=10, fg_color="#1e1e1e")
    settingContainer.pack(pady=10, padx=10, expand=True, fill="both", side="right")

    for settingDef in settingsDefinitions:
        settingName = settingDef["name"]
        settingType = settingDef["type"]
        settingKey = settingDef["key"]
        defaultValue = settingDef["default"]

        currentValue = currentSettings.get(settingKey, defaultValue)

        settingFrame = ctk.CTkFrame(settingContainer, fg_color="transparent")
        settingFrame.pack(pady=5, padx=10, fill="x")

        settingLabel = ctk.CTkLabel(settingFrame, text=settingName)
        settingLabel.pack(side="left", padx=(0, 5))

        if settingType == "dropdown":
            settingOptionMenu = ctk.CTkOptionMenu(settingFrame, values=settingDef["dropdown"])
            settingOptionMenu.set(currentValue)
            settingOptionMenu.pack(side="right", padx=(5, 0))
            settingOptionMenu.configure(command=lambda value, key=settingKey: updateSetting(key, value, currentSettings))
        elif settingType == "bool":
            settingCheckbox = ctk.CTkCheckBox(settingFrame, text="", onvalue=True, offvalue=False)
            settingCheckbox.pack(side="right", padx=(5, 0))
            if currentValue:
                settingCheckbox.select()
            else:
                settingCheckbox.deselect()
            settingCheckbox.configure(command=lambda key=settingKey: updateSetting(key, settingCheckbox.get(), currentSettings))
        elif settingType == "path":
            pathEntry = ctk.CTkEntry(settingFrame, width=200)
            pathEntry.insert(0, currentValue)
            pathEntry.pack(side="right", padx=(5, 0))

            def browsePath(entry_widget=pathEntry, key=settingKey):
                directory = filedialog.askdirectory()
                if directory:
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, directory)
                    updateSetting(key, directory, currentSettings)

            browseButton = ctk.CTkButton(settingFrame, text="Browse", command=browsePath, width=70)
            browseButton.pack(side="right", padx=(5, 0))
            pathEntry.bind("<FocusOut>", lambda event, key=settingKey, entry=pathEntry: updateSetting(key, entry.get(), currentSettings))

    def updateSetting(key, value, settings_dict):
        settings_dict[key] = value
        print(f"Setting {key} updated to {value}")

    saveButton = ctk.CTkButton(settingContainer, text="Save Settings", command=lambda: saveSettings(currentSettings))
    saveButton.pack(pady=10)

    return settingContainer
