import LdDialog
from LdDialog import ConfigCmd, ConfigImg
from LdConfiguration import LdConfiguration

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout
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
    self.config = LdConfiguration()
    
    layout = QGridLayout()
    for row in range(3):
      encoderL = Encoder("enc. " + str(row+1) + " Left")
      encoderL.setObjectName("enc%sL" % (row+1))
      encoderL.cmd_edit.clicked.connect(self.choose_action)
      layout.addWidget(encoderL, row, 0)

      displayL = Display("dis." + str(row+1) + " Left")
      displayL.setObjectName("dis%sL" % (row+1))
      displayL.cmd_edit.clicked.connect(self.choose_action)
      displayL.img_edit.clicked.connect(self.choose_image)
      layout.addWidget(displayL, row, 1)

      buttons = [TouchButton("but. " + str(row+1) + " " + str(col+1)) for col in range(4)]
      _ = [buttons[col].setObjectName("tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [buttons[col].cmd_edit.clicked.connect(self.choose_action) for col in range(4)]
      _ = [buttons[col].img_edit.clicked.connect(self.choose_image) for col in range(4)]
      _ = [layout.addWidget(buttons[col], row, col+2) for col in range(4)]

      displayR = Display("dis. " + str(row+1) + " Right")
      displayR.setObjectName("dis%sL" % (row+1))
      displayR.cmd_edit.clicked.connect(self.choose_action)
      displayR.img_edit.clicked.connect(self.choose_image)
      layout.addWidget(displayR, row, 6)

      encoderR = Encoder("enc. " + str(row+1) + " Right")
      encoderR.setObjectName("enc%sR" % (row+1))
      layout.addWidget(encoderR, row, 7)
      encoderR.cmd_edit.clicked.connect(self.choose_action)

    pages = [ModeButton(str(i)) for i in range(8)]
    _ = [layout.addWidget(pages[i], 4, i) for i in range(8)]

    self.setLayout(layout)
    
  def choose_action(self):
    sender_id = self.sender().parent().objectName()
    dialog = ConfigCmd(self.sender().parent())
    print("choose_action called")
    if (dialog.exec()):
      self.config.actions[sender_id] = dialog.user_cmd.text()
    
    
  def choose_image(self):
    sender_id = self.sender().parent().objectName()
    dialog = ConfigImg(self.sender().parent())
    print("choose_image called")
    if (dialog.exec()):
      path = dialog.user_img.text()
      self.config.images[sender_id] = path
      self.sender().parent().setStyleSheet("QPushButton#%s { background-image: url(%s);}" % (sender_id, path))

    
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

