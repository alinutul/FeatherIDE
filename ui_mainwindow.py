from PySide6.QtCore import QCoreApplication, QRect, Qt, QMetaObject
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QMenuBar, QMenu, QStatusBar,
    QTreeView, QTextEdit, QSplitter, QVBoxLayout, QFileSystemModel, QFileDialog,
    QMessageBox, QTabWidget, QLineEdit, QPushButton, QHBoxLayout
)

class Ui_MainWindow(object):
    """
    Generated UI setup for the main window, defining actions, menus, and basic layout elements.
    """
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 575)
        
        # Define actions for file, edit, and template menus
        self.actionNewProject = QAction(MainWindow)
        self.actionNewProject.setObjectName(u"actionNewProject")
        self.actionNewFile = QAction(MainWindow)
        self.actionNewFile.setObjectName(u"actionNewFile")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionCut = QAction(MainWindow)
        self.actionCut.setObjectName(u"actionCut")
        self.actionCopy = QAction(MainWindow)
        self.actionCopy.setObjectName(u"actionCopy")
        self.actionPaste = QAction(MainWindow)
        self.actionPaste.setObjectName(u"actionPaste")
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")

        # Template actions
        self.actionLoadTemplate = QAction(MainWindow)
        self.actionLoadTemplate.setObjectName(u"actionLoadTemplate")
        self.actionSaveTemplate = QAction(MainWindow)
        self.actionSaveTemplate.setObjectName(u"actionSaveTemplate")

        # Build actions
        self.actionBuild = QAction(MainWindow)
        self.actionBuild.setObjectName(u"actionBuild")
        self.actionBuildAndRun = QAction(MainWindow)
        self.actionBuildAndRun.setObjectName(u"actionBuildAndRun")

        # Competition actions
        self.actionEnableCompetition = QAction(MainWindow)
        self.actionEnableCompetition.setObjectName(u"actionEnableCompetition")
        self.actionDisableCompetition = QAction(MainWindow)
        self.actionDisableCompetition.setObjectName(u"actionDisableCompetition")


        # Central Widget
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu Bar setup
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuTemplate = QMenu(self.menubar) # New Template menu
        self.menuTemplate.setObjectName(u"menuTemplate")
        self.menuBuild = QMenu(self.menubar) # New Build menu
        self.menuBuild.setObjectName(u"menuBuild") # Corrected object name syntax
        self.menuCompetition = QMenu(self.menubar) # New Competition menu
        self.menuCompetition.setObjectName(u"menuCompetition")
        MainWindow.setMenuBar(self.menubar)
        
        # Status Bar setup
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Add actions to menus and menus to menu bar
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTemplate.menuAction()) 
        self.menubar.addAction(self.menuBuild.menuAction()) # Add Build menu to menubar
        self.menubar.addAction(self.menuCompetition.menuAction()) # Add Competition menu to menubar

        self.menuFile.addAction(self.actionNewProject) 
        self.menuFile.addAction(self.actionNewFile) 
        self.menuFile.addSeparator() 
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)

        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionDelete)

        # Add actions to Template menu
        self.menuTemplate.addAction(self.actionLoadTemplate)
        self.menuTemplate.addAction(self.actionSaveTemplate)

        # Add actions to Build menu
        self.menuBuild.addAction(self.actionBuild)
        self.menuBuild.addAction(self.actionBuildAndRun)
        
        # Add actions to Competition menu
        self.menuCompetition.addAction(self.actionEnableCompetition)
        self.menuCompetition.addAction(self.actionDisableCompetition)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Sets the display text for UI elements.
        """
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNewProject.setText(QCoreApplication.translate("MainWindow", u"New Project...", None))
        self.actionNewFile.setText(QCoreApplication.translate("MainWindow", u"New File...", None)) 
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save...", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        self.actionCut.setText(QCoreApplication.translate("MainWindow", u"Cut", None))
        self.actionCopy.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.actionPaste.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))

        # Template action texts
        self.actionLoadTemplate.setText(QCoreApplication.translate("MainWindow", u"Load Template...", None))
        self.actionSaveTemplate.setText(QCoreApplication.translate("MainWindow", u"Save Template...", None))

        # Build action texts
        self.actionBuild.setText(QCoreApplication.translate("MainWindow", u"Build", None))
        self.actionBuildAndRun.setText(QCoreApplication.translate("MainWindow", u"Build and Run", None))

        # Competition action texts
        self.actionEnableCompetition.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.actionDisableCompetition.setText(QCoreApplication.translate("MainWindow", u"Disable", None))

        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuTemplate.setTitle(QCoreApplication.translate("MainWindow", u"Template", None)) 
        self.menuBuild.setTitle(QCoreApplication.translate("MainWindow", u"Build", None)) # Title for new Build menu
        self.menuCompetition.setTitle(QCoreApplication.translate("MainWindow", u"Competition", None))


