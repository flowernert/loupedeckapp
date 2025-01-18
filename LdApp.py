import LdWidget as ldw
from LdConfiguration import LdAction
from LdDialog import ConfigImgDialog

from Loupedeck import DeviceManager
from Loupedeck.Devices import LoupedeckLive
from Loupedeck.Devices.LoupedeckLive import CALLBACK_KEYWORD as CBC

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QCommonStyle
from PyQt5.QtCore import pyqtSignal
from PIL import Image, ImageColor
from math import floor
import os, time, serial, gc, sys


class LdApp(QApplication):
  save_to = pyqtSignal(str)
  load_from = pyqtSignal(str)

  submenu_opened = pyqtSignal(str)
  submenu_closed = pyqtSignal(str)

  back_but_path = "Images/submenu_back_button.png"

  ws_keys = ["circle"] + [str(i) for i in range(1, 8)]
  selected_ws = ws_keys[0]

  submenu_stack = []

  def __init__(self, argv):
    QApplication.__init__(self, argv)
    QApplication.qApp = self
    self.main_window = QMainWindow()
    self.main_window.setWindowTitle("Loupedeck Live control")
    self.ld_widget = ldw.LoupedeckWidget(self.main_window)
    self.location = QLabel(self.selected_ws)
    self.config = self.ld_widget.config
    self.profile = QLineEdit()
    self.save_but = QPushButton("Save profile", self.main_window)
    self.load_but = QPushButton("Load profile", self.main_window)
    hlayout= QHBoxLayout()
    hlayout.addWidget(self.profile)
    hlayout.addWidget(self.save_but)
    hlayout.addWidget(self.load_but)
    profile_widget = QWidget(self.main_window)
    profile_widget.setLayout(hlayout)
    vlayout = QVBoxLayout()
    vlayout.addWidget(self.location)
    vlayout.addWidget(self.ld_widget)
    vlayout.addWidget(profile_widget)
    vwidget = QWidget(self.main_window)
    vwidget.setLayout(vlayout)
    self.main_window.setCentralWidget(vwidget)
    self.save_but.clicked.connect(self.save_profile)
    self.save_to.connect(self.ld_widget.config.save)
    self.load_but.clicked.connect(self.load_profile)
    self.load_but.setDisabled(True)
    self.save_but.setDisabled(True)
    self.load_from.connect(self.ld_widget.config.load)
    self.load_from.connect(self.profile.setText)
    self.profile.textChanged.connect(self.onProfileTextChanged)
    self.submenu_opened.connect(self.ld_widget.disable_ws_buttons)
    self.submenu_opened.connect(self.ld_widget.disable_widget_configurable)
    self.submenu_closed.connect(self.ld_widget.enable_ws_buttons)
    self.submenu_closed.connect(self.ld_widget.enable_widget_configurable)
    self.main_window.closeEvent = self.close
    self.main_window.show()

  def detect(self):
    ld = None
    try_cpt = 0
    LoupedeckLive.BAUD_RATE = 460800  # no idea if effective
    while not ld:
      ld = DeviceManager().enumerate()
      if len(ld) >= 1:
        print("detected %s" % ld[0].DECK_TYPE)
        self.ld_device = ld[0]
        self.ld_device.set_callback(self.device_callback)
        self.init_ld_device()
        self.on_workspace_press(self.ws_keys[0])
      elif try_cpt < 10:
        print(try_cpt)
        try_cpt +=1
        time.sleep(try_cpt/10.0)
      else:
        print("Unable to detect the Loupedeck device after %i attempts" % (try_cpt))
        self.closeAllWindows()
        break

  def init_ld_device(self):
    self.ld_device.reset()
    self.ld_device.set_button_color("circle", "green")
    for i in range(1,8):
      self.ld_device.set_button_color(str(i), (63, 63, 63))  # dim white
    self.ld_device.set_brightness(40)

  def save_profile(self):
    self.save_to.emit(self.profile.text())

  def onProfileTextChanged(self, arg):
    state = bool(arg)
    self.load_but.setEnabled(state)
    self.save_but.setEnabled(state)

  def load_profile(self):
    self.ld_device.reset()
    self.ld_widget.reset_images()
    self.load_from.emit(self.profile.text())
    self.on_workspace_press(self.ws_keys[0])

  def device_callback(self, ld, message:dict):
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
    elif message[CBC.IDENTIFIER.value] in self.ws_keys:
      if message[CBC.STATE.value] == "down" and message[CBC.IDENTIFIER.value] != self.selected_ws:
        self.on_workspace_press(message[CBC.IDENTIFIER.value])

    # catch other untreated yet cases
    else:
      print("Unhandled event! Please report to the developer")
      print(message.keys())
      print(message.values())

  def on_image_selected(self, image_path):
    sender_id = self.sender().parent().objectName()
    self.current_menu().images[sender_id] = image_path
    if "tb" in sender_id:
      keycode = self.tb_name_to_keycode(sender_id)
      self.set_img_to_touchbutton(image_path, keycode)
    elif "dis" in sender_id:
      side = sender_id[4]
      row = int(sender_id[3])
      self.set_img_to_touchdisplay(image_path, side, row)
    self.ld_widget.update()

  def on_action_selected(self, ld_action):
    sender_id = self.sender().parent().objectName()
    if ld_action:
      self.current_menu().actions[sender_id] = ld_action
    else:
      self.current_menu().actions[sender_id] = LdAction()

  def set_img_to_touchbutton(self, image_path, keycode):
    try:
      with open(image_path, "rb") as infile:
        image = Image.open(infile).convert("RGBA").resize((90, 90))
    except:
      image = Image.new("RGBA", (90, 90), "black")
    finally:
      self.ld_device.set_key_image(keycode, image)

  def set_img_to_touchdisplay(self, image_path, side, row, auto_refresh=True):
    if side == "L":
      x = 0
      display = "left"
    else:
      x = 480
      display = "right"

    try:
      with open(image_path, "rb") as infile:
        image = Image.open(infile).convert("RGBA").resize((60,60)).crop((0,-15,60,75))
    except:
      image = Image.new("RGBA", (60, 60), "black")
    finally:
      self.ld_device.draw_image(image, display=display, width=60, height=90, x=x, y=(row-1)*90, auto_refresh=auto_refresh)

  def current_ws(self):
    return self.config.workspaces[self.ws_keys.index(self.selected_ws)]

  def current_menu(self):
    if self.submenu_stack:
      return self.submenu_stack[-1].action
    else:
      return self.current_ws()

  def get_ws(self, key):
    return self.config.workspaces[self.ws_keys.index(key)]

  def tb_name_to_keycode(self, name):
    if "tb" in name and len(name) == 4:
      row = int(name[2])
      col = int(name[3])
      tb_id = (row-1)*4 + col-1
      return tb_id

  def td_name_to_xy_pos(td_name):
    if td_name[4] == "L":
      x = 0
    else:
      x = 480
    y = (int(td_name[3])-1)*90
    return x, y

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

  def load_workspace(self, ws):
    self.ld_widget.reset_images()
    self.ld_device.reset()

    for key, path in ws.images.items():
      widget = self.ld_widget.elements["root_" + key]
      if widget and path:
        widget.set_image(path)
        if "tb" in widget.objectName() :
          self.set_img_to_touchbutton(path, self.tb_name_to_keycode(key))
        elif "dis" in widget.objectName():
          self.set_img_to_touchdisplay(path, key[4], int(key[3]))
        else:
          print("load_ws: unknown image key, please report the bug to the developer %s" % widget.objectName())

    for key, action in ws.actions.items():
      widget = self.ld_widget.elements["root_" + key.strip("lr-")]
      if widget and action:
        widget.set_action(action, key)

    location = self.selected_ws
    if self.submenu_stack:
      location = location + " > " + " > ".join([s.name for s in self.submenu_stack])

    self.location.setText(location)
    self.ld_widget.update()

  def on_submenu_is_opened(self, submenu):
    self.load_workspace(submenu.action)
    self.submenu_opened.emit("root_dis1L")

  def on_submenu_is_closed(self, reload_menu=True):
    if reload_menu:
      self.load_workspace(self.current_menu())
    if not self.submenu_stack:
      self.submenu_closed.emit("root_dis1L")

  def on_touch_press(self, str_key, action):
    # if a submenu is currently opened and one of its key has been pressed
    if self.submenu_stack:
      if action.a_type == "submenu":
        self.submenu_stack.append(action)
        self.on_submenu_is_opened(action)
      elif action.a_type == "back":
        self.submenu_stack.pop()
        self.on_submenu_is_closed()
      else:
        action.execute()  # executes submenu command
    # no submenu is currently opened
    else:
      if action.a_type == "submenu":
        self.submenu_stack.append(action)
        self.on_submenu_is_opened(action)
      elif action.a_type == "back":
        print("back from basemenu, shouldn't happen!! Please report to the developper")
      else:
        action = self.current_menu().actions[str_key]
        action.execute() # executes main menu command

  def on_touchkey_press(self, key):
    row = floor(key/4)+1
    col = floor(key-(4*(row-1)))+1
    str_key = "tb" + str(row) + str(col)
    action = self.current_menu().actions[str_key]
    self.on_touch_press(str_key, action)

  def on_touchdisplay_press(self, x, y):
    str_key = self.td_pos_to_display_name(x, y)
    action = self.current_menu().actions[str_key]
    self.on_touch_press(str_key, action)

  def on_encoder_press(self, encoder):
    str_key = self.knob_to_enc_name(encoder)
    self.current_menu().actions[str_key].execute()

  def on_encoder_rotate(self, encoder, direction):
    str_key = self.knob_to_enc_name(encoder) + "-" + direction[0]
    self.current_menu().actions[str_key].execute()

  def on_workspace_press(self, ws_key):
    current_ws = self.selected_ws
    mb = self.ld_widget.modebuttons[current_ws]
    mb.setProperty("state", "unselected")
    mb.style().polish(mb)

    # switching workspace returns from any submenu context
    if self.submenu_stack:
      self.submenu_stack.clear()
      self.on_submenu_is_closed(False)

    self.ld_device.set_button_color(current_ws, (63, 63, 63))  # dim white
    self.selected_ws = ws_key
    self.ld_device.set_button_color(ws_key, "green")  # selected button in green

    self.load_workspace(self.get_ws(ws_key))

    mb = self.ld_widget.modebuttons[ws_key]
    mb.setProperty("state", "selected")
    mb.style().polish(mb)

  def close(self, event):
    if hasattr(self, "ld_device") and self.ld_device:
      self.ld_device.stop()
    sys.exit(0)

