import sys

from LdApp import LdApp

from Loupedeck import DeviceManager
from Loupedeck.Devices import LoupedeckLive

from PIL import Image, ImageColor


def main(argv):
  app = LdApp(argv)
  app.detect()
  sys.exit(app.exec())


if __name__ == "__main__":
  main(sys.argv)

