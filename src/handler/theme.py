import json
import os
import src.backend.getFromJSON as getFromJSON
import src.handler.path as pathHandler
import sys

def getThemePath():
    return os.path.join(pathHandler.assetsPath(), 'theme')

# took from src/backend/settings
def getCustomThemePath():
    if sys.platform == 'win32':
        return os.path.join(os.getenv('APPDATA'), 'Noteted', 'theme')
    elif sys.platform == 'linux': # Linux
        return os.path.join(os.getenv('XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config')), 'Noteted', 'theme')
    elif sys.platform == 'darwin': # macOS
        return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'Noteted', 'theme')
    # fallback for other systems or if APPDATA is not set
    return os.path.join(os.path.expanduser('~'), '.noteted', 'theme')

def loadTheme(themeName=None):
    if themeName is None:
        themeName = getFromJSON.getSetting('Theme')

    if themeName == "Dark" or themeName == "Light" or themeName == "Pure Black":
        themeFilePath = os.path.join(getThemePath(), f"{themeName}.json")
    else:
        themeFilePath = os.path.join(getCustomThemePath(), f"{themeName}.json")

    try:
        with open(themeFilePath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Theme '{themeName}' not found or is corrupted, falling back to Dark theme.")
        defaultThemePath = os.path.join(getThemePath(), 'Dark.json')
        with open(defaultThemePath, 'r') as f:
            return json.load(f)

def listThemes():
    # -- default themes
    themePath = getThemePath()
    if not os.path.exists(themePath):
        return []
    themes = [f.replace('.json', '') for f in os.listdir(themePath) if f.endswith('.json')]

    # -- custom themes
    customThemePath = getCustomThemePath()
    if not os.path.exists(customThemePath):
        os.makedirs(customThemePath)
    customThemes = [f.replace('.json', '') for f in os.listdir(customThemePath) if f.endswith('.json')]

    return themes + customThemes

# listen mate
def getThemePart(part):
    themeGot = {}
    theme = loadTheme()
    if part == "accent":
        themeGot = theme.get("accentColor", {})
    elif part == "secondary":
        themeGot = theme.get("secondaryColor", {})
    elif part == "hover":
        themeGot = theme.get("hoverColor", {})
    elif part == "background":
        themeGot = theme.get("backgroundColor", {})

    elif part == "frame":
        themeGot = theme.get("frameColor", {})
    elif part == "textBox":
        themeGot = theme.get("textBoxColor", {})
    elif part == "selected":
        themeGot = theme.get("selectedColor", {})
    elif part == "frameHover":
        themeGot = theme.get("frameHoverColor", {})
    elif part == "rightClick":
        themeGot = theme.get("rightClickMenuColor", {})

    elif part == "frameText":
        themeGot = theme.get("frameTextColor", {})
    elif part == "text":
        themeGot = theme.get("textColor", {})
    elif part == "button":
        themeGot = theme.get("buttonColor", {})

    elif part == "WPM":
        themeGot = theme.get("ctkWindowAppearanceMode", {})
    elif part == "DCT":
        themeGot = theme.get("ctkDefaultColorTheme", {})
    return str(themeGot)