import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFrame

def createSidebar():
    sidebarFrame = QFrame()
    sidebarFrame.setFixedWidth(200)
    sidebarFrame.setStyleSheet("""
        background-color: #3B3B3B;
        padding: 10px;
        border-radius: 15px;
    """)
    return sidebarFrame

def createMainContent():
    mainContent = QWidget()
    mainContent.setStyleSheet("background-color: #363636;")
    return mainContent

def setupUi(mainWindow):
    mainWindow.setWindowTitle("Noteted")
    mainWindow.setGeometry(100, 100, 800, 600)
    mainWindow.setStyleSheet("background-color: #363636;")

    centralWidget = QWidget()
    mainWindow.setCentralWidget(centralWidget)

    layout = QHBoxLayout(centralWidget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    sidebar = createSidebar()
    mainContent = createMainContent()

    layout.addWidget(sidebar)
    layout.addWidget(mainContent)

def initializeNoteted():
    app = QApplication(sys.argv)
    window = QMainWindow()
    setupUi(window)
    window.show()
    sys.exit(app.exec())