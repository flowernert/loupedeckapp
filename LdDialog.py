from PyQt5.QtWidgets import QWidget, QDialog, QDialogButtonBox, QLineEdit, QLabel, QFileDialog, QButtonGroup, QPushButton, QKeySequenceEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QApplication, QMainWindow
from PyQt5.QtGui import QKeySequence, QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from PIL import Image, ImageColor
from pathlib import Path

from LdConfiguration import LdAction
import LdWidget as ldw


class ConfigActionDialog (QDialog):
  action_selected = pyqtSignal(LdAction)

  selected_action = None

  def __init__(self, parent):
    QDialog.__init__(self, parent)
    self.setWindowTitle("Configure action when pressed")

    self.action_type_select = QButtonGroup()
    self.b_cmd = QPushButton("Execute a command")
    self.b_hk = QPushButton("Execute a hotkey")
    self.b_sub = QPushButton("Open a submenu")

    self.b_cmd.clicked.connect(self.display_cmd_select)
    self.b_hk.clicked.connect(self.display_hk_select)
    self.b_sub.clicked.connect(self.display_submenu_config)

    self.user_action = QLabel("Select command or hotkey")
    self.hotkey_input = QKeySequenceEdit()
    self.hotkey_input.editingFinished.connect(self.update_key_sequence)
    self.hotkey_input.setVisible(False)
    self.command_input = QLineEdit()
    self.command_input.setVisible(False)
    self.submenu_name_input = QLineEdit()
    self.submenu_name_input.setVisible(False)

    self.but_box = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
    self.but_box.accepted.connect(self.accept)
    self.but_box.rejected.connect(self.reject)
    self.but_box.setDisabled(True)
    self.b_reset = QPushButton("Reset action")
    self.b_reset.clicked.connect(self.reset_action_selection)
    self.b_reset.setDisabled(True)

    # restore previous action if existing
    action = QApplication.instance().current_ws().actions[parent.objectName()]
    if action:
      self.selected_action = action
      if action.a_type == "command":
        self.b_cmd.setDisabled(True)
        self.b_cmd.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
        self.b_hk.setDisabled(True)
        self.user_action.setVisible(False)
        self.command_input.setVisible(True)
        self.command_input.setText(action.action)
        self.command_input.setFocus()
        self.hotkey_input.setVisible(False)
        self.hotkey_input.setEnabled(False)
      elif action.a_type == "hotkey":
        self.b_hk.setDisabled(True)
        self.b_hk.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
        self.b_cmd.setDisabled(True)
        self.user_action.setVisible(False)
        self.hotkey_input.setVisible(True)
        self.hotkey_input.setKeySequence(QKeySequence(action.action))
        self.hotkey_input.setEnabled(False)
        self.command_input.setVisible(False)
        self.command_input.setEnabled(False)
      elif action.a_type == "submenu":
        print("not implemented yet")
      self.b_reset.setEnabled(True)
      self.but_box.setEnabled(True)

    action_but_layout = QHBoxLayout()
    action_but_layout.addWidget(self.b_cmd)
    action_but_layout.addWidget(self.b_hk)
    action_but_layout.addWidget(self.b_sub)

    reset_accept_layout = QHBoxLayout()
    reset_accept_layout.addWidget(self.b_reset)
    reset_accept_layout.addWidget(self.but_box)

    vlayout = QVBoxLayout()
    vlayout.addLayout(action_but_layout)
    vlayout.addWidget(self.user_action)
    vlayout.addWidget(self.hotkey_input)
    vlayout.addWidget(self.command_input)
    vlayout.addWidget(self.submenu_name_input)
    vlayout.addLayout(reset_accept_layout)

    self.setLayout(vlayout)

  def display_cmd_select(self):
    self.b_hk.setDisabled(True)
    self.b_cmd.setDisabled(True)
    self.b_sub.setDisabled(True)
    self.b_cmd.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
    self.user_action.setVisible(False)
    self.hotkey_input.setVisible(False)
    self.command_input.setVisible(True)
    self.command_input.setFocus()
    self.command_input.setClearButtonEnabled(True)
    self.b_reset.setEnabled(True)
    self.but_box.setEnabled(True)

  def display_hk_select(self):
    self.b_cmd.setDisabled(True)
    self.b_hk.setDisabled(True)
    self.b_sub.setDisabled(True)
    self.b_hk.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
    self.user_action.setVisible(False)
    self.command_input.setVisible(False)
    self.hotkey_input.setVisible(True)
    self.hotkey_input.setEnabled(True)
    self.hotkey_input.setFocus()

  def display_submenu_config(self):
    self.b_hk.setDisabled(True)
    self.b_cmd.setDisabled(True)
    self.b_sub.setDisabled(True)
    self.b_sub.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
    self.user_action.setVisible(False)
    self.command_input.setVisible(False)
    self.hotkey_input.setVisible(False)
    self.submenu_name_input.setVisible(True)
    self.submenu_name_input.setEnabled(False)
    submenu = ConfigSubmenuDialog(self, "test")
    submenu.submenu_configured.connect(self.on_submenu_configured)
    submenu.show()

  def update_key_sequence(self):
    self.b_reset.setEnabled(True)
    self.but_box.setEnabled(True)

  def reset_action_selection(self):
    self.b_hk.setStyleSheet("")
    self.b_hk.setEnabled(True)
    self.b_cmd.setStyleSheet("")
    self.b_cmd.setEnabled(True)
    self.b_cmd.setFocus()
    self.b_sub.setStyleSheet("")
    self.b_sub.setEnabled(True)
    self.hotkey_input.clear()
    self.hotkey_input.setVisible(False)
    self.command_input.clear()
    self.command_input.setVisible(False)
    self.submenu_name_input.clear()
    self.submenu_name_input.setVisible(False)
    self.user_action.setVisible(True)
    self.user_action.setText("Select command, hotkey or submenu")
    self.b_reset.setDisabled(True)
    self.but_box.setDisabled(True)
    self.selected_action = None

  def on_submenu_configured(self, submenu_data):
    #print(submenu_data.to_JSON())
    self.selected_action = submenu_data
    self.submenu_name_input.setEnabled(True)
    self.b_reset.setEnabled(True)
    self.but_box.setEnabled(True)

  def accept(self):
    ldApp = QApplication.instance()
    if self.command_input.isVisible():
      self.selected_action = LdAction("command", self.command_input.text())
      self.action_selected.emit(self.selected_action)
    elif self.hotkey_input.isVisible():
      self.selected_action = LdAction("hotkey", self.hotkey_input.keySequence().toString())
      self.action_selected.emit(self.selected_action)
    elif self.submenu_name_input.isVisible():
      s = self.submenu_name_input.text()
      if s:
        self.selected_action.setName(s)
      self.action_selected.emit(self.selected_action)
    else:
      print("no action selected, this is a bug and shouldn't happen', please report to the developer")
    super().accept()

  def reject(self):
    if self.selected_action is None:  # reset button has been pressed and no other action has been set
      self.action_selected.emit(None)
    super().reject()


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


class ConfigImgDialog (QDialog):
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

class ConfigSubmenuDialog(QDialog):

  submenu_configured = pyqtSignal(ldw.LdSubmenu)

  def __init__(self, parent, submenu_name=""):
    QDialog.__init__(self, parent)
    self.submenu = ldw.SubmenuConfigurationWidget("test")

    self.but_box = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
    self.but_box.accepted.connect(self.accept)
    self.but_box.rejected.connect(self.reject)

    layout = QVBoxLayout()
    layout.addWidget(self.submenu)
    layout.addWidget(self.but_box)
    self.setLayout(layout)
    self.setWindowTitle("Edit submenu elements")

  def accept(self):
    self.submenu_configured.emit(self.submenu.submenu_data)
    super().accept()

  def reject(self):
    super().reject()

