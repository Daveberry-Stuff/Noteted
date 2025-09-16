import os
import src.backend.settings as settings
import json

def getSetting(key):
    settingsData = settings.loadSettings()
    if settingsData and key in settingsData:
        return settingsData[key]
    else:
        # return default value meow
        for setting in settings.settingsDefinitions:
            if setting["key"] == key:
                return setting["default"]
    return None