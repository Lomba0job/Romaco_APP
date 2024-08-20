from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class RoundedRect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class QCustom3CirclesLoader(QFrame):
    def __init__(
            self, 
            parent=None,
            default_color=QColor("#5D5D5D"),
            active_color=QColor("#E74C3C"),
            penWidth=20,
            animationDuration=400,
            size=140
            ):
        QFrame.__init__(self, parent=parent)
        
        self.size = size
        self.scale_factor = size / 140
        
        self.setFixedSize(size, size)

        self.default_color = default_color
        self.active_color = active_color
        self.colors = [default_color, default_color, default_color]
        self.penWidth = int(penWidth)
        self.animationDuration = animationDuration

        self.initRects()
        
        self.startAnimations()
    
    def initRects(self):
        x = self.penWidth/2
        rect_size = int(40 * self.scale_factor)
        rect_gap = int(80 * self.scale_factor)
        self.rectsList = [
            RoundedRect(x, x, rect_size, rect_size),
            RoundedRect(x+rect_gap, x, rect_size, rect_size),
            RoundedRect(x, x+rect_gap, rect_size, rect_size)
        ]
    
    def getVariantAnimation(self):
        animation = QVariantAnimation(self)
        animation.setDuration(self.animationDuration)
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        return animation

    def initMoveDownAnimation(self):
        self.moveDownGP = QSequentialAnimationGroup(self)

        animation = self.getVariantAnimation()
        animation.setStartValue(int(40 * self.scale_factor))
        animation.setEndValue(int(120 * self.scale_factor))
        animation.valueChanged.connect(self.moveDownUpdateH)
        self.moveDownGP.addAnimation(animation)

        animation = self.getVariantAnimation()
        animation.setStartValue(int(10 * self.scale_factor))
        animation.setEndValue(int(90 * self.scale_factor))
        animation.valueChanged.connect(self.moveDownUpdateY)
        self.moveDownGP.addAnimation(animation)
    
    def initMoveRightAnimation(self):
        self.moveRightGP = QSequentialAnimationGroup(self)

        animation = self.getVariantAnimation()
        animation.setStartValue(int(40 * self.scale_factor))
        animation.setEndValue(int(120 * self.scale_factor))
        animation.valueChanged.connect(self.moveRightUpdateW)
        self.moveRightGP.addAnimation(animation)

        animation = self.getVariantAnimation()
        animation.setStartValue(int(10 * self.scale_factor))
        animation.setEndValue(int(90 * self.scale_factor))
        animation.valueChanged.connect(self.moveRightUpdateX)
        self.moveRightGP.addAnimation(animation)

    def initMoveUpAnimation(self):
        self.moveUpGP = QSequentialAnimationGroup(self)

        animation = QVariantAnimation(self)
        animation.setDuration(self.animationDuration)
        animation.setStartValue(int(90 * self.scale_factor))
        animation.setEndValue(int(10 * self.scale_factor))
        animation.valueChanged.connect(self.moveUpUpdateY)
        self.moveUpGP.addAnimation(animation)

        animation = self.getVariantAnimation()
        animation.setStartValue(int(120 * self.scale_factor))
        animation.setEndValue(int(40 * self.scale_factor))
        animation.valueChanged.connect(self.moveUpUpdateH)
        self.moveUpGP.addAnimation(animation)

    def initMoveLeftAnimation(self):
        self.moveLeftGP = QSequentialAnimationGroup(self)

        animation = self.getVariantAnimation()
        animation.setStartValue(int(90 * self.scale_factor))
        animation.setEndValue(int(10 * self.scale_factor))
        animation.valueChanged.connect(self.moveLeftUpdateX)
        self.moveLeftGP.addAnimation(animation)

        animation = self.getVariantAnimation()
        animation.setStartValue(int(120 * self.scale_factor))
        animation.setEndValue(int(40 * self.scale_factor))
        animation.valueChanged.connect(self.moveLeftUpdateH)
        self.moveLeftGP.addAnimation(animation)

    def setActiveColor(self, index):
        self.colors = [self.default_color] * 3
        self.colors[index] = self.active_color
        self.update()

    def moveDownUpdateH(self, newValue):
        self.setActiveColor(1)
        self.rectsList[1].h = newValue
        self.update()
    
    def moveDownUpdateY(self, newValue):
        self.rectsList[1].y = newValue
        self.rectsList[1].h = int(130 * self.scale_factor) - newValue
        self.update()
    
    def moveRightUpdateW(self, newValue):
        self.setActiveColor(0)
        self.rectsList[0].w = newValue
        self.update()

    def moveRightUpdateX(self, newValue):
        self.rectsList[0].x = newValue
        self.rectsList[0].w = int(130 * self.scale_factor) - newValue
        self.update()

    def moveUpUpdateY(self, newValue):
        self.setActiveColor(2)
        self.rectsList[2].y = newValue
        self.rectsList[2].h = int(130 * self.scale_factor) - newValue
        self.update()

    def moveUpUpdateH(self, newValue):
        self.rectsList[2].h = newValue
        self.update()

    def moveLeftUpdateX(self, newValue):
        self.setActiveColor(1)
        self.rectsList[1].x = newValue
        self.rectsList[1].w = int(130 * self.scale_factor) - newValue
        self.update()

    def moveLeftUpdateH(self, newValue):
        self.rectsList[1].w = newValue
        self.update()

    def startAnimations(self):
        self.initMoveDownAnimation()
        self.initMoveRightAnimation()
        self.initMoveUpAnimation()
        self.initMoveLeftAnimation()
        gp = QSequentialAnimationGroup(self)
        gp.addAnimation(self.moveDownGP)
        gp.addAnimation(self.moveRightGP)
        gp.addAnimation(self.moveUpGP)
        gp.addAnimation(self.moveLeftGP)
        self.moveLeftGP.finished.connect(self.finished)
        gp.setLoopCount(-1)  # Loop infinitely
        gp.start()
    
    def finished(self):
        self.rectsList = [self.rectsList[2], self.rectsList[0], self.rectsList[1]]

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        x = self.penWidth/2
        for i, rect in enumerate(self.rectsList):
            pen = QPen()
            pen.setColor(self.colors[i])
            pen.setWidth(self.penWidth)
            painter.setPen(pen)
            painter.drawRoundedRect(
                int(rect.x), int(rect.y), int(rect.w), int(rect.h), 
                20.0 * self.scale_factor, 20.0 * self.scale_factor
            )
        painter.end()