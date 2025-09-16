import os

def mainPath():
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def assetsPath():
    return os.path.join(mainPath(), 'assets')

def iconsPath(which, what):
    if which == "buttons":
        return os.path.join(assetsPath(), 'icons', 'buttons', what)
    elif which == "filetype":
        return os.path.join(assetsPath(), 'icons', 'filetype', what)