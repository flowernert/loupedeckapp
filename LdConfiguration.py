from PyQt5.QtCore import QObject

class LdConfiguration(QObject):
  def __init__(self):
    super().__init__()
    self.profile = "default"
    self.actions = {"enc1L": "", "enc2L": "", "enc3L": "",
                    "enc1R": "", "enc2R": "", "enc3R": "",
                    "dis1L": "", "dis2L": "", "dis3L": "",
                    "dis1R": "", "dis2R": "", "dis3R": "",
                    "tb11": "", "tb12": "", "tb13": "", "tb14": "",
                    "tb21": "", "tb22": "", "tb23": "", "tb24": "",
                    "tb31": "", "tb32": "", "tb33": "", "tb34": "",
                    "mb0": "", "mb1": "", "mb2": "", "mb3": "",
                    "mb4": "", "mb5": "", "mb6": "", "mb7": ""}
                    
    self.images =  {"dis1L": "", "dis2L": "", "dis3L": "",
                    "dis1R": "", "dis2R": "", "dis3R": "",
                    "tb11": "", "tb12": "", "tb13": "", "tb14": "",
                    "tb21": "", "tb22": "", "tb23": "", "tb24": "",
                    "tb31": "", "tb32": "", "tb33": "", "tb34": ""}
    
