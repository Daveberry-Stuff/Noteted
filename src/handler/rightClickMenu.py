import customtkinter as ctk
import src.handler.theme as themeHandler

# i fucking fucking fucking hate this code so much
# i know there's probably a easier and better way
# but like... i don't care anymore
# it works, and that's all that matters
# half of the code was written by gemini and half the code was written by me through bing searching
# also stfu that i use bing, i can use whatever i want :/
class RightClickMenu(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        transparent_color = themeHandler.getThemePart("background")
        super().__init__(master, fg_color=transparent_color, **kwargs)

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", transparent_color)

        self.frame = ctk.CTkFrame(self, corner_radius=5, fg_color=themeHandler.getThemePart("rightClick"))
        self.frame.pack(expand=True, fill="both")

        self.addCommand(label="Delete", command=self.delete)
        self.addCommand(label="Rename", command=self.rename)
        self.addCommand(label="Pin", command=self.pin)
        self.addCommand(label="Lock", command=self.lock)

        self.withdraw()

    def addCommand(self, label, command):
        button = ctk.CTkButton(self.frame, text=label, command=command, anchor="w", corner_radius=5, fg_color="transparent", hover_color=themeHandler.getThemePart("selected"), text_color=themeHandler.getThemePart("text"))
        button.pack(in_=self.frame, fill="x", padx=10, pady=5)

    def popup(self, event):
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

    def rename(self):
        self.withdraw()

    def pin(self):
        self.withdraw()

    def lock(self):
        self.withdraw()