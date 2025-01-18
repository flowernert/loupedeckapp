import json, os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QObject, pyqtSignal
import pyautogui


class LdConfiguration(QObject):

  config_loaded = pyqtSignal()

  def __init__(self, profile="default"):
    super().__init__()
    self.profile = profile
    self.workspaces = [LdWorkspace() for i in range(8)]

  def save(self, profile_name):
    if profile_name:
      self.profile = profile_name
      with open("./Profiles/" + profile_name + ".json", "w") as file:
        json.dump(self.to_JSON(), file, indent=True)

  def load(self, json_file):
    try:
      with open("./Profiles/" + json_file + ".json", "r") as file:
        data = json.load(file)
        self.from_JSON(data)
        self.config_loaded.emit()
    except FileNotFoundError:
      print("File %s not found" % json_file)
    except json.decoder.JSONDecodeError:
      print("Can't read JSON in file %s" % json_file)

  def to_JSON(self):
    ldApp = QApplication.instance()
    s = {"profile": self.profile, 
           "workspaces": {i: ws.to_JSON() for i, ws in zip(ldApp.ws_keys, self.workspaces)}}
    return s
    
  def from_JSON(self, json_str):
    ldApp = QApplication.instance()
    self.profile = json_str["profile"]
    for i, ws_key in enumerate(ldApp.ws_keys):
      self.workspaces[i] = LdWorkspace.from_JSON(json_str["workspaces"][ws_key])


class LdWorkspace(QObject):

  def __init__(self, ws_profile="default"):
    super().__init__()
    self.profile = ws_profile
    action_keys = ["enc1L" , "enc1L-l", "enc1L-r",
                   "enc2L", "enc2L-l", "enc2L-r",
                   "enc3L", "enc3L-l", "enc3L-r",
                   "enc1R", "enc1R-l", "enc1R-r",
                   "enc2R", "enc2R-l", "enc2R-r",
                   "enc3R", "enc3R-l", "enc3R-r",
                   "dis1L", "dis2L", "dis3L",
                   "dis1R", "dis2R", "dis3R",
                   "tb11", "tb12", "tb13", "tb14",
                   "tb21", "tb22", "tb23", "tb24",
                   "tb31", "tb32", "tb33", "tb34"]
    self.actions = {key: LdAction() for key in action_keys}
                    
    self.images =  {"dis1L": "", "dis2L": "", "dis3L": "",
                    "dis1R": "", "dis2R": "", "dis3R": "",
                    "tb11": "", "tb12": "", "tb13": "", "tb14": "",
                    "tb21": "", "tb22": "", "tb23": "", "tb24": "",
                    "tb31": "", "tb32": "", "tb33": "", "tb34": ""}

  def save(self, profile_name):
    self.profile = profile_name
    with open("./Profiles/" + profile_name + ".json", "w") as file:
      json.dump(self.__dict__, file)

  def load(self, json_file):
    data = None
    with open("./Profiles/" + json_file + ".json", "r") as file:
      data = json.load(file)
    for key, value in data.items():
      setattr(self, key, value)
      
  def to_JSON(self):
    s = {"profile": self.profile,
          "actions": {key: action.to_JSON() for key, action in self.actions.items()},
          "images": {key: image for key, image in self.images.items()}}
    return s

  def from_JSON(json_data):
    ldw = LdWorkspace(ws_profile=json_data["profile"])
    for key, action in json_data["actions"].items():
      ldw.actions[key] = LdAction.from_JSON(action)
    for key, image in json_data["images"].items():
      ldw.images[key] = image
    return ldw


class LdAction (QObject):
  type ActionType = Literal["command", "hotkey", "submenu", "back", "none"]

  def __init__(self, action_type: ActionType ="none", action="", summary=""):
    super().__init__()
    self.a_type = action_type
    self.action = action
    if summary:
      self.summary = summary
    elif action_type == "command" or action_type == "hotkey" or action_type == "back":
      self.summary = self.action
    else:
      self.summary = "none"

  def execute(self):
    if self.a_type == "command":
      os.system(self.action)
    elif self.a_type == "hotkey":
      hotkey = self.action.lower().split("+")
      pyautogui.hotkey(hotkey)
    else:
      print("no action to execute for action type %s" % self.a_type)

  def to_JSON(self):
    if isinstance(self.action, str):
      s = {"a_type": str(self.a_type), "action": self.action}
    else:
      print("this shouldn't happen, please report the bug to the developer'")
    return s

  def from_JSON(json_str):
    if json_str["a_type"] != "submenu":
      lda = LdAction(action_type=json_str["a_type"], action=json_str["action"])
      return lda
    else:
      lds = LdSubmenu.from_json(json_str)
      return lds

  def __str__(self):
    return "%s : %s" % (self.a_type, self.action)


class LdSubmenu (LdAction):
  def __init__(self, name, action_type="submenu", action=None, summary=""):
    super().__init__(action_type, action, summary)
    self.a_type = "submenu"
    if action:
      self.action = action
    else:
      self.action = LdWorkspace()
    self.action.ws_profile = name
    self.summary = ""
    self.name = ""
    self.setName(name)

  def execute(self):
    print("submenu %s execute, this is a bug and shouldn't happen" % self.summary)

  def to_JSON(self):
    s = {"a_type" : self.a_type, "action": self.action.to_JSON()}
    return s

  def from_json(json_str):
    ws = LdWorkspace.from_JSON(json_str["action"])
    name = json_str["action"]["profile"]
    lds = LdSubmenu(name=name, action=ws)
    return lds

  def setName(self, s):
    self.name = s
    self.summary = "%s %s" % (self.a_type, self.name)
    self.action.profile = self.name

