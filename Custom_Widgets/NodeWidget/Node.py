from PyQt5.QtWidgets import QFrame, QApplication
from PyQt5.QtCore import Qt
from Custom_Widgets.NodeWidget.styles import NodeStyles
from Custom_Widgets.NodeWidget.NodeName import NodeName
from Custom_Widgets.NodeWidget.NodeHeuristic import NodeHeuristic

class Node(QFrame):
    def __init__(self, parent, name, heuristic, x, y):
        super().__init__(parent)

        self.parent = parent
        self.name = name
        self.heuristic = heuristic
        self.x = x
        self.y = y
        self.radius = 50

        self.nameSelected = False
        self.heuristicSelected = False

        self.moveOffset = None

        self.initializeNode()
    
    def initializeNode(self):
        self.setGeometry(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)

        self.nodeName = NodeName(self.name, self)
        self.nodeName.setObjectName('nodeName')
        self.nodeName.setGeometry(28, 15, 50, 50)

        self.nodeHeuristic = NodeHeuristic(str(self.heuristic), self)
        self.nodeHeuristic.setObjectName('nodeHeuristic')
        self.nodeHeuristic.setGeometry(40, 70, 15, 15)

        self.setDefaultStyle()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and QApplication.keyboardModifiers() == Qt.ControlModifier:
            if self.parent.edgeNode1:
                self.parent.edgeNode2 = self
                self.parent.paintEdge()
            else:
                self.parent.edgeNode1 = self
            return
        
        self.parent.clearNodeSelection()
        self.parent.clearWeightSelection()
        self.setNodeNameSelectedStyle()

    def mouseMoveEvent(self, event):
        posX = event.windowPos().toPoint().x()
        posY = event.windowPos().toPoint().y()

        if not self.moveOffset:
            # Calculating the offset of the location of the mouse click from the radius
            # So that when moving a node, the node clips to the mouse location rather than
            # latching the center onto the mouse
            # Note that labels are moved by their top-left corner, not the center
            self.moveOffset = (posX - self.x + self.radius, posY - self.y + self.radius)

        newPosX = posX - self.moveOffset[0]
        newPosY = posY - self.moveOffset[1]
        self.x = newPosX + self.radius
        self.y = newPosY + self.radius

        self.move(newPosX, newPosY)

        self.parent.repaint() # Repainting the edge lines after moving the node

    def mouseReleaseEvent(self, event):
        self.moveOffset = None

    def keyPressEvent(self, event):
        keyValue = event.key()

        # ASCII values + weird pyqt5 values
        enter = 16777220
        delete = 16777223
        backSpace = 16777219
        a = 97
        z = 122
        A = 65
        Z = 90
        _0 = 48
        _9 = 57

        if keyValue == enter:
            self.setDefaultStyle()

        elif self.nameSelected:

            if keyValue == delete:
                self.parent.deleteNode(self)

            elif keyValue == backSpace:
                self.nodeName.setText(self.nodeName.text()[:-1])

            elif (keyValue >= A and keyValue <= Z) or (keyValue >= a and keyValue <= z) or (keyValue >= _0 and keyValue <= _9):
                name = self.nodeName.text()
                if name == '-':
                    self.nodeName.setText('')
                elif len(name) == 2: # Max input 2 characters cause I can't be bothered to make it responsive
                    return
                self.nodeName.setText(self.nodeName.text()+event.text())

        elif self.heuristicSelected:

            if keyValue == backSpace:
                self.nodeHeuristic.setText(self.nodeHeuristic.text()[:-1])

            elif keyValue >= _0 and keyValue <= _9:
                heuristic = self.nodeHeuristic.text()
                if heuristic == '0':
                    self.nodeHeuristic.setText('')
                elif len(heuristic) == 2:
                    return
                self.nodeHeuristic.setText(self.nodeHeuristic.text()+event.text())

    def setDefaultStyle(self):
        self.setStyleSheet(NodeStyles.defaultStyle)
        self.nameSelected = False
        self.heuristicSelected = False

    def setNodeNameSelectedStyle(self):
        self.setStyleSheet(NodeStyles.nodeNameSelectedStyle)
        self.nameSelected = True
        self.heuristicSelected = False

    def setNodeHeuristicSelectedStyle(self):
        self.setStyleSheet(NodeStyles.nodeHeuristicSelectedStyle)
        self.heuristicSelected = True
        self.nameSelected = False