import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject


class LdConfiguration(QObject):

  def __init__(self, profile="default"):
    super().__init__()
    self.profile = profile
    self.workspaces = [LdWorkspace() for i in range(8)]

  def save(self, profile_name):
    self.profile = profile_name
    with open("./Profiles/" + profile_name + ".json", "w") as file:
      json.dump(self.to_JSON(), file, indent=True)

  def load(self, json_file):
    ldApp = QApplication.instance()
    data = None
    with open("./Profiles/" + json_file + ".json", "r") as file:
      data = json.load(file)
      self.profile = data["profile"]
      for i, ws_key in enumerate(ldApp.ws_keys):
        for key, value in data["workspaces"][ws_key].items():
          setattr(self.workspaces[i], key, value)

  def to_JSON(self):
    ldApp = QApplication.instance()
    return {"profile": self.profile, "workspaces": {i: ws.__dict__ for i, ws in zip(ldApp.ws_keys, self.workspaces)}}


class LdWorkspace(QObject):

  def __init__(self, ws_profile="default"):
    super().__init__()
    self.profile = ws_profile
    self.actions = {"enc1L": "", "enc1L-l": "", "enc1L-r": "",
                    "enc2L": "", "enc2L-l": "", "enc2L-r": "",
                    "enc3L": "", "enc3L-l": "", "enc3L-r": "",
                    "enc1R": "", "enc1R-l": "", "enc1R-r": "",
                    "enc2R": "", "enc2R-l": "", "enc2R-r": "",
                    "enc3R": "", "enc3R-l": "", "enc3R-r": "",
                    "dis1L": "", "dis2L": "", "dis3L": "",
                    "dis1R": "", "dis2R": "", "dis3R": "",
                    "tb11": "", "tb12": "", "tb13": "", "tb14": "",
                    "tb21": "", "tb22": "", "tb23": "", "tb24": "",
                    "tb31": "", "tb32": "", "tb33": "", "tb34": ""}
                    
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
 

