defaultStyle = """
    QFrame {
        border: 3px solid black;
        min-height: 100px;
        min-width: 100px;
        border-radius: 53px;
    }

    QFrame#nodeName {
        qproperty-alignment: AlignCenter;
        border: 0px;
        font-size: 30px;
        min-height: 50px;
        min-width: 50px;
    }

    QFrame#nodeHeuristic {
        min-height: 20px;
        min-width: 20px;
        border-radius: 12px;
        qproperty-alignment: AlignCenter;
        font-size: 15px;
    }
"""

nodeNameSelectedStyle = """
    QFrame {
        background-color: #fcc2d4;
        border: 3px solid #5c162c;
        min-height: 100px;
        min-width: 100px;
        border-radius: 53px;
    }

    QFrame#nodeName {
        qproperty-alignment: AlignCenter;
        border: 0px;
        font-size: 30px;
        min-height: 50px;
        min-width: 50px;
        color: #5c162c;
    }

    QFrame#nodeHeuristic {
        height:10px;
        width:10px;
        min-height: 20px;
        min-width: 20px;
        border-radius: 12px;
        qproperty-alignment: AlignCenter;
        font-size: 15px;
        background-color: white;
        border-color: black;
    }
"""

nodeHeuristicSelectedStyle = """
    QFrame {
        border: 3px solid black;
        min-height: 100px;
        min-width: 100px;
        border-radius: 53px;
    }

    QFrame#nodeName {
        qproperty-alignment: AlignCenter;
        border: 0px;
        font-size: 30px;
        min-height: 50px;
        min-width: 50px;
    }

    QFrame#nodeHeuristic {
        height:10px;
        width:10px;
        min-height: 20px;
        min-width: 20px;
        border-radius: 12px;
        qproperty-alignment: AlignCenter;
        font-size: 15px;
        color: #5c162c;
        border-color: #5c162c;
        background-color: #fcc2d4;
    }
"""