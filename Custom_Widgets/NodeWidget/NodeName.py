from PyQt5.QtWidgets import QLabel

class NodeName(QLabel):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.name = name
        self.parent = parent

    def mousePressEvent(self, event):
        self.parent.mousePressEvent(event)