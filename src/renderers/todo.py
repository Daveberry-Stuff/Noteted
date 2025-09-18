import customtkinter as ctk
import tkinter as tk
import re
import src.handler.theme as themeHandler

class TodoRenderer(ctk.CTkScrollableFrame):
    def __init__(self, parent, fileContent, filePath):
        super().__init__(parent, fg_color=themeHandler.getThemePart("frame"))
        self.filePath = filePath
        self.lines = fileContent.split('\n')
        self.contentFrame = None
        self.render()

    def render(self):
        if self.contentFrame:
            self.contentFrame.destroy()
        
        self.contentFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.contentFrame.pack(expand=True, fill="both")

        self.boardFrames = {}
        currentBoardFrame = self.contentFrame

        # Create a default board frame for todos that are not under any board
        defaultBoardFrame = ctk.CTkFrame(self.contentFrame, fg_color="transparent")
        defaultBoardFrame.pack(fill="x", padx=10)
        currentBoardFrame = defaultBoardFrame

        for i, line in enumerate(self.lines):
            # Board
            boardMatch = re.match(r'^\s*###\s+(.*)', line)
            if boardMatch:
                boardName = boardMatch.group(1).strip()
                headerFrame = ctk.CTkFrame(self.contentFrame, fg_color="transparent")
                headerFrame.pack(fill="x", padx=10, pady=(10, 5))

                boardLabel = ctk.CTkLabel(headerFrame, text=boardName, font=("Arial", 24, "bold"))
                boardLabel.pack(side="left", anchor="w")
                boardLabel.bind("<Double-Button-1>", lambda event, li=i, label=boardLabel: self.startRename(event, li, label, "board"))

                deleteButton = ctk.CTkButton(headerFrame, text="[x]", width=30, fg_color="transparent", text_color="#E74C3C", hover_color="#555555")
                deleteButton.pack(side="right")
                deleteButton.configure(command=lambda li=i: self.deleteLine(li))
                
                boardFrame = ctk.CTkFrame(self.contentFrame, fg_color="transparent")
                boardFrame.pack(fill="x", padx=10)

                self.boardFrames[boardName] = boardFrame
                currentBoardFrame = boardFrame
                continue

            # Todo
            todoMatch = re.match(r'^(\s*)\[(.)\]\s+(.*)', line)
            if todoMatch:
                indent = len(todoMatch.group(1))
                status = todoMatch.group(2)
                text = todoMatch.group(3).strip()
                
                self.renderTodoItem(currentBoardFrame, i, indent, status, text)
        
        # Add new todo/board buttons
        self.renderGlobalButtons()

    def renderTodoItem(self, parent, lineIndex, indent, status, text):
        todoFrame = ctk.CTkFrame(parent, fg_color="transparent")
        todoFrame.pack(anchor="w", fill="x", padx=(indent * 20, 0))

        # Checkbox
        checkboxText = {' ': '[ ]', 'x': '[x]', '~': '[~]'}.get(status, '[ ]')
        checkbox = ctk.CTkButton(todoFrame, text=checkboxText, width=30, fg_color="transparent", text_color="#3498DB", hover_color="#555555")
        checkbox.pack(side="left")
        checkbox.configure(command=lambda li=lineIndex: self.toggleTodo(li))
        checkbox.bind("<Button-3>", lambda event, li=lineIndex: self.cancelTodo(event, li))

        # Text
        todoTextLabel = ctk.CTkLabel(todoFrame, text=text)
        if status == '~':
            todoTextLabel.configure(text_color="gray")
        todoTextLabel.pack(side="left", padx=5)
        todoTextLabel.bind("<Double-Button-1>", lambda event, li=lineIndex, label=todoTextLabel: self.startRename(event, li, label, "todo"))

        # Buttons
        deleteButton = ctk.CTkButton(todoFrame, text="[x]", width=30, fg_color="transparent", text_color="#E74C3C", hover_color="#555555")
        deleteButton.pack(side="right")
        deleteButton.configure(command=lambda li=lineIndex: self.deleteLine(li))
        
        addSubButton = ctk.CTkButton(todoFrame, text="[+]", width=30, fg_color="transparent", text_color="gray", hover_color="#555555")
        addSubButton.pack(side="right")
        addSubButton.configure(command=lambda li=lineIndex: self.addSubTodo(li))

    def renderGlobalButtons(self):
        buttonFrame = ctk.CTkFrame(self.contentFrame, fg_color="transparent")
        buttonFrame.pack(fill="x", pady=20, padx=10)

        addTodoButton = ctk.CTkButton(buttonFrame, text="[+]", width=30, command=self.addTodo, fg_color="transparent", text_color="gray", hover_color="#555555")
        addTodoButton.pack(side="left")

        addBoardButton = ctk.CTkButton(buttonFrame, text="[#]", width=30, command=self.addBoard, fg_color="transparent", text_color="gray", hover_color="#555555")
        addBoardButton.pack(side="left", padx=5)

    def startRename(self, event, lineIndex, labelWidget, itemType):
        # Hide the label
        labelWidget.pack_forget()

        # Create an Entry widget
        entryWidget = ctk.CTkEntry(labelWidget.master, width=labelWidget.winfo_width())
        entryWidget.insert(0, labelWidget.cget("text"))
        
        if itemType == "board":
            entryWidget.pack(anchor="w", pady=(10, 5), padx=10, fill="x", expand=True)
        elif itemType == "todo":
            entryWidget.pack(side="left", padx=5, fill="x", expand=True)
        
        entryWidget.focus_set()

        # Bind events to finish renaming
        entryWidget.bind("<Return>", lambda event, li=lineIndex, oldLabel=labelWidget, entry=entryWidget, iType=itemType: self.finishRename(event, li, oldLabel, entry, iType))
        entryWidget.bind("<FocusOut>", lambda event, li=lineIndex, oldLabel=labelWidget, entry=entryWidget, iType=itemType: self.finishRename(event, li, oldLabel, entry, iType))

    def finishRename(self, event, lineIndex, oldLabelWidget, entryWidget, itemType):
        newName = entryWidget.get().strip()
        entryWidget.destroy() # Remove the entry widget

        if newName: # Only update if new name is not empty
            if itemType == "board":
                # Update board name
                oldLine = self.lines[lineIndex]
                self.lines[lineIndex] = re.sub(r'###\s+.*', f'### {newName}', oldLine)
            elif itemType == "todo":
                # Update todo text, preserving status and indentation
                oldLine = self.lines[lineIndex]
                # Extract indentation and status
                match = re.match(r'^(\s*)\[(.)\]\s+(.*)', oldLine)
                if match:
                    indent = match.group(1)
                    status = match.group(2)
                    self.lines[lineIndex] = f"{indent}[{status}] {newName}"
            
            self.saveAndRerender()
        else:
            # If new name is empty, just show the old label again
            if itemType == "board":
                oldLabelWidget.pack(side="left", anchor="w")
            elif itemType == "todo":
                oldLabelWidget.pack(side="left", padx=5)

    def addTodo(self):
        self.lines.append("[ ] New Todo")
        self.saveAndRerender()

    def addBoard(self):
        self.lines.append("\n### New Board")
        self.saveAndRerender()

    def addSubTodo(self, lineIndex):
        originalLine = self.lines[lineIndex]
        indentMatch = re.match(r'^(\s*)', originalLine)
        indent = indentMatch.group(1) if indentMatch else "" 
        
        self.lines.insert(lineIndex + 1, f"{indent}  [ ] New Sub-Todo")
        self.saveAndRerender()

    def deleteLine(self, lineIndex):
        del self.lines[lineIndex]
        self.saveAndRerender()

    def toggleTodo(self, lineIndex):
        line = self.lines[lineIndex]
        if "[ ]" in line:
            self.lines[lineIndex] = line.replace("[ ]", "[x]", 1)
        elif "[x]" in line:
            self.lines[lineIndex] = line.replace("[x]", "[ ]", 1)
        elif "[~]" in line:
            self.lines[lineIndex] = line.replace("[~]", "[ ]", 1)
        
        self.checkParentCompletion(lineIndex)
        self.saveAndRerender()

    def cancelTodo(self, event, lineIndex):
        line = self.lines[lineIndex]
        self.lines[lineIndex] = line.replace("[ ]", "[~]", 1).replace("[x]", "[~]", 1)
        self.saveAndRerender()

    def checkParentCompletion(self, lineIndex):
        line = self.lines[lineIndex]
        match = re.match(r'^(\s*)', line)
        if not match: return
        
        currentIndent = len(match.group(1))
        if currentIndent == 0: return # Not a sub-todo

        parentLineIndex = -1
        for i in range(lineIndex - 1, -1, -1):
            parentLine = self.lines[i]
            parentMatch = re.match(r'^(\s*)', parentLine)
            if parentMatch:
                parentIndent = len(parentMatch.group(1))
                if parentIndent < currentIndent:
                    parentLineIndex = i
                    break
        
        if parentLineIndex == -1: return # No parent found

        allChildrenComplete = True
        parentIndent = len(re.match(r'^(\s*)', self.lines[parentLineIndex]).group(1)) # type: ignore
        for i in range(parentLineIndex + 1, len(self.lines)):
            childLine = self.lines[i]
            childMatch = re.match(r'^(\s*)', childLine)
            if childMatch:
                childIndent = len(childMatch.group(1))
                if childIndent > parentIndent:
                    if "[ ]" in childLine:
                        allChildrenComplete = False
                        break
                elif childIndent <= parentIndent:
                    break
        
        if allChildrenComplete:
            self.lines[parentLineIndex] = self.lines[parentLineIndex].replace("[ ]", "[x]")

    def saveAndRerender(self):
        self.saveChanges()
        self.render()

    def saveChanges(self):
        with open(self.filePath, "w", encoding='utf-8') as f:
            f.write('\n'.join(self.lines))
