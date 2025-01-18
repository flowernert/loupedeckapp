from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QFrame, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PIL import Image, ImageColor
from LdConfiguration import LdConfiguration, LdSubmenu, LdAction
from LdDialog import ConfigActionDialog, ConfigImgDialog


class LoupedeckWidget (QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.config = LdConfiguration()
    self.elements = dict()
    self.encoders = dict()
    self.displays = dict()
    self.touchbuttons = dict()
    self.modebuttons = dict()

    layout = QGridLayout()
    for row in range(3):
      encoderL = Encoder()
      encoderL.setObjectName("root_enc%sL" % (row+1))
      encoderL.push_action_edit.clicked.connect(self.choose_action)
      encoderL.push_action_edit.setObjectName("enc%sL" % (row+1))
      encoderL.left_action_edit.clicked.connect(self.choose_action)
      encoderL.left_action_edit.setObjectName("enc%sL-l" % (row+1))
      encoderL.right_action_edit.clicked.connect(self.choose_action)
      encoderL.right_action_edit.setObjectName("enc%sL-r" % (row+1))
      layout.addWidget(encoderL, row, 0)
      self.encoders[encoderL.objectName()] = encoderL

      displayL = TouchDisplay()
      displayL.setObjectName("root_dis%sL" % (row+1))
      displayL.action_edit.clicked.connect(self.choose_action)
      displayL.action_edit.setObjectName("dis%sL" % (row+1))
      displayL.img_edit.clicked.connect(self.choose_image)
      displayL.img_edit.setObjectName("dis%sL" % (row+1))
      layout.addWidget(displayL, row, 1, alignment=Qt.AlignRight)
      self.displays[displayL.objectName()] = displayL

      buttons = [TouchButton() for col in range(4)]
      _ = [buttons[col].setObjectName("root_tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [buttons[col].action_edit.clicked.connect(self.choose_action) for col in range(4)]
      _ = [buttons[col].action_edit.setObjectName("tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [buttons[col].img_edit.clicked.connect(self.choose_image) for col in range(4)]
      _ = [buttons[col].img_edit.setObjectName("tb%i%i" % (row+1, col+1)) for col in range(4)]
      _ = [layout.addWidget(buttons[col], row, col+2) for col in range(4)]
      self.touchbuttons.update({b.objectName(): b for b in buttons})

      displayR = TouchDisplay()
      displayR.setObjectName("root_dis%sR"% (row+1))
      displayR.action_edit.clicked.connect(self.choose_action)
      displayR.action_edit.setObjectName("dis%sR" % (row+1))
      displayR.img_edit.clicked.connect(self.choose_image)
      displayR.img_edit.setObjectName("dis%sR" % (row+1))
      layout.addWidget(displayR, row, 6, alignment=Qt.AlignLeft)
      self.displays[displayR.objectName()] = displayR

      encoderR = Encoder()
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
    _ = [layout.addWidget(pages[i], 4, i, alignment=Qt.AlignCenter) for i in range(8)]
    self.modebuttons = pages

    self.elements.update(self.encoders)
    self.elements.update(self.displays)
    self.elements.update(self.touchbuttons)

    self.setLayout(layout)

  def choose_action(self):
    ldApp = QApplication.instance()
    sender_id = self.sender().objectName()
    dialog = ConfigActionDialog(self.sender())
    dialog.action_selected.connect(ldApp.on_action_selected)
    dialog.action_selected.connect(self.on_action_selected)
    dialog.show()

  def on_action_selected(self, action):
    b = self.sender().parent()
    b.parent().set_action(action, b.objectName())
    self.update()

  def choose_image(self):
    ldApp = QApplication.instance()
    sender_id = self.sender().objectName()
    dialog = ConfigImgDialog(self.sender())
    dialog.image_selected.connect(ldApp.on_image_selected)
    dialog.image_selected.connect(self.on_image_selected)
    dialog.show()

  def on_image_selected(self, img_path):
    b = self.sender().parent()
    b.parent().set_image(img_path)  # setting image to the tb/dis widget
    self.update()

  def reset_images(self):
    for tb in self.touchbuttons.values():
      tb.set_image("")
    for d in self.displays.values():
      d.set_image("")
    self.update()

  def enable_ws_buttons(self):
    self.set_ws_buttons(True)

  def disable_ws_buttons(self):
    self.set_ws_buttons(False)

  def set_ws_buttons(self, enable):
    for mb in self.modebuttons:
      mb.setEnabled(enable)
    self.update()

  def enable_widget_configurable(self, widget_key):
    self.set_widget_configurable(widget_key, True)

  def disable_widget_configurable(self, widget_key):
    self.set_widget_configurable(widget_key, False)

  def set_widget_configurable(self, widget_key, configurable):
    self.elements[widget_key].set_configurable(configurable)


class Widget (QFrame):
  def __init__(self):
    QFrame.__init__(self)
    self.setFixedSize(90, 90)
    self.setFrameStyle(QFrame.StyledPanel|QFrame.Raised)
    self.action_edit = QPushButton("action")
    self.action_edit.setFixedSize(35, 20)
    vlayout = QVBoxLayout()
    vlayout.addWidget(self.action_edit, alignment=Qt.AlignRight|Qt.AlignTop)
    self.setLayout(vlayout)

  def set_action(self, action, key=None):
    if action:
      color = "green" if action.a_type != "none" else "black"
      self.action_edit.setToolTip(action.summary)
      self.action_edit.setStyleSheet("QPushButton#%s {color:%s;}" % (self.action_edit.objectName(), color))

  def disable_configurable(self):
    self.set_configurable(False)

  def enable_configurable(self):
    self.set_configurable(True)

  def set_configurable(self, configurable):
    self.action_edit.setVisible(configurable)


class Display (Widget):
  def __init__(self):
    super().__init__()
    self.image = QPixmap()
    self.img_edit = QPushButton("img")
    self.img_edit.setFixedSize(35, 20)
    self.setStyleSheet("QFrame { border: 2px solid darkgrey; border-radius: 5px;}")
    layout = self.layout()
    layout.addWidget(self.img_edit, alignment=Qt.AlignRight|Qt.AlignBottom)
    self.setLayout(layout)

  def set_image(self, img_path):
    self.image = QPixmap(img_path)
    if not self.image.isNull() and img_path:
      self.image = self.image.scaled(self.size(), Qt.KeepAspectRatio)
      self.img_edit.setToolTip(img_path)
      self.img_edit.setStyleSheet("QPushButton#%s {color:green;}" % self.img_edit.objectName())
    else:
      self.image = QPixmap()
      self.img_edit.setToolTip("")
      self.img_edit.setStyleSheet("QPushButton#%s {color:black;}" % self.img_edit.objectName())

  def disable_configurable(self):
    self.set_configurable(False)

  def enable_configurable(self):
    self.set_configurable(True)

  def set_configurable(self, configurable):
    self.img_edit.setVisible(configurable)
    super().set_configurable(configurable)

  def paintEvent(self, qpaint_event):
#    if not self.image.isNull():
    qpainter = QPainter(self)
    # in order not to cover the widget borders
    margin=2
    size = self.size()
    yshift = int((90-size.width())/2)
    xsub = int(size.width()-margin*2)
    ysub = int(size.width()-margin*2)
    qpainter.drawPixmap(margin, yshift+margin, xsub, ysub, self.image)
    QFrame.paintEvent(self, qpaint_event)


class Encoder (Widget):
  def __init__(self):
    super().__init__()
    self.setFixedSize(80,80)
    self.push_action_edit = self.action_edit
    self.left_action_edit = QPushButton("L", self)
    self.left_action_edit.setFixedSize(25, 20)
    self.right_action_edit = QPushButton("R", self)
    self.right_action_edit.setFixedSize(25, 20)
    self.setStyleSheet("QFrame { border: 4px solid darkgrey; border-radius: 40px;}")

    hlayout = QHBoxLayout()
    hlayout.addWidget(self.left_action_edit, alignment=Qt.AlignLeft|Qt.AlignBottom)
    hlayout.addWidget(self.right_action_edit, alignment=Qt.AlignRight|Qt.AlignBottom)

    vlayout = self.layout()
    vlayout.addLayout(hlayout)
    self.setLayout(vlayout)

  def set_action(self, action, key):
    if action and key and action.a_type != "none":
      color = "green" if action.a_type != "none" else "black"
      if len(key)<=5:
        super().set_action(action, key)
      elif key.endswith("-r"):
        self.right_action_edit.setToolTip(action.summary)
        self.right_action_edit.setStyleSheet("QPushButton#%s {color:%s;}" % (self.right_action_edit.objectName(), color))
      elif key.endswith("-l"):
        self.left_action_edit.setToolTip(action.summary)
        self.left_action_edit.setStyleSheet("QPushButton#%s {color:%s;}" % (self.left_action_edit.objectName(), color))
      else:
        print("load_ws unknown action key, please report to the developer %s" % key)


class TouchButton (Display):
  def __init__(self):
    super().__init__()
    self.setFixedSize(90, 90)


class TouchDisplay (Display):
  def __init__(self):
    super().__init__()
    self.setFixedSize(60, 90)


class ModeButton (QPushButton):
  def __init__(self, text):
    super().__init__(text)
    self.setFixedSize(70, 70)
    self.setStyleSheet("QPushButton { border: 2px solid darkgrey; border-radius: 35px;}")

