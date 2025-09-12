import os
import src.ui as ui
import src.settings as settings
import json

def getSetting(key):
    settingsData = settings.loadSettings()
    if settingsData and key in settingsData:
        return settingsData[key]
    else:
        # Return default value if setting not found
        for setting in settings.settingsDefinitions:
            if setting["key"] == key:
                return setting["default"]
    return None