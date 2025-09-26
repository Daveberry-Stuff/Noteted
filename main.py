# ===================================================================================
#             This script includs the launching and checking for updates
#                 Also includes checking if you have tkhtmlview patch.
# ===================================================================================

import sys
import os
import requests

import src.main.Noteted as Noteted
import src.main.firstTimeUse as firstTimeUse
import src.backend.settings as settings

import customtkinter as ctk
import src.handler.theme as themeHandler
import src.handler.path as pathHandler
import webbrowser

def initializeWindowUpdate():
    def topLevelIcon(toplevel_window):
        baseDirectory = pathHandler.mainPath()
        if sys.platform == "win32":
            iconPath = os.path.join(baseDirectory, 'assets', 'NTD.ico')
            if os.path.exists(iconPath):
                toplevel_window.after(200, lambda: toplevel_window.iconbitmap(iconPath))
        else:
            iconPath = os.path.join(baseDirectory, 'assets', 'NTD.png')
            if os.path.exists(iconPath):
                photo = tk.PhotoImage(file=iconPath)
                toplevel_window.iconphoto(False, photo)

    def continueAnyways():
        notificationUpdate.destroy()
        if not os.path.exists(settings.settingsFile):
            print("First time use detected, running setup...")
            firstTimeUse.initializeFirstTimeUI()
        else:
            Noteted.initializeUI()
    
    def latestRelese():
        notificationUpdate.destroy()
        webbrowser.open_new_tab("https://github.com/Daveberry-Stuff/Noteted/releases/latest")
        continueAnyways()
    
    notificationUpdate = ctk.CTk()
    notificationUpdate.title("Noteted - Update Available")
    notificationUpdate.geometry("500x175")
    notificationUpdate.resizable(False, False)

    notificationUpdate.configure(fg_color=themeHandler.getThemePart("background"))
    ctk.set_appearance_mode(themeHandler.getThemePart("WPM"))
    ctk.set_default_color_theme(themeHandler.getThemePart("DCT"))

    notificationUpdate.transient()
    notificationUpdate.after(10, notificationUpdate.grab_set)
    topLevelIcon(notificationUpdate)
    
    notificationContainer = ctk.CTkFrame(notificationUpdate, fg_color=themeHandler.getThemePart("frame"))
    notificationContainer.pack(pady=10, padx=10, expand=True, fill="both")

    messageLabel = ctk.CTkLabel(notificationContainer, text="Heya, your noteted has an update!", text_color=themeHandler.getThemePart("text"), font=("Arial", 20, "bold"))
    messageLabel.pack(pady=10, padx=10, fill="both")

    messageLabel = ctk.CTkLabel(notificationContainer, text="This is a reccomended thing to do, so please update Noteted regularly!", text_color=themeHandler.getThemePart("text"), font=("Arial", 14))
    messageLabel.pack(pady=10, padx=10, fill="both")

    updateButtonLabel = ctk.CTkButton(notificationContainer, text="Latest Release", command=latestRelese, text_color=themeHandler.getThemePart("text"))
    updateButtonLabel.pack(side="left", pady=10, padx=(10, 5), fill="x", expand=True)

    continueButtonLabel = ctk.CTkButton(notificationContainer, text="Continue Anyways", command=continueAnyways, text_color=themeHandler.getThemePart("text"))
    continueButtonLabel.pack(side="right", pady=10, padx=(5, 10), fill="x", expand=True)

    notificationUpdate.protocol("WM_DELETE_WINDOW", notificationUpdate.destroy)
    notificationUpdate.mainloop()

if __name__ == "__main__":
    def fetchUserVer():
        versionPath = os.path.join('gitver.txt')
        if os.path.exists(versionPath):
            with open(versionPath, 'r') as f:
                versionText = f.read().strip()
                return versionText

    def fetchLatestGitVer():
        response = requests.get("https://raw.githubusercontent.com/Daveberry-Stuff/Noteted/main/gitver.txt")
        response.raise_for_status()
        return response.text

    latestGitVer = fetchLatestGitVer()
    userVersion = fetchUserVer()

    print("Github latest release:", latestGitVer)
    print("User is using version:", userVersion)
    print("Is user's version the same as github?", userVersion == latestGitVer)

    if userVersion != latestGitVer:
        print("User's version is outdated or it's the wrong version!")
        initializeWindowUpdate()
    else:
        print("User's version is up to date.")
        if not os.path.exists(settings.settingsFile):
            print("First time use detected, running setup...")
            firstTimeUse.initializeFirstTimeUI()
        else:
            print("Starting up...")
            Noteted.initializeUI()