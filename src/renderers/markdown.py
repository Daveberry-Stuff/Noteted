import tkinter as tk
import markdown2
from tkhtmlview import HTMLLabel
import customtkinter as ctk
import src.handler.theme as themeHandler

def previewbox(parent):
    previewContainer = ctk.CTkFrame(parent, corner_radius=10, fg_color=themeHandler.getThemePart("frame"))
    previewBox = HTMLLabel(previewContainer, background=themeHandler.getThemePart("frame"))
    previewBox.pack(expand=True, fill="both", padx=5, pady=5)
    previewContainer.label = previewBox # type: ignore
    return previewContainer

def updatePreview(writingBox, previewBox):
    markdown_text = writingBox.get("1.0", tk.END)
    html_text = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "strike"])

    # Basic styling for dark theme
    tags_to_style = ["<p>", "<h1>", "<h2>", "<h3>", "<h4>", "<h5>", "<h6>", "<li>", "<strong>", "<em>", "<a>", "<s>"]
    for tag in tags_to_style:
        html_text = html_text.replace(tag, tag[:-1] + ' style="color:' + themeHandler.getThemePart("text") + ';">')
    
    html_text = html_text.replace('<pre>', '<pre style="background-color:#2b2b2b; padding:10px; border-radius:4px;">')
    html_text = html_text.replace('<code>', '<code style="color:white;">')

    previewBox.set_html(html_text)

def renderMarkdown(writingBox, previewContainer, updatePreviewCallback):
    writingBox.pack(pady=0, padx=0, expand=True, fill="both", side="left")
    previewContainer.pack(pady=0, padx=10, expand=True, fill="both", side="right")
    updatePreviewCallback()
