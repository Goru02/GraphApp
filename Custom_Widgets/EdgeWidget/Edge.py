from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPoint
from Custom_Widgets.EdgeWidget.styles import edgeStyles
from math import sqrt

class Edge(QLabel):
    def __init__(self, parent, weight, node1, node2, directed = False):
        super().__init__(str(weight), parent)

        self.parent = parent
        self.weight = weight
        self.node1 = node1
        self.node2 = node2
        self.directed = directed

        self.width = self.height = 30   # Weight bubble dimensions
        self.selected = False
        self.positionRatio = 0.5        # The ratio of the position of the weight bubble on the edge line

        self.initializeEdge()

    def initializeEdge(self):
        self.x1, self.y1, self.x2, self.y2 = [round(n) for n in self.computeIntersections(self.node1, self.node2)]

        self.weightX, self.weightY = (round((self.x1 + self.x2) / 2), round((self.y1 + self.y2) / 2))
        self.setGeometry(self.weightX-18, self.weightY-18, self.width, self.height)

        self.setDefaultStyle()

    def mousePressEvent(self, event):       # Selecting edge weight
        self.parent.clearNodeSelection()
        self.parent.clearWeightSelection()
        
        self.setWeightSelectedStyle()

    def mouseMoveEvent(self, event):        # Moving weight bubble along the edge Line
        zeroDivisionCoefficient = 0.0001
        weightBubbleRadius = 18
        restriction = weightBubbleRadius
        verticalityStartSlope = 1.3

        m = (self.y1 - self.y2) / (self.x1 - self.x2 + zeroDivisionCoefficient)
        
        globalCanvasPos = self.parent.mapToGlobal(QPoint(0, 0))
        if m > verticalityStartSlope or m < -verticalityStartSlope:     # Switching to working with y coordinates when the line
            posY = event.globalY() - globalCanvasPos.y()                # gets more vertical (delta x becomes very small)
            posX = self.translateYtoX(posY)                             # in order to avoid shaking motion & lack of movability

            edgeWidth = abs(self.y1 - self.y2)

            if ((self.y1 > self.y2 and posY > self.y2 + restriction and posY < self.y1 - restriction)
                or (self.y1 < self.y2 and posY > self.y1 + restriction and posY < self.y2 - restriction)):

                self.move(posX-weightBubbleRadius, posY-weightBubbleRadius)
                self.positionRatio = abs(self.y1 - posY) / edgeWidth
        else:
            posX = event.globalX() - globalCanvasPos.x()
            posY = self.translateXtoY(posX)

            edgeWidth = abs(self.x1 - self.x2)

            if ((self.x1 > self.x2 and posX > self.x2 + restriction and posX < self.x1 - restriction)
                or (self.x1 < self.x2 and posX > self.x1 + restriction and posX < self.x2 - restriction)):

                self.move(posX-weightBubbleRadius, posY-weightBubbleRadius)
                self.positionRatio = abs(self.x1 - posX) / edgeWidth

        self.movingWeight = False

    def keyPressEvent(self, event):         # Inserting a weight value or deleting
        keyValue = event.key()
       
        enter = 16777220
        delete = 16777223
        backSpace = 16777219
        _0 = 48
        _9 = 57

        if self.selected:
            if keyValue == enter:
                self.setDefaultStyle()

            elif keyValue == delete:
                self.parent.deleteEdge(self)

            elif keyValue == backSpace:
                self.setText(self.text()[:-1])

            elif keyValue >= _0 and keyValue <= _9:
                heuristic = self.text()
                if heuristic == '0':
                    self.setText('')
                elif len(heuristic) == 2:
                    return
                self.setText(self.text()+event.text())
                    
    def setDefaultStyle(self):              # Setting the weight bubble default style and deselcting
        self.setStyleSheet(edgeStyles.defaultStyle)
        self.selected = False

    def setWeightSelectedStyle(self):       # Setting the weight bubble selected style and selecting
        self.setStyleSheet(edgeStyles.weightSelectedStyle)
        self.selected = True

    def computeIntersections(self, node1, node2):   # Finding the line intersection points of the two nodes
        border = node1.frameWidth()                 # And the line going through their centers, to find the
        a, b = node1.x + border, node1.y + border   # Edge drawing points
        c, d = node2.x + border, node2.y + border
        r1 = node1.radius + border
        r2 = node2.radius + border

        zeroDivisionCoefficient = 0.0001

        m = (d - b) / (c - a + zeroDivisionCoefficient)

        nodeOneIntersections = self.findCircleLineIntersections(m, a, b, r1, a, b)
        nodeTwoIntersections = self.findCircleLineIntersections(m, c, d, r2, c, d)

        distances = {}
        for point1 in nodeOneIntersections:
            for point2 in nodeTwoIntersections:
                x1, y1 = point1[0], point1[1]
                x2, y2 = point2[0], point2[1]

                distance = self.distanceBetweenTwoPoints(x1, y1, x2, y2)

                distances[distance] = (x1, y1, x2, y2)

        return distances[min(distances.keys())]

    def findCircleLineIntersections(self, lineSlope, lineX, lineY, circleRadius, radiusX, radiusY):     # Math helper function
        g = lineSlope**2 + 1

        a = g
        b = -2 * (radiusX + lineSlope * (lineSlope * lineX - lineY + radiusY))
        c = radiusX**2 + (lineSlope * lineX)**2 - 2 * lineSlope * lineX * lineY + 2 * lineSlope * lineX * radiusY + lineY**2 - 2 * lineY * radiusY + radiusY**2 - circleRadius**2

        x1 = (-b + sqrt(b**2 - 4 * a * c)) / (2 * a)
        x2 = (-b - sqrt(b**2 - 4 * a * c)) / (2 * a)
        y1 = lineSlope * (x1 - lineX) + lineY
        y2 = lineSlope * (x2 - lineX) + lineY

        return (x1, y1), (x2, y2)

    def distanceBetweenTwoPoints(self, x1, y1, x2, y2):     # Math helper function
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def updateCoordinates(self):            # Updating the edge coordinates and weight bubble position along the edge line
        self.x1, self.y1, self.x2, self.y2 = [round(n) for n in self.computeIntersections(self.node1, self.node2)]

        zeroDivisionCoefficient = 0.0001
        verticalityStartSlope = 1.3
        weightBubbleRadius = 18

        m = (self.y1 - self.y2) / (self.x1 - self.x2 + zeroDivisionCoefficient)

        if m > verticalityStartSlope or m < -verticalityStartSlope:     # Switching to working with y coordinates when the line
            sign = 1                                                    # gets more vertical (delta x becomes very small)
            if self.y1 > self.y2:                                       # in order to avoid shaking motion & lack of movability
                sign = -1
            posY = round(self.y1 + sign * self.positionRatio * abs(self.y1 - self.y2))
            posX = self.translateYtoX(posY)
            self.move(posX-weightBubbleRadius, posY-weightBubbleRadius)
        else:
            sign = 1
            if self.x1 > self.x2:
                sign = -1
            posX = round(self.x1 + sign * self.positionRatio * abs(self.x1 - self.x2))
            posY = self.translateXtoY(posX)
            self.move(posX-weightBubbleRadius, posY-weightBubbleRadius)

    def translateXtoY(self, x):             # Math helper function
        zeroDivisionCoefficient = 0.0001
        m = (self.y1 - self.y2) / (self.x1 - self.x2 + zeroDivisionCoefficient)
        return round(m*(x - self.x1) + self.y1)

    def translateYtoX(self, y):             # Math helper function
        zeroDivisionCoefficient = 0.0001
        m = (self.y1 - self.y2) / (self.x1 - self.x2 + zeroDivisionCoefficient)
        return round((y - self.y1)/m + self.x1)

    def getArrowPoints(self):               # Finding the 3 points on which the arrow should be drawn
        triangleBase = 15
        triangleHeight = 18

        zeroDivisionCoefficient = 0.0001

        m = (self.y1 - self.y2 + zeroDivisionCoefficient) / (self.x1 - self.x2 + zeroDivisionCoefficient)

        intersectionPoints = self.findCircleLineIntersections(m, self.x2, self.y2, triangleHeight, self.x2, self.y2)
        
        x1, y1 = self.x2, self.y2   # First point is the node2 edge line intersection point
        if abs(self.node2.x - self.node1.x) < 3: # Edge is vertical with a margin
            sign = 1                             # with a margin of 3px (To fix a visual bug)
            if self.node2.y > self.node1.y:
                sign = -1

            x2, y2 = self.x2 + triangleBase/2, self.y2 + sign * triangleHeight
            x3, y3 = self.x2 - triangleBase/2, self.y2 + sign * triangleHeight
        

        elif self.node2.y == self.node1.y:      # Edge is horizontal
            sign = 1
            if self.node2.x > self.node1.x:
                sign = -1
            x2, y2 = self.x2 + sign * triangleHeight, self.y2 - triangleBase/2
            x3, y3 = self.x2 + sign * triangleHeight, self.y2 + triangleBase/2
        
        else:
            if intersectionPoints[0][0] > intersectionPoints[1][0]:
                xMax, yMax = intersectionPoints[0]
                xMin, yMin = intersectionPoints[1]
            else:
                xMax, yMax = intersectionPoints[1]
                xMin, yMin = intersectionPoints[0]

            if self.node2.x > self.node1.x:
                trianglePoints = self.findCircleLineIntersections(-1/m, xMin, yMin, triangleBase/2, xMin, yMin)
            else:
                trianglePoints = self.findCircleLineIntersections(-1/m, xMax, yMax, triangleBase/2, xMax, yMax)

            x2, y2 = trianglePoints[0]
            x3, y3 = trianglePoints[1]

        return [(x1, y1), (x2, y2), (x3, y3)]



            
            


