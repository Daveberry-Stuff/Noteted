import os
import sys
from PIL import Image

# !==================================================!
#                  MAJOR WARNING!!!!
#      This file is SPECIFICALLY FOR WORKFLOWS!!!
#        I don't reccomend you to run this file.
# !==================================================!

def patchTKhtmlView():
    major = sys.version_info.major
    minor = sys.version_info.minor
    micro = sys.version_info.micro
    try:
        if sys.platform == "win32":
            parserPath = f"C:\\hostedtoolcache\\windows\\python\\{major}.{minor}.{micro}\\x64\\lib\\site-packages\\tkhtmlview\\html_parser.py"
        elif sys.platform == "linux":
            parserPath = f"/opt/hostedtoolcache/Python/{major}.{minor}.{micro}/x64/lib/python{major}.{minor}/site-packages/tkhtmlview/html_parser.py"
        elif sys.platform == "darwin":
            parserPath = f"/Library/Frameworks/Python.framework/Versions/{major}.{minor}/lib/python{major}.{minor}/site-packages/tkhtmlview/html_parser.py"

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

if __name__ == "__main__":
    patchTKhtmlView()