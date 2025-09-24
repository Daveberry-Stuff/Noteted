import customtkinter as ctk
import src.handler.theme as themeHandler
import src.main.NTDwindow as NTDwindow
import sys

# i fucking fucking fucking hate this code so much
# i know there's probably a easier and better way
# but like... i don't care anymore
# it works, and that's all that matters
# half of the code was written by gemini and half the code was written by me through bing searching
# also stfu that i use bing, i can use whatever i want :/
class RightClickMenu(ctk.CTkToplevel):
    def __init__(self, master, reload_callback, **kwargs):
        transparent_color = themeHandler.getThemePart("background")
        if sys.platform == "win32":
            super().__init__(master, fg_color=transparent_color, **kwargs)
        else:
            super().__init__(master, **kwargs)

        if sys.platform == "win32":
            self.overrideredirect(True)
            self.attributes("-topmost", True)
            self.attributes("-transparentcolor", transparent_color)

        if sys.platform == "win32":
            self.frame = ctk.CTkFrame(self, fg_color=themeHandler.getThemePart("rightClick"))
        else:
            self.frame = ctk.CTkFrame(self, corner_radius=5, fg_color=themeHandler.getThemePart("rightClick"))
        self.frame.pack(expand=True, fill="both")

        self.addCommand(label="Delete", command=self.delete)
        self.addCommand(label="Rename", command=self.rename)
        # self.addCommand(label="Pin", command=self.pin)
        # self.addCommand(label="Lock", command=self.lock)

        self.withdraw()
        self.filePath = None
        self.reload_callback = reload_callback

    def addCommand(self, label, command):
        button = ctk.CTkButton(self.frame, text=label, command=command, anchor="w", corner_radius=5, fg_color="transparent", hover_color=themeHandler.getThemePart("selected"), text_color=themeHandler.getThemePart("text"))
        button.pack(in_=self.frame, fill="x", padx=10, pady=5)

    def popup(self, event, filePath):
        self.filePath = filePath
        self.deiconify()
        self.update_idletasks()
        
        x = event.x_root
        y = event.y_root
        
        self.geometry(f"+{x}+{y}")
        self.lift()
        self.focus_set()
        self.bind("<FocusOut>", self.onFocusOut)

    def onFocusOut(self, event):
        self.withdraw()

    def delete(self):
        self.withdraw()
        if self.filePath:
            NTDwindow.delete(self.filePath, self.reload_callback)

    def rename(self):
        self.withdraw()
        if self.filePath:
            NTDwindow.rename(self.filePath, self.reload_callback)

    # coming soon :3
    def pin(self):
        self.withdraw()

    def lock(self):
        self.withdraw()