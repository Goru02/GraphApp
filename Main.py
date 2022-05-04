from PyQt5.QtWidgets import QWidget, QApplication
from Custom_Widgets.CanvasWidget.GraphCanvas import GraphCanvas
import sys

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        #
        #
        #
        # Place-holder GUI for future menus
        #
        #
        #
        self.WIDTH = 1600
        self.HEIGHT = 800
        self.initPosX = 160
        self.initPosY = 140

        self.topBar = QWidget(self)
        self.sideMenu = QWidget(self)
        self.canvas = GraphCanvas(self)

        self.topBar.WIDTH = self.WIDTH
        self.topBar.HEIGHT = 40
        self.topBar.initPosX = 0
        self.topBar.initPosY = 0

        self.sideMenu.WIDTH = self.WIDTH // 4
        self.sideMenu.HEIGHT = self.HEIGHT - self.topBar.HEIGHT
        self.sideMenu.initPosX = self.topBar.initPosX
        self.sideMenu.initPosY = self.topBar.initPosY + self.topBar.HEIGHT

        self.canvas.WIDTH = self.WIDTH - self.sideMenu.WIDTH
        self.canvas.HEIGHT = self.sideMenu.HEIGHT
        self.canvas.initPosX = self.topBar.initPosX + self.sideMenu.WIDTH
        self.canvas.initPosY = self.topBar.initPosY + self.topBar.HEIGHT

        self.initialize()

    def initialize(self):
        self.setGeometry(self.initPosX, self.initPosY, self.WIDTH, self.HEIGHT)

        self.topBar.setGeometry(self.topBar.initPosX, self.topBar.initPosY, self.topBar.WIDTH, self.topBar.HEIGHT)
        self.topBar.setStyleSheet('background-color: black;')

        self.sideMenu.setGeometry(self.sideMenu.initPosX, self.sideMenu.initPosY, self.sideMenu.WIDTH, self.sideMenu.HEIGHT)
        self.sideMenu.setStyleSheet('background-color: blue;')

        self.canvas.setGeometry(self.canvas.initPosX, self.canvas.initPosY, self.canvas.WIDTH, self.canvas.HEIGHT)

    def keyPressEvent(self, event):
        self.canvas.keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

