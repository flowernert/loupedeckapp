import sys

from LdApp import LdApp

from Loupedeck import DeviceManager
from Loupedeck.Devices import LoupedeckLive

from PIL import Image, ImageColor


def detect():
  devices = DeviceManager().enumerate()
  if len(devices) >= 1:
    print("detected")
    return devices[0]
  else:
    return None
   

def main(argv):
  app = LdApp(argv)
  app.detect()
  sys.exit(app.exec())
  

if __name__ == "__main__":
  main(sys.argv)
#    image2 = Image.new("RGBA", (90, 90), "blue")
#    ld.set_key_image(6, image2)
#    with open("Images/emoji_laugh.png", "rb") as infile:
#      image = Image.open(infile).convert("RGBA")
#      image.thumbnail((90,90))
#      ld.set_key_image(6, image)
      #ld.draw_image(image, "center")

    
    
    
    
    
    
    
