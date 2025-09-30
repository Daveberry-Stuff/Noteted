import os
import sys
from PIL import Image

def patchTKhtmlView():
    major = sys.version_info.major
    minor = sys.version_info.minor
    venvFolderName = input("Input your virtual environment folder name: ")
    
    try:
        if sys.platform == "win32":
            parserPath = os.path.join(os.getcwd(), venvFolderName, "Lib", "site-packages", "tkhtmlview",  "html_parser.py")
        else:
            parserPath = os.path.join(os.getcwd(), venvFolderName, "lib", f"python{major}.{minor}", "site-packages", "tkhtmlview",  "html_parser.py")

        with open(str(parserPath), "r", encoding="utf-8") as f:
            content = f.read()

        if "if width > 0 and height > 0:" not in content:
            libCodeFix = """if width > 0 and height > 0:
                        image = image.resize((width, height), Image.Resampling.LANCZOS) """
            newContent = content.replace("image = image.resize((width, height), Image.ANTIALIAS)", libCodeFix)
            with open(str(parserPath), "w", encoding="utf-8") as f:
                f.write(newContent)
            print("Patched tkhtmlview!")
        else:
            print("Seems like tkhtmlview is already patched, no need to patch it again!")

    except Exception as e:
        print(f"Error patching tkhtmlview: {e}", file=sys.stderr)

patchTKhtmlView()