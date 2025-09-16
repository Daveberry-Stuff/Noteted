import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
import json

#                            I'm sure one day this will be different becuase fuck all microsoft
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Microsoft: ~\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\Roaming\Noteted
# Python: ~\AppData\Roaming\Noteted\

appdataDirectory = os.path.join(os.getenv('APPDATA'), "Noteted") # type: ignore
if not os.path.exists(appdataDirectory):
    os.makedirs(appdataDirectory)

settingsFile = os.path.join(appdataDirectory, 'settings.json')

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
        "default": os.path.expanduser('~') + os.path.sep + "Noteted Notes",
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