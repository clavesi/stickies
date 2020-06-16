from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTextEdit, QPushButton, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont, QMouseEvent
from PyQt5.QtCore import Qt, pyqtSlot, QPoint, pyqtSignal
import sys, random, settings

#! See if I can find a way to save the stickies if you shut your computer off, might need to be executable
#! ...... definitely needs to be executable since its running of CMD right now
#! Make this an executable, nice thing to learn

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.title = 'sticky'
        self.setWindowTitle(self.title)

        # Set window position
        self.left = 100 + settings.OFFSETX
        self.top = 100 + settings.OFFSETY
        self.width = 250
        self.height = 250
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumWidth(self.width)
        self.setMinimumHeight(self.height)
        self.setMaximumWidth(self.width)
        self.setMaximumHeight(self.height)

        # Get if the mouse is being pressed down
        self.pressing = False

        # Button padding
        self.toppadding = 25

        # Remove title bar, this is the reason for the Mouse events
        # The title bar was the only way to move the window, so I had to design my own way
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Pick random from sticky note colors, just to spice up your sticky notes
        self.colors = ['#ff7eb9', '#ff65a3', '#7afcff', '#feff9c', '#fff740']
        self.setColor = random.choice(self.colors)
        self.setStyleSheet(f'background-color: {self.setColor};border: 3px solid {self.setColor};')

        self.initUI()
 
    def initUI(self):
        # Create textbox
        self.textbox = QTextEdit(self)
        self.textbox.move(0, self.toppadding)
        self.textbox.resize(self.width, self.height - self.toppadding)

        # Set textbox font
        self.textbox.setFont(QFont('Inter', 12))

        # Set exit button
        self.exitbutton = QPushButton('X', self)
        self.exitbutton.setGeometry(self.width - 35, 0, 35, 35)
        self.exitbutton.setFont(QFont('Arial', 16))
        self.exitbutton.clicked.connect(self.exitButton)

        # Set add sticky button
        self.addsticky = QPushButton('+', self)
        self.addsticky.setGeometry(self.width - 75, 0, 34, 34)
        self.addsticky.setFont(QFont('Arial', 16))
        self.addsticky.clicked.connect(self.addSticky)
        
        # Part of addSticky()
        self.dialogs = list()

    @pyqtSlot()
    def exitButton(self):
        self.destroy()

        # Subtract one to number of stickies
        settings.NUMSTICKIES = settings.NUMSTICKIES - 1

        # Usually, you would use something like sys.exit(app.exec_()),
        # but this closes all instances. self.destroy() just destroys that window.
        # So sys.exit() is only called if all the windows are closed, otherwise the program remains running
        if settings.NUMSTICKIES == 0:
            sys.exit(app.exec_())

    @pyqtSlot()
    def addSticky(self):
        # This is set here so that the initial window is not also offset
        settings.OFFSETX = self.geometry().x() - 100
        settings.OFFSETY = self.geometry().y() - 50

        # Create another instance of a sticky
        dialog = Window(self)
        self.dialogs.append(dialog)
        dialog.show()

        # Add one to number of stickies
        settings.NUMSTICKIES = settings.NUMSTICKIES + 1

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Store original position to allow window to follow where you first clicked
            self.originalpos = [event.x(), event.y()]
            self.pressing = True
 
    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.LeftButton) and self.pressing:
            # Set window geometry to follow original mouse position

            # (event.x/y() gets the position relative to the window, so the absolute position is it's position on the screen)
            # Gets current absolute mouse position then subtracts originalpos to offset following
            # to look like it's dragging where you first clicked
            xdiff = (self.geometry().x() + event.x()) - self.originalpos[0]
            ydiff = (self.geometry().y() + event.y()) - self.originalpos[1]

            self.setGeometry(xdiff, ydiff, self.width, self.height)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressing = False
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()