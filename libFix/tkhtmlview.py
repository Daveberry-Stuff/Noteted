import os
import sys
from PIL import Image

# fuck you fuck you fuck y-
# thank you pillow and tkhtmlvi-
def patchTKhtmlView():
    major = sys.version_info.major
    minor = sys.version_info.minor
    try:
        if sys.platform == "win32":
            parentPath = os.path.abspath(os.path.join(__file__, '..', '..'))
            parserPath = os.path.join(os.path.join(parentPath), "venv", "Lib", "site-packages", "tkhtmlview",  "html_parser.py")
        else:
            parentPath = os.path.abspath(os.path.join(__file__, '..', '..'))
            parserPath = os.path.join(os.path.join(parentPath), "venv", "lib", f"python{major}.{minor}", "site-packages", "tkhtmlview",  "html_parser.py")

        with open(parserPath, "r", encoding="utf-8") as f:
            content = f.read()

        if hasattr(Image, 'Resampling') and "Image.ANTIALIAS" in content:
            new_content = content.replace("Image.ANTIALIAS", "Image.Resampling.LANCZOS")
            with open(parserPath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("successfully patched tkhtmlview for pillow 10+.")
        elif "Image.ANTIALIAS" not in content:
            print("tkhtmlview appears to be already patched or doesn't need patching.")
        else:
            print("pillow version is less than 10.0.0, no patch needed.")


    except Exception as e:
        print(f"Error patching tkhtmlview: {e}", file=sys.stderr)

if __name__ == "__main__":
    patchTKhtmlView()