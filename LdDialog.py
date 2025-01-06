from PyQt5.QtWidgets import QWidget, QDialog, QDialogButtonBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from PIL import Image, ImageColor

class ConfigCmd (QDialog):
  def __init__(self, parent):
    QDialog.__init__(self, parent)
    
    self.setWindowTitle("Configure command to be executed when the button is pressed")
    
    self.user_cmd = QLineEdit(self)
    value = parent.parent().config.actions[parent.objectName()]
    self.user_cmd.setText(value)
    
    self.but_box = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
    self.but_box.accepted.connect(self.accept)
    self.but_box.rejected.connect(self.reject)
    
    layout = QVBoxLayout()
    layout.addWidget(self.user_cmd)
    layout.addWidget(self.but_box)
    self.setLayout(layout)
  
  def accept(self):
    user_cmd = self.user_cmd.text()
    super().accept()
    
    
  def reject(self):
    print("Cancel pressed")
    print(str(QDialogButtonBox.Cancel))
    super().reject()

