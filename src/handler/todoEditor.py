import os
import tkinter as tk
import customtkinter as ctk
import src.renderers.todo as tdRenderer
import src.main.Noteted as Noteted
import src.handler.theme as themeHandler
import src.handler.path as pathHandler

def refreshAll(textEditor, tdRenderFrame, filePath, Noteted):
    content = textEditor.get("1.0", "end-1c")

    for widget in tdRenderFrame.winfo_children():
        widget.destroy()

    textEditorFrame = ctk.CTkFrame(tdRenderFrame, fg_color="transparent")
    textEditorFrame.pack(fill="both", padx=0, pady=0, side="bottom")

    rawTextEditor = ctk.CTkTextbox(textEditorFrame, fg_color=themeHandler.getThemePart("frame"))
    rawTextEditor.pack(fill="both", padx=(0, 10), pady=(10, 0), side="left", expand=True)
    rawTextEditor.insert("1.0", content)

    renderer = tdRenderer.TodoRenderer(tdRenderFrame, content, filePath, rawTextEditor)
    renderer.pack(expand=True, fill="both")
    tdRenderFrame.pack(pady=0, padx=(0, 10), expand=True, fill="both", side="top")
    
    renderer.tkraise()

    textEditorButtons = ctk.CTkFrame(textEditorFrame, fg_color=themeHandler.getThemePart("frame"))
    textEditorButtons.pack(fill="both", padx=0, pady=(10, 0), side="right")

    iconSize = (20, 20)
    buttonSize = 30

    # -- Refresh Button --
    refreshButtonPath = str(pathHandler.iconsPath("buttons", "refresh-ccw.png"))
    if os.path.exists(refreshButtonPath):
        recoloredIcon = Noteted.recolorImage(refreshButtonPath, color=themeHandler.getThemePart("button"))
        if recoloredIcon:
            refreshIcon = ctk.CTkImage(recoloredIcon, size=iconSize)
            refreshContent = ctk.CTkButton(textEditorButtons, image=refreshIcon, text="", command=lambda: refreshAll(rawTextEditor, tdRenderFrame, filePath, Noteted), width=buttonSize, height=buttonSize)
        else:
            refreshContent = ctk.CTkButton(textEditorButtons, text="R", command=lambda: refreshAll(rawTextEditor, tdRenderFrame, filePath, Noteted), width=buttonSize, height=buttonSize, text_color=themeHandler.getThemePart("text"))
    else:
        refreshContent = ctk.CTkButton(textEditorButtons, text="R", command=lambda: refreshAll(rawTextEditor, tdRenderFrame, filePath, Noteted), width=buttonSize, height=buttonSize, text_color=themeHandler.getThemePart("text"))
    
    refreshContent.pack(expand=True, fill="y", pady=10, padx=10)