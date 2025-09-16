import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
import sys
import json

# silly main
#     - Windows: %APPDATA%/Noteted
#     - Linux: ~/.config/Noteted (or $XDG_CONFIG_HOME/Noteted)
#     - macOS: ~/Library/Application Support/Noteted

def getAppConfigDirectory():
    if sys.platform == 'win32':
        appdata = os.getenv('APPDATA')
        if appdata:
            return os.path.join(appdata, 'Noteted')
    elif sys.platform == 'linux': # Linux
        return os.path.join(os.getenv('XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config')), 'Noteted')
    elif sys.platform == 'darwin': # macOS
        return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'Noteted')
    # fallback for other systems or if APPDATA is not set
    return os.path.join(os.path.expanduser('~'), '.noteted')

appDirectory = getAppConfigDirectory()
if not os.path.exists(appDirectory):
    os.makedirs(appDirectory)

settingsFile = os.path.join(appDirectory, 'settings.json')

def loadSettings():
    try:
        with open(settingsFile, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def saveSettings(settingsData):
    print(f"Attempting to save settings to: {settingsFile}")
    with open(settingsFile, 'w') as f:
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
        "default": os.path.join(os.path.expanduser('~'), "Documents", "Noteted Notes"),
        "key": "NotesDirectory"
    }
]

def listAllSettings(parent, currentSettings):
    for settingDef in settingsDefinitions:
        settingName = settingDef["name"]
        settingType = settingDef["type"]
        settingKey = settingDef["key"]
        defaultValue = settingDef["default"]

        currentValue = currentSettings.get(settingKey, defaultValue)

        settingFrame = ctk.CTkFrame(parent, fg_color="transparent")
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