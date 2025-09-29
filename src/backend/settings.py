import customtkinter as ctk
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import src.handler.path as pathHandler
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

import src.handler.theme as themeHandler

def getSettingsDef(currentSettings):
    settingsDefinitions = [
        {
            "name": "Theme",
            "type": "dropdown",
            "dropdown": themeHandler.listThemes(),
            "default": "Dark",
            "key": "Theme"
        },
        {
            "name": "Notes Directory",
            "type": "path",
            "default": os.path.join(os.path.expanduser('~'), "Documents", "Noteted Notes"),
            "key": "NotesDirectory"
        },
        {
            "name": "Enable Discord RPC",
            "type": "bool",
            "default": True,
            "key": "EnableDiscordRPC"
        }
    ]

    if currentSettings.get("EnableDiscordRPC", True):
        settingsDefinitions.extend([
            {
                "name": "Discord RPC Details",
                "type": "text",
                "default": "Using Noteted.",
                "key": "DiscordRPCdetails"
            },
            {
                "name": "Discord RPC State",
                "type": "text",
                "default": "Taking notes, as usual.",
                "key": "DiscordRPCstate"
            }
        ])

    settingsDefinitions.extend([
        {
            "name": "Enable Auto Saving",
            "type": "bool",
            "default": True,
            "key": "EnableAutoSaving"
        },
        {
            "name": "Check for updates",
            "type": "bool",
            "default": True,
            "key": "CheckForUpdate"
        }
    ])

    return settingsDefinitions

def listAllSettings(parent, currentSettings):
    settingsDefinitions = getSettingsDef(currentSettings)
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
            settingOptionMenu = ctk.CTkOptionMenu(settingFrame, values=settingDef["dropdown"], fg_color=themeHandler.getThemePart("accent"), button_color=themeHandler.getThemePart("secondary"), button_hover_color=themeHandler.getThemePart("hover"), text_color=themeHandler.getThemePart("text"))
            settingOptionMenu.set(currentValue)
            settingOptionMenu.pack(side="right", padx=(5, 0))
            settingOptionMenu.configure(command=lambda value, key=settingKey: updateSetting(key, value, currentSettings, parent))
        elif settingType == "bool":
            boolVar = tk.BooleanVar(value=currentValue)
            settingCheckbox = ctk.CTkCheckBox(settingFrame, text="", variable=boolVar, onvalue=True, offvalue=False, fg_color=themeHandler.getThemePart("accent"), hover_color=themeHandler.getThemePart("hover"))
            settingCheckbox.pack(side="right", padx=(5, 0))
            boolVar.trace("w", lambda *args, key=settingKey, var=boolVar: updateSetting(key, var.get(), currentSettings, parent))
        elif settingType == "path":
            pathEntry = ctk.CTkEntry(settingFrame, width=200, fg_color=themeHandler.getThemePart("textBox"), text_color=themeHandler.getThemePart("text"))
            pathEntry.insert(0, currentValue)
            pathEntry.pack(side="right", padx=(5, 0))

            def browsePath(entry_widget=pathEntry, key=settingKey):
                directory = filedialog.askdirectory()
                if directory:
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, directory)
                    updateSetting(key, directory, currentSettings, parent)

            browseButton = ctk.CTkButton(settingFrame, text="Browse", command=browsePath, width=70, fg_color=themeHandler.getThemePart("accent"), hover_color=themeHandler.getThemePart("hover"), text_color=themeHandler.getThemePart("text"))
            browseButton.pack(side="right", padx=(5, 0))
            pathEntry.bind("<FocusOut>", lambda event, key=settingKey, entry=pathEntry: updateSetting(key, entry.get(), currentSettings, parent))
        elif settingType == "text":
            settingEntry = ctk.CTkEntry(settingFrame, width=200, fg_color=themeHandler.getThemePart("textBox"), text_color=themeHandler.getThemePart("text"))
            settingEntry.insert(0, currentValue)
            settingEntry.pack(side="right", padx=(5, 0))
            settingEntry.bind("<FocusOut>", lambda event, key=settingKey, entry=settingEntry: updateSetting(key, entry.get(), currentSettings, parent))

def updateSetting(key, value, settings_dict, parent):
    print(f"updateSetting - key: {key}, value: {value}")
    settings_dict[key] = value
    print(f"Setting {key} updated to {value}")
    for widget in parent.winfo_children():
        widget.destroy()
    listAllSettings(parent, settings_dict)