import sys
import os

import src.main.Noteted as Noteted
import src.main.firstTimeUse as firstTimeUse
import src.backend.settings as settings

if __name__ == "__main__":
    if not os.path.exists(settings.settingsFile):
        print("First time use detected, running setup...")
        firstTimeUse.initializeFirstTimeUI()
    else:
        Noteted.initializeUI()