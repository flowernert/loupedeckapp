import LdDialog
import LdApp

from LdDialog import ConfigCmd, ConfigImg
from LdConfiguration import LdConfiguration

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QApplication
from PyQt5.QtCore import Qt
from PIL import Image, ImageColor


class Loupedeck (QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.config = LdConfiguration()

    layout = QGridLayout()
    for row in range(3):
      encoderL = Encoder("enc. " + str(row+1) + " Left")
      encoderL.push_cmd_edit.setObjectName("enc%sL" % (row+1))
      encoderL.push_cmd_edit.clicked.connect(self.choose_action)
      encoderL.left_cmd_edit.clicked.connect(self.choose_action)
      encoderL.left_cmd_edit.setObjectName("enc%sL-l" % (row+1))
      encoderL.right_cmd_edit.clicked.connect(self.choose_action)
      encoderL.right_cmd_edit.setObjectName("enc%sL-r" % (row+1))
      layout.addWidget(encoderL, row, 0)

      displayL = TDisplay("dis." + str(row+1) + " Left")
      displayL.setObjectName("root_dis%sL"% (row+1))
      displayL.cmd_edit.setObjectName("dis%sL" % (row+1))
      displayL.cmd_edit.clicked.connect(self.choose_action)
      displayL.img_edit.setObjectName("dis%sL" % (row+1))
      displayL.img_edit.clicked.connect(self.choose_image)
      layout.addWidget(displayL, row, 1, alignment=Qt.AlignRight)

      buttons = [TouchButton("but. " + str(row+1) + " " + str(col+1)) for col in range(4)]
      _ = [buttons[col].setObjectName("root_tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [buttons[col].cmd_edit.setObjectName("tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [buttons[col].cmd_edit.clicked.connect(self.choose_action) for col in range(4)]
      _ = [buttons[col].img_edit.setObjectName("tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [buttons[col].img_edit.clicked.connect(self.choose_image) for col in range(4)]
      _ = [layout.addWidget(buttons[col], row, col+2) for col in range(4)]

      displayR = TDisplay("dis. " + str(row+1) + " Right")
      displayR.setObjectName("root_dis%sL"% (row+1))
      displayR.cmd_edit.setObjectName("dis%sR" % (row+1))
      displayR.cmd_edit.clicked.connect(self.choose_action)
      displayR.img_edit.setObjectName("dis%sR" % (row+1))
      displayR.img_edit.clicked.connect(self.choose_image)
      layout.addWidget(displayR, row, 6, alignment=Qt.AlignLeft)

      encoderR = Encoder("enc. " + str(row+1) + " Right")
      encoderR.push_cmd_edit.setObjectName("enc%sR" % (row+1))
      encoderR.push_cmd_edit.clicked.connect(self.choose_action)
      encoderR.left_cmd_edit.clicked.connect(self.choose_action)
      encoderR.left_cmd_edit.setObjectName("enc%sR-l" % (row+1))
      encoderR.right_cmd_edit.clicked.connect(self.choose_action)
      encoderR.right_cmd_edit.setObjectName("enc%sR-r" % (row+1))
      layout.addWidget(encoderR, row, 7)

    pages = [ModeButton(str(i)) for i in range(8)]
    _ = [layout.addWidget(pages[i], 4, i) for i in range(8)]

    self.setLayout(layout)

  def choose_action(self):
    sender_id = self.sender().objectName()
    dialog = ConfigCmd(self.sender())
    if (dialog.exec()):
      print(sender_id)
      self.config.actions[sender_id] = dialog.user_cmd.text()

  def choose_image(self):
    sender_id = self.sender().parent().objectName()
    dialog = ConfigImg(self.sender())
    dialog.image_selected.connect(QApplication.instance().on_image_selected)

    if (dialog.exec()):
      path = dialog.user_img.text()
      self.config.images[self.sender().objectName()] = path
      self.sender().parent().setStyleSheet("QPushButton#%s { background-image: url(%s);background-size: 90x90px}" % (sender_id, path))


class Widget (QPushButton):
  def __init__(self, text):
    QPushButton.__init__(self, text)
    self.setFixedSize(90, 90)
    self.cmd_edit = QPushButton("cmd")
    self.cmd_edit.setFixedSize(35, 15)
    vlayout = QVBoxLayout()
    vlayout.addWidget(self.cmd_edit, alignment=Qt.AlignRight|Qt.AlignTop)
    self.setLayout(vlayout)


class Display (Widget):
  def __init__(self, text):
    super().__init__(text)
    self.img_edit = QPushButton("img")
    self.img_edit.setFixedSize(35, 15)
    layout = self.layout()
    layout.addWidget(self.img_edit, alignment=Qt.AlignRight|Qt.AlignBottom)
    self.setLayout(layout)


class Encoder (Widget):
  def __init__(self, text):
    super().__init__(text)
    self.push_cmd_edit = self.cmd_edit
    self.left_cmd_edit = QPushButton("L", self)
    self.left_cmd_edit.setFixedSize(25, 15)
    self.right_cmd_edit = QPushButton("R", self)
    self.right_cmd_edit.setFixedSize(25, 15)

    hlayout = QHBoxLayout()
    hlayout.addWidget(self.left_cmd_edit, alignment=Qt.AlignLeft|Qt.AlignBottom)
    hlayout.addWidget(self.right_cmd_edit, alignment=Qt.AlignRight|Qt.AlignBottom)

    vlayout = self.layout()
    vlayout.addLayout(hlayout)
    self.setLayout(vlayout)


class TouchButton (Display):
  def __init__(self, text): 
    super().__init__(text)


class TDisplay (Display):
  def __init__(self, text):
    super().__init__(text)
    self.setFixedSize(60, 90)


class ModeButton (Widget):
  def __init__(self, text):
    super().__init__(text)

