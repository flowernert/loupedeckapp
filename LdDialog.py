from PyQt5.QtWidgets import QWidget, QDialog, QDialogButtonBox, QLineEdit, QFileDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PIL import Image, ImageColor
from pathlib import Path

class ConfigCmd (QDialog):
  cmd_selected = pyqtSignal(str)  #command

  def __init__(self, parent):
    QDialog.__init__(self, parent)
    self.setWindowTitle("Configure command to be executed when pressed")

    self.user_cmd = QLineEdit(self)
    self.user_cmd.setClearButtonEnabled(True)
    value = QApplication.instance().current_ws().actions[parent.objectName()]
    if value:
      self.user_cmd.setText(value)
    else:
      self.user_cmd.setText("./Launcher/")
    self.but_box = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
    self.but_box.accepted.connect(self.accept)
    self.but_box.rejected.connect(self.reject)

    layout = QVBoxLayout()
    layout.addWidget(self.user_cmd)
    layout.addWidget(self.but_box)
    self.setLayout(layout)
  
  def accept(self):
    self.cmd_selected.emit(self.user_cmd.text())
    super().accept()

  def reject(self):
    super().reject()


class ConfigImg (QDialog):
  image_selected = pyqtSignal(str)

  def __init__(self, parent):
    QDialog.__init__(self, parent)
    self.setWindowTitle("Configure image to be displayed")

    self.user_img = QLineEdit(self)
    self.user_img.setClearButtonEnabled(True)
    ldApp = QApplication.instance()
    value = ldApp.current_ws().images[parent.objectName()]
    self.user_img.setText(value)

    path_select_but = QPushButton("Open file selector ...", self)
    path_select_but.clicked.connect(self.path_selection_popup)

    self.but_box = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
    self.but_box.accepted.connect(self.accept)
    self.but_box.rejected.connect(self.reject)

    layout = QVBoxLayout()
    layout.addWidget(self.user_img)
    layout.addWidget(path_select_but)
    layout.addWidget(self.but_box)
    self.setLayout(layout)

  def path_selection_popup(self):
    filename, ok = QFileDialog.getOpenFileName(self,
                                         "Select the image to load",
                                         "./Images/",
                                         "Images (*.png *.jpg)")
    if filename:
      path = Path(filename)
      self.user_img.setText(str(path))
      self.image_selected.emit(str(path))

  def accept(self):
    super().accept()

  def reject(self):
    super().reject()

