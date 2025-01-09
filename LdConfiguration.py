import json
from PyQt5.QtCore import QObject


class LdConfiguration(QObject):

  def __init__(self):
    super().__init__()
    self.profile = "default"
    self.actions = {"enc1L-p": "", "enc1L-ccw": "", "enc1L-cw": "",
                    "enc2L-p": "", "enc2L-ccw": "", "enc2L-cw": "",
                    "enc3L-p": "", "enc3L-ccw": "", "enc3L-cw": "",
                    "enc1R-p": "", "enc1R-ccw": "", "enc1R-cw": "",
                    "enc2R-p": "", "enc2R-ccw": "", "enc2R-cw": "",
                    "enc3R-p": "", "enc3R-ccw": "", "enc3R-cw": "",
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

