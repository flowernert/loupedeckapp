import LdWidget as ldw

from Loupedeck import DeviceManager
from Loupedeck.Devices import LoupedeckLive
from Loupedeck.Devices.LoupedeckLive import CALLBACK_KEYWORD as CBC

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout, qApp
from PIL import Image, ImageColor


class LdApp(QApplication):
  def __init__(self, argv):
    QApplication.__init__(self, argv)
    QApplication.qApp = self
    self.main_window = QMainWindow()
    self.main_window.setWindowTitle("Loupedeck Live control")
    self.ld_widget = ldw.Loupedeck(self.main_window)
    self.main_window.setCentralWidget(self.ld_widget)
    self.main_window.show()

  def detect(self):
    ld = DeviceManager().enumerate()
    if len(ld) >= 1:
      print("detected")
      self.ld_device = ld[0] 
      self.ld_device.set_callback(self.device_callback)
    else:
      print("no device found")

  def device_callback(self, ld, message:dict):
    if CBC.SCREEN.value in message:  # touch event
      if message[CBC.KEY.value] is not None:  # touch key pressed
        print("touch event on key %i" % message[CBC.KEY.value])
      else:  # left or right screen press
        print("display event on display %s" % message[CBC.SCREEN.value])
    elif CBC.STATE.value in message:  # encoder rotate or press or mode button press
      l = ["circle"]
      l = l + [str(i) for i in range(1, 8)]
      if message[CBC.ACTION.value] is CBC.ROTATE.value:
        print("rotate %s event on encoder %s" % (message[CBC.STATE.value], message[CBC.IDENTIFIER.value]))
      elif message[CBC.IDENTIFIER.value] in l:  # mode button
        print ("press event on button %s" % message[CBC.IDENTIFIER.value])
      else:  # encoder button
        print ("press event on encoder %s" % message[CBC.IDENTIFIER.value])
    else:
      print(message.keys())
      print(message.values())


  def on_image_selected(self, image_path):
    sender_id = self.sender().parent().objectName()
    path = self.ld_widget.config.images[sender_id]
    if "tb" in sender_id:
      row = int(sender_id[2])
      col = int(sender_id[3])
      tb_id = (row-1)*4 + col-1
      with open(image_path, "rb") as infile:
        image = Image.open(infile).convert("RGBA")
        image.thumbnail((90,90))
        self.ld_device.set_key_image(tb_id, image)

