import sys

from Loupedeck import DeviceManager
from Loupedeck.Devices import LoupedeckLive
import LdWidget as ldw

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout
from PIL import Image, ImageColor


def detect():
  devices = DeviceManager().enumerate()
  if len(devices) >= 1:
    print("detected")
    return devices[0]
  else:
    return None
   

def qtapp_main(ld):
  app = QApplication([])
  main_window = QMainWindow()
  main_window.setWindowTitle("Loupedeck Live control")
  ld = ldw.Loupedeck(main_window)
  main_window.setCentralWidget(ld)
  main_window.show()
  app.exec()
  

if __name__ == "__main__":
  ld = 1
  #ld = detect()
  if ld:
    qtapp_main(ld)
#    image2 = Image.new("RGBA", (90, 90), "blue")
#    ld.set_key_image(6, image2)
#    with open("Images/emoji_laugh.png", "rb") as infile:
#      image = Image.open(infile).convert("RGBA")
#      image.thumbnail((90,90))
#      ld.set_key_image(6, image)
      #ld.draw_image(image, "center")
      
    
  else:
    print("No loupedeck device found")
    
    
    
    
    
    
    
    
    
