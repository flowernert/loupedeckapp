import sys

from Loupedeck import DeviceManager
from Loupedeck.Devices import LoupedeckLive

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout
from PIL import Image, ImageColor


def detect():
  devices = DeviceManager().enumerate()
  if len(devices) >= 1:
    print("detected")
    return devices[0]
  else:
    return None
    

def setup_ld_widget():
  layout = QGridLayout()
  for row in range(3):
    encoderL = QPushButton("enc. " + str(row) + " Left")
    layout.addWidget(encoderL, row, 0)

    displayL = QPushButton("dis." + str(row) + " Left")
    layout.addWidget(displayL, row, 1)

    buttons = [QPushButton("but. " + str(row) + " " + str(col)) for col in range(4)]
    _ = [layout.addWidget(buttons[col], row, col+2) for col in range(4)]

    displayR = QPushButton("dis. " + str(row) + " Right")
    layout.addWidget(displayR, row, 6)

    encoderR = QPushButton("enc. " + str(row) + " Right")
    layout.addWidget(encoderR, row, 7)

  pages = [QPushButton(str(i)) for i in range(8)]
  _ = [layout.addWidget(pages[i], 4, i) for i in range(8)]

  ld_widget = QWidget()
  ld_widget.setLayout(layout)
  return ld_widget
  

def qtapp_main(ld):
  app = QApplication([])
  main_window = QMainWindow()
  ldw = setup_ld_widget()
  main_window.setCentralWidget(ldw)
  main_window.show()
  app.exec()
  

if __name__ == "__main__":
  ld = detect()
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
    
    
    
    
    
    
    
    
    
