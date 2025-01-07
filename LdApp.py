import LdWidget as ldw

from Loupedeck import DeviceManager
from Loupedeck.Devices import LoupedeckLive
from Loupedeck.Devices.LoupedeckLive import CALLBACK_KEYWORD as CBC

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, qApp
from PyQt5.QtCore import pyqtSignal
from PIL import Image, ImageColor
from math import floor
import os


class LdApp(QApplication):
  save_to = pyqtSignal(str)
  load_to = pyqtSignal(str)

  def __init__(self, argv):
    QApplication.__init__(self, argv)
    QApplication.qApp = self
    self.main_window = QMainWindow()
    self.main_window.setWindowTitle("Loupedeck Live control")
    self.ld_widget = ldw.Loupedeck(self.main_window)
    self.profile = QLineEdit()
    self.save_but = QPushButton("Save profile", self.main_window)
    self.load_but = QPushButton("Load profile", self.main_window)
    hlayout= QHBoxLayout()
    hlayout.addWidget(self.profile)
    hlayout.addWidget(self.save_but)
    hlayout.addWidget(self.load_but)
    hwidget = QWidget(self.main_window)
    hwidget.setLayout(hlayout)
    vlayout = QVBoxLayout()
    vlayout.addWidget(self.ld_widget)
    vlayout.addWidget(hwidget)
    vwidget = QWidget(self.main_window)
    vwidget.setLayout(vlayout)
    self.main_window.setCentralWidget(vwidget)
    self.save_but.clicked.connect(self.save)
    self.save_to.connect(self.ld_widget.config.save)
    self.load_but.clicked.connect(self.load)
    self.load_to.connect(self.ld_widget.config.load)
    self.main_window.show()

  def detect(self):
    ld = DeviceManager().enumerate()
    if len(ld) >= 1:
      print("detected")
      self.ld_device = ld[0] 
      self.ld_device.set_callback(self.device_callback)
    else:
      print("no device found")

  def save(self):
    self.save_to.emit(self.profile.text())

  def load(self):
    self.load_to.emit(self.profile.text())
    # restore profile name and load profile images onto the GUI
    self.profile.setText(self.ld_widget.config.profile)
    for key, path in self.ld_widget.config.images.items():
      if path:
        button = self.ld_widget.findChild(QPushButton, key)
        if button :
          button.setStyleSheet("QPushButton#%s { background-image: url(%s);}" % (key, path))
          self.set_img_to_touchbutton(path, self.tb_to_keycode(key))

  def device_callback(self, ld, message:dict):
    if CBC.SCREEN.value in message:  # touch event
      if message[CBC.KEY.value] is not None:  # touch key pressed
        if "touchstart" in message[CBC.ACTION.value]:  # to avoid double activation
          self.on_touchkey_press(message[CBC.KEY.value])
      else:  # left or right screen press
        print("display event on display %s" % message[CBC.SCREEN.value])

    elif CBC.STATE.value in message:  # encoder rotate or press or mode button press
      l = ["circle"]
      l = l + [str(i) for i in range(1, 8)]
      if message[CBC.ACTION.value] is CBC.ROTATE.value:  # encoder rotate
        print("rotate %s event on encoder %s" % (message[CBC.STATE.value], message[CBC.IDENTIFIER.value]))
      elif message[CBC.IDENTIFIER.value] in l:  # mode button pressed
        print ("press event on button %s" % message[CBC.IDENTIFIER.value])
      else:  # encoder button pressed
        print ("press event on encoder %s" % message[CBC.IDENTIFIER.value])

    else:  # catch other untreated yet cases
      print(message.keys())
      print(message.values())

  def on_image_selected(self, image_path):
    tb_id = self.sender().parent().objectName()
    path = self.ld_widget.config.images[tb_id]
    if "tb" in tb_id:
      keycode = self.tb_to_keycode(tb_id)
      self.set_img_to_touchbutton(image_path, keycode)

  def set_img_to_touchbutton(self, image_path, keycode):
    with open(image_path, "rb") as infile:
        image = Image.open(infile).convert("RGBA")
        image.thumbnail((90,90))
        self.ld_device.set_key_image(keycode, image)

  def tb_to_keycode(self, name):
    if "tb" in name and len(name) == 4:
      row = int(name[2])
      col = int(name[3])
      tb_id = (row-1)*4 + col-1
      return tb_id

  def on_touchkey_press(self, key):
    row = floor(key/4)+1
    col = floor(key-(4*(row-1)))+1
    str_key = "tb" + str(row) + str(col)
    cmd = self.ld_widget.config.actions[str_key]
    os.system(cmd)

  def __exit__(self, exc_type, exc_value, traceback):
    self.ld_device.stop()
    super().__exit__(exc_type, exc_value, traceback)

