import sys
import os

import src.ui as ui
import src.firstTimeUse as firstTimeUse
import src.settings as settings

if __name__ == "__main__":
    # Check if settings file exists to determine if it's the first run
    if not os.path.exists(settings.settingsFile):
        print("First time use detected, running setup...")
        firstTimeUse.initializeFirstTimeUI()
    else:
        ui.initializeUI()