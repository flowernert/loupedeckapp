import LdWidget as ldw

from Loupedeck import DeviceManager
from Loupedeck.Devices import LoupedeckLive
from Loupedeck.Devices.LoupedeckLive import CALLBACK_KEYWORD as CBC

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, qApp
from PyQt5.QtCore import pyqtSignal
from PIL import Image, ImageColor
from math import floor
import os, time, serial, gc


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
    self.main_window.closeEvent = self.close
    self.main_window.show()

  def detect(self):
    ld = None
    try_cpt = 0
    while not ld:
      ld = DeviceManager().enumerate()
      if len(ld) >= 1:
        print("detected")
        self.ld_device = ld[0]
        self.ld_device.set_callback(self.device_callback)
      elif try_cpt < 10:
        try_cpt +=1
        time.sleep(try_cpt/10.0)
      else:
        self.close("Unable to detect the Loupedeck device after %i attempts" % (try_cpt))

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
          self.set_img_to_touchbutton(path, self.tb_name_to_keycode(key))

  def device_callback(self, ld, message:dict):
    ws_keys = ["circle"] + [str(i) for i in range(1, 8)]

    # touch event
    if CBC.SCREEN.value in message:
      if "touchstart" in message[CBC.ACTION.value]:  # to avoid double activation
        # touch key pressed
        if message[CBC.KEY.value] is not None:
          self.on_touchkey_press(message[CBC.KEY.value])
        # left or right screen press
        else:
          self.on_touchdisplay_press(message[CBC.X.value], message[CBC.Y.value])

    # encoder event
    elif "knob" in message[CBC.IDENTIFIER.value]:
      if message[CBC.ACTION.value] is CBC.ROTATE.value:  # encoder rotate
        self.on_encoder_rotate(message[CBC.IDENTIFIER.value], message[CBC.STATE.value])
      elif message[CBC.ACTION.value] is CBC.PUSH.value and message[CBC.STATE.value] == "down":  # encoder press and avoid double activation
        self.on_encoder_press(message[CBC.IDENTIFIER.value])

    # workspace selection event
    elif message[CBC.IDENTIFIER.value] in ws_keys:
      print ("press event on button %s" % message[CBC.IDENTIFIER.value])

    # catch other untreated yet cases
    else:
      print("Unhandled event!")
      print(message.keys())
      print(message.values())

  def on_image_selected(self, image_path):
    sender_id = self.sender().parent().objectName()
    path = self.ld_widget.config.images[sender_id]
    if "tb" in sender_id:
      keycode = self.tb_name_to_keycode(sender_id)
      self.set_img_to_touchbutton(image_path, keycode)
    elif "dis" in sender_id:
      side = sender_id[4]
      row = int(sender_id[3])
      self.set_img_to_touchdisplay(image_path, side, row)

  def set_img_to_touchbutton(self, image_path, keycode):
    with open(image_path, "rb") as infile:
        image = Image.open(infile).convert("RGBA")
        image.thumbnail((90,90))
        self.ld_device.set_key_image(keycode, image)

  def set_img_to_touchdisplay(self, image_path, side, row):
    with open(image_path, "rb") as infile:
        image = Image.open(infile).convert("RGBA").resize((60,60)).crop((0,-15,60,75))
        if side == "L":
          x = 0
          display = "left"
        else:
          x = 480
          display = "right"
        #self.ld_device.set_key_image(display, image)
        self.ld_device.draw_image(image, display=display, width=60, height=90, x=x, y=(row-1)*90, auto_refresh=True)

  def tb_name_to_keycode(self, name):
    if "tb" in name and len(name) == 4:
      row = int(name[2])
      col = int(name[3])
      tb_id = (row-1)*4 + col-1
      return tb_id

  def td_pos_to_display_name(self, x, y):
    s = "dis"
    row = str(floor(y/90)+1)
    s += row
    if x < 60:
      s +="L"
    else:
      s +="R"
    return s

  def knob_to_enc_name(self, knob):
    if knob[4] == "T":
      row = 1
    elif knob[4] == "C":
      row = 2
    else:
      row = 3
    return "enc" + str(row) + knob[5]

  def on_touchkey_press(self, key):
    row = floor(key/4)+1
    col = floor(key-(4*(row-1)))+1
    str_key = "tb" + str(row) + str(col)
    cmd = self.ld_widget.config.actions[str_key]
    os.system(cmd)

  def on_touchdisplay_press(self, x, y):
     str_key = self.td_pos_to_display_name(x, y)
     cmd = self.ld_widget.config.actions[str_key]
     os.system(cmd)

  def on_encoder_press(self, encoder):
    str_key = self.knob_to_enc_name(encoder)
    cmd = self.ld_widget.config.actions[str_key]
    os.system(cmd)

  def on_encoder_rotate(self, encoder, direction):
    str_key = self.knob_to_enc_name(encoder) + "-" + direction[0]
    cmd = self.ld_widget.config.actions[str_key]
    os.system(cmd)

  def close(self, event):
    print("onclose")
    if self.ld_device.reading_running or self.ld_device.process_running:
      self.ld_device.stop()

