from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QBrush, QPolygonF
from PyQt5.QtCore import Qt, QPointF
from Custom_Widgets.NodeWidget.Node import Node
from Custom_Widgets.EdgeWidget.Edge import Edge

class GraphCanvas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.nodes = []
        self.edges = []

        # Edge queuing
        self.edgeNode1 = None
        self.edgeNode2 = None

    def paintEvent(self, event):            # Painting the edge lines over their calculated positions
        for edge in self.edges:
            edge.updateCoordinates()
            qp = QPainter()
            qp.begin(self)
            qp.setRenderHints(QPainter.Antialiasing)
            qp.setPen(QPen(Qt.black, 2))

            qp.drawLine(edge.x1, edge.y1, edge.x2, edge.y2)

            if edge.directed:
                points = [QPointF(point[0], point[1]) for point in edge.getArrowPoints()]
                qp.setBrush(QBrush(Qt.black))
                qp.drawPolygon(QPolygonF(points))

    def mousePressEvent(self, event):       # Drawing nodes on shift+click / deselecting node and edge selections
        modifiers = QApplication.keyboardModifiers()

        if event.buttons() == Qt.LeftButton and modifiers == Qt.ShiftModifier:
            node = Node(self, '-', 0, event.x(), event.y())
            self.nodes.append(node)
            node.show()

        self.clearNodeSelection()
        self.clearWeightSelection()

    def keyPressEvent(self, event):         # Passing key presses to be handled by the nodes and edges
        for node in self.nodes:
            node.keyPressEvent(event) 

        for edge in self.edges:
            edge.keyPressEvent(event)
    
    def clearNodeSelection(self):           # Resetting the style of all nodes
        for node in self.nodes:
            node.setDefaultStyle()

    def clearWeightSelection(self):         # Resetting the style of all edge weights
        for edge in self.edges:
            edge.setDefaultStyle()

    def paintEdge(self):                    # Function called when an edge is to be created (painted) through ctrl+click over two different nodes
        if self.edgeNode1 != self.edgeNode2:
            currentEdge = Edge(self, 0, self.edgeNode1, self.edgeNode2, True)
            self.edges.append(currentEdge)
            currentEdge.show()
            self.edgeNode1 = None
            self.edgeNode2 = None
            
            self.repaint()

    def deleteNode(self, node):             # Deleting a node from the nodes list property as well as the GUI and deleting the edges it was connected to
        for i in range(len(self.nodes)):
            if self.nodes[i] == node:
                self.nodes[i].setParent(None)
                self.nodes.pop(i)
                break

        self.deleteNodeRelatedEdges(node)

    def deleteNodeRelatedEdges(self, node): # Deleting all the edges connected to a given node
        deletedIndices = []
        for i in range(len(self.edges)):
            if self.edges[i].node1 == node or self.edges[i].node2 == node:
                self.edges[i].setParent(None)
                deletedIndices.append(i)
        
        for index in sorted(deletedIndices, reverse=True): # Delete the largest indices first so that no smaller index is shifted
            self.edges.pop(index)

        self.repaint()

    def deleteEdge(self, edge):             # Deleting an edge from the edge list property as well as updating the paintEvent to remove it from the GUI
        for i in range(len(self.edges)):
            if self.edges[i] == edge:
                self.edges[i].setParent(None)
                self.edges.pop(i)
                break

        self.repaint()