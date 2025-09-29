import json
import os
import src.backend.getFromJSON as getFromJSON
import src.handler.path as pathHandler

def getThemePath():
    return os.path.join(pathHandler.assetsPath(), 'theme')

def loadTheme(themeName=None):
    if themeName is None:
        themeName = getFromJSON.getSetting('Theme')

    theme_file_path = os.path.join(getThemePath(), f"{themeName}.json")

    try:
        with open(theme_file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to default theme if the specified theme is not found or corrupted
        print(f"Theme '{themeName}' not found or is corrupted, falling back to Dark theme.")
        default_theme_path = os.path.join(getThemePath(), 'Dark.json')
        with open(default_theme_path, 'r') as f:
            return json.load(f)

def listThemes():
    theme_path = getThemePath()
    if not os.path.exists(theme_path):
        return []
    
    themes = [f.replace('.json', '') for f in os.listdir(theme_path) if f.endswith('.json')]
    return themes

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

    elif part == "text":
        themeGot = theme.get("textColor", {})
    elif part == "button":
        themeGot = theme.get("buttonColor", {})

    elif part == "WPM":
        themeGot = theme.get("ctkWindowAppearanceMode", {})
    elif part == "DCT":
        themeGot = theme.get("ctkDefaultColorTheme", {})
    return str(themeGot)