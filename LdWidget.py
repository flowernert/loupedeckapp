import LdDialog
import LdApp

from LdDialog import ConfigAction, ConfigCmd, ConfigImg
from LdConfiguration import LdConfiguration

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PIL import Image, ImageColor


class Loupedeck (QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.config = LdConfiguration()
    self.elements = dict()
    self.encoders = dict()
    self.displays = dict()
    self.touchbuttons = dict()

    layout = QGridLayout()
    for row in range(3):
      encoderL = Encoder("enc. " + str(row+1) + " Left")
      encoderL.setObjectName("root_enc%sL" % (row+1))
      encoderL.push_action_edit.clicked.connect(self.choose_action)
      encoderL.push_action_edit.setObjectName("enc%sL" % (row+1))
      encoderL.left_action_edit.clicked.connect(self.choose_action)
      encoderL.left_action_edit.setObjectName("enc%sL-l" % (row+1))
      encoderL.right_action_edit.clicked.connect(self.choose_action)
      encoderL.right_action_edit.setObjectName("enc%sL-r" % (row+1))
      layout.addWidget(encoderL, row, 0)
      self.encoders[encoderL.objectName()] = encoderL

      displayL = TouchDisplay("dis." + str(row+1) + " Left")
      displayL.setObjectName("root_dis%sL" % (row+1))
      displayL.action_edit.clicked.connect(self.choose_action)
      displayL.action_edit.setObjectName("dis%sL" % (row+1))
      displayL.img_edit.clicked.connect(self.choose_image)
      displayL.img_edit.setObjectName("dis%sL" % (row+1))
      layout.addWidget(displayL, row, 1, alignment=Qt.AlignRight)
      self.displays[displayL.objectName()] = displayL

      buttons = [TouchButton("but. " + str(row+1) + " " + str(col+1)) for col in range(4)]
      _ = [buttons[col].setObjectName("root_tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [buttons[col].action_edit.clicked.connect(self.choose_action) for col in range(4)]
      _ = [buttons[col].action_edit.setObjectName("tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [buttons[col].img_edit.clicked.connect(self.choose_image) for col in range(4)]
      _ = [buttons[col].img_edit.setObjectName("tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [layout.addWidget(buttons[col], row, col+2) for col in range(4)]
      self.touchbuttons.update({b.objectName(): b for b in buttons})

      displayR = TouchDisplay("dis. " + str(row+1) + " Right")
      displayR.setObjectName("root_dis%sR"% (row+1))
      displayR.action_edit.clicked.connect(self.choose_action)
      displayR.action_edit.setObjectName("dis%sR" % (row+1))
      displayR.img_edit.clicked.connect(self.choose_image)
      displayR.img_edit.setObjectName("dis%sR" % (row+1))
      layout.addWidget(displayR, row, 6, alignment=Qt.AlignLeft)
      self.displays[displayR.objectName()] = displayR

      encoderR = Encoder("enc. " + str(row+1) + " Right")
      encoderR.setObjectName("root_enc%sR" % (row+1))
      encoderR.push_action_edit.clicked.connect(self.choose_action)
      encoderR.push_action_edit.setObjectName("enc%sR" % (row+1))
      encoderR.left_action_edit.clicked.connect(self.choose_action)
      encoderR.left_action_edit.setObjectName("enc%sR-l" % (row+1))
      encoderR.right_action_edit.clicked.connect(self.choose_action)
      encoderR.right_action_edit.setObjectName("enc%sR-r" % (row+1))
      layout.addWidget(encoderR, row, 7)
      self.encoders[encoderR.objectName()] = encoderR

    pages = [ModeButton(str(i)) for i in range(8)]
    _ = [layout.addWidget(pages[i], 4, i) for i in range(8)]

    self.elements.update(self.encoders)
    self.elements.update(self.displays)
    self.elements.update(self.touchbuttons)

    self.setLayout(layout)

  def choose_action(self):
    ldApp = QApplication.instance()
    sender_id = self.sender().objectName()
    dialog = ConfigAction(self.sender())
    dialog.action_selected.connect(ldApp.on_action_selected)
    if (dialog.exec_()):
      action = dialog.selected_action
      if action:
        self.sender().setToolTip(action.action)
    else:
      self.sender().setToolTip("")

  def choose_image(self):
    ldApp = QApplication.instance()
    sender_id = self.sender().objectName()
    dialog = ConfigImg(self.sender())
    dialog.image_selected.connect(ldApp.on_image_selected)
    if (dialog.exec_()):
      path = dialog.user_img.text()
      self.sender().parent().set_image(path)  # setting image to the tb/dis widget
      self.sender().setToolTip(path)

  def reset_images(self):
    for tb in self.touchbuttons.values():
      tb.set_image("")
    for d in self.displays.values():
      d.set_image("")


class Widget (QPushButton):
  def __init__(self, text):
    QPushButton.__init__(self, text)
    self.setFixedSize(90, 90)
    self.action_edit = QPushButton("action")
    self.action_edit.setFixedSize(35, 20)
    vlayout = QVBoxLayout()
    vlayout.addWidget(self.action_edit, alignment=Qt.AlignRight|Qt.AlignTop)
    self.setLayout(vlayout)


class Display (Widget):
  def __init__(self, text):
    super().__init__(text)
    self.img_edit = QPushButton("img")
    self.img_edit.setFixedSize(35, 20)
    layout = self.layout()
    layout.addWidget(self.img_edit, alignment=Qt.AlignRight|Qt.AlignBottom)
    self.setLayout(layout)

  def set_image(self, img_path):
    self.setStyleSheet("QPushButton#%s { border: 1px solid black; border-image: url(%s);}" % (self.objectName(), img_path))


class Encoder (Widget):
  def __init__(self, text):
    super().__init__(text)

    self.push_action_edit = self.action_edit
    self.left_action_edit = QPushButton("L", self)
    self.left_action_edit.setFixedSize(25, 20)
    self.right_action_edit = QPushButton("R", self)
    self.right_action_edit.setFixedSize(25, 20)

    hlayout = QHBoxLayout()
    hlayout.addWidget(self.left_action_edit, alignment=Qt.AlignLeft|Qt.AlignBottom)
    hlayout.addWidget(self.right_action_edit, alignment=Qt.AlignRight|Qt.AlignBottom)

    vlayout = self.layout()
    vlayout.addLayout(hlayout)
    self.setLayout(vlayout)


class TouchButton (Display):
  def __init__(self, text): 
    super().__init__(text)


class TouchDisplay (Display):
  def __init__(self, text):
    super().__init__(text)
    self.setFixedSize(60, 90)


class ModeButton (Widget):
  def __init__(self, text):
    super().__init__(text)

