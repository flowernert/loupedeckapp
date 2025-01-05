

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from PIL import Image, ImageColor



class Widget (QPushButton):
  def __init__(self, text):
    QPushButton.__init__(self, text)
    self.setFixedSize(90, 90)
    self.cmd_edit = QPushButton("cmd")
    self.cmd_edit.setFixedSize(45, 20)
    vlayout = QVBoxLayout()
    vlayout.addWidget(self.cmd_edit, alignment=Qt.AlignRight|Qt.AlignTop)
    self.setLayout(vlayout)
    

class Loupedeck (QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    
    layout = QGridLayout()
    for row in range(3):
      encoderL = Encoder("enc. " + str(row+1) + " Left")
      layout.addWidget(encoderL, row, 0)

      displayL = Display("dis." + str(row+1) + " Left")
      layout.addWidget(displayL, row, 1)

      buttons = [TouchButton("but. " + str(row+1) + " " + str(col+1)) for col in range(4)]
      _ = [layout.addWidget(buttons[col], row, col+2) for col in range(4)]

      displayR = Display("dis. " + str(row+1) + " Right")
      layout.addWidget(displayR, row, 6)

      encoderR = Encoder("enc. " + str(row+1) + " Right")
      layout.addWidget(encoderR, row, 7)

    pages = [ModeButton(str(i)) for i in range(8)]
    _ = [layout.addWidget(pages[i], 4, i) for i in range(8)]

    self.setLayout(layout)

    
class Display (Widget):
  def __init__(self, text):
    super().__init__(text)
    self.img_edit = QPushButton("img")
    self.img_edit.setFixedSize(45, 20)
    layout = self.layout()
    layout.addWidget(self.img_edit, alignment=Qt.AlignRight|Qt.AlignBottom)
    self.setLayout(layout)


class Encoder (Widget):
  def __init__(self, text):
    super().__init__(text)

    
class TouchButton (Display):
  def __init__(self, text): 
    super().__init__(text)
    

class Display (Display):
  def __init__(self, text):
    super().__init__(text)


class ModeButton (Widget):
  def __init__(self, text):
    super().__init__(text)

    
    

