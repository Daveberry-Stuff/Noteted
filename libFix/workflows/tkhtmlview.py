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
            parserPath = f"/usr/lib/python{major}.{minor}/tkhtmlview/html_parser.py", 
        elif sys.platform == "darwin":
            parserPath = f"/Library/Frameworks/Python.framework/Versions/{major}.{minor}/lib/python{major}.{minor}/site-packages/tkhtmlview/html_parser.py"

        with open(str(parserPath), "r", encoding="utf-8") as f:
            content = f.read()

        if hasattr(Image, 'Resampling') and "Image.ANTIALIAS" in content:
            newContent = content.replace("Image.ANTIALIAS", "Image.Resampling.LANCZOS")
            with open(str(parserPath), "w", encoding="utf-8") as f:
                f.write(newContent)
            print("successfully patched tkhtmlview for pillow 10+.")
        elif "Image.ANTIALIAS" not in content:
            print("tkhtmlview appears to be already patched or doesn't need patching.")
        else:
            print("pillow version is less than 10.0.0, no patch needed.")


    except Exception as e:
        print(f"Error patching tkhtmlview: {e}", file=sys.stderr)

if __name__ == "__main__":
    patchTKhtmlView()