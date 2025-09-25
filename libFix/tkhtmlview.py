import os
import sys
from PIL import Image

# fuck you fuck you fuck y-
# thank you pillow and tkhtmlvi-
def patchTKhtmlView():
    major = sys.version_info.major
    minor = sys.version_info.minor
    micro = sys.version_info.micro
    try:
        if sys.platform == "win32":
            parentPath = os.path.abspath(os.path.join(__file__, '..', '..'))
            parserPath = os.path.join(os.path.join(parentPath), "venv", "Lib", "site-packages", "tkhtmlview",  "html_parser.py")
        elif sys.platform == "linux" and sys.platform == "darwin":
            parentPath = os.path.abspath(os.path.join(__file__, '..', '..'))
            parserPath = os.path.join(os.path.join(parentPath), "venv", "lib", f"python{major}.{minor}", "site-packages", "tkhtmlview",  "html_parser.py")

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