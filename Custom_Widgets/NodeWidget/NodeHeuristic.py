from PyQt5.QtWidgets import QLabel

class NodeHeuristic(QLabel):
    def __init__(self, heuristic, parent):
        super().__init__(heuristic, parent)
        self.heuristic = heuristic
        self.parent = parent

    def mousePressEvent(self, event):
        self.parent.parent.clearNodeSelection()
        self.parent.parent.clearWeightSelection()
        self.parent.setNodeHeuristicSelectedStyle()