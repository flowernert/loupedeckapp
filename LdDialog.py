from PyQt5.QtWidgets import QWidget, QDialog, QDialogButtonBox, QLineEdit, QLabel, QFileDialog, QButtonGroup, QPushButton, QKeySequenceEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QApplication, QMainWindow
from PyQt5.QtGui import QKeySequence, QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from PIL import Image, ImageColor
from pathlib import Path

from LdConfiguration import LdAction, LdSubmenu
import LdWidget as ldw


class ConfigActionDialog (QDialog):
  action_selected = pyqtSignal(LdAction)

  selected_action = None

  def __init__(self, parent):
    QDialog.__init__(self, parent)
    self.setModal(True)
    self.setWindowTitle("Configure action when pressed")

    self.action_type_select = QButtonGroup()
    self.b_cmd = QPushButton("Execute a command")
    self.b_hk = QPushButton("Execute a hotkey")
    self.b_sub = QPushButton("Open a submenu")

    self.b_cmd.clicked.connect(self.display_cmd_selected)
    self.b_hk.clicked.connect(self.display_hk_selected)
    self.b_sub.clicked.connect(self.display_submenu_config_selected)

    self.user_action = QLabel("Select command, hotkey or submenu")

    self.b_cmd.setFocus()
    self.command_input = QLineEdit()
    self.command_input.setVisible(False)
    self.command_input.setEnabled(False)
    self.command_input.textEdited.connect(self.on_cmd_updated)

    self.hotkey_input = QKeySequenceEdit()
    self.hotkey_input.setVisible(False)
    self.hotkey_input.setEnabled(False)
    self.hotkey_input.editingFinished.connect(self.on_key_sequence_updated)

    self.submenu_name_input = QLineEdit()
    self.submenu_name_input.setVisible(False)
    self.submenu_name_input.setEnabled(False)
    self.submenu_name_input.textEdited.connect(self.on_submenu_name_updated)

    self.but_box = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
    self.but_box.accepted.connect(self.accept)
    self.but_box.rejected.connect(self.reject)
    self.but_box.setEnabled(False)

    self.b_reset = QPushButton("Reset action")
    self.b_reset.clicked.connect(self.reset_action_selection)
    self.b_reset.setEnabled(False)

    # restore previous action if existing
    action = QApplication.instance().current_menu().actions[parent.objectName()]
    if action:
      self.selected_action = action
      if action.a_type == "command":
        self.b_cmd.setDisabled(True)
        self.b_cmd.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
        self.b_hk.setDisabled(True)
        self.b_sub.setDisabled(True)
        self.user_action.setVisible(False)
        self.command_input.setVisible(True)
        self.command_input.setText(action.action)
        self.command_input.setFocus()
        self.hotkey_input.setVisible(False)
        self.hotkey_input.setEnabled(False)
        self.submenu_name_input.setVisible(False)
        self.submenu_name_input.setEnabled(False)
      elif action.a_type == "hotkey":
        self.b_hk.setDisabled(True)
        self.b_hk.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
        self.b_cmd.setDisabled(True)
        self.b_sub.setDisabled(True)
        self.user_action.setVisible(False)
        self.hotkey_input.setVisible(True)
        self.hotkey_input.setKeySequence(QKeySequence(action.action))
        self.hotkey_input.setEnabled(False)
        self.command_input.setVisible(False)
        self.command_input.setEnabled(False)
        self.submenu_name_input.setVisible(False)
        self.submenu_name_input.setEnabled(False)
      elif action.a_type == "submenu":
        self.b_sub.setDisabled(True)
        self.b_sub.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
        self.b_cmd.setDisabled(True)
        self.b_hk.setDisabled(True)
        self.user_action.setVisible(False)
        self.submenu_name_input.setVisible(True)
        self.submenu_name_input.setText(action.name)
        self.submenu_name_input.setEnabled(False)
        self.hotkey_input.setVisible(False)
        self.hotkey_input.setEnabled(False)
        self.command_input.setVisible(False)
        self.command_input.setEnabled(False)

      if action.a_type != "none":
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

  def display_cmd_selected(self):
    self.b_hk.setDisabled(True)
    self.b_cmd.setDisabled(True)
    self.b_sub.setDisabled(True)
    self.b_cmd.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
    self.user_action.setVisible(False)
    self.hotkey_input.setVisible(False)
    self.command_input.setVisible(True)
    self.command_input.setEnabled(True)
    self.command_input.setFocus()
    self.command_input.setClearButtonEnabled(True)
    self.b_reset.setEnabled(True)

  def display_hk_selected(self):
    self.b_cmd.setDisabled(True)
    self.b_hk.setDisabled(True)
    self.b_sub.setDisabled(True)
    self.b_hk.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
    self.user_action.setVisible(False)
    self.command_input.setVisible(False)
    self.hotkey_input.setVisible(True)
    self.hotkey_input.setEnabled(True)
    self.hotkey_input.setFocus()
    self.b_reset.setEnabled(True)

  def display_submenu_config_selected(self):
    self.b_hk.setDisabled(True)
    self.b_cmd.setDisabled(True)
    self.b_sub.setDisabled(True)
    self.b_sub.setStyleSheet("QPushButton { border: 2px solid dimgrey; }")
    self.user_action.setVisible(False)
    self.command_input.setVisible(False)
    self.hotkey_input.setVisible(False)
    self.submenu_name_input.setVisible(True)
    self.submenu_name_input.setEnabled(True)

  def on_key_sequence_updated(self):
    self.but_box.setEnabled(True)

  def on_cmd_updated(self, str):
    if str:
      self.but_box.setEnabled(True)
    else:
      self.but_box.setEnabled(False)

  def on_submenu_name_updated(self, str):
    self.on_cmd_updated(str)

  def on_submenu_configured(self, submenu_data):
    self.selected_action = submenu_data
    self.submenu_name_input.setEnabled(True)
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

  def accept(self):
    ldApp = QApplication.instance()
    if self.command_input.isVisible():
      self.selected_action = LdAction("command", self.command_input.text())
      self.action_selected.emit(self.selected_action)
    elif self.hotkey_input.isVisible():
      self.selected_action = LdAction("hotkey", self.hotkey_input.keySequence().toString())
      self.action_selected.emit(self.selected_action)
    elif self.submenu_name_input.isVisible():
      name = self.submenu_name_input.text()
      print("name :%s" % name)
      submenu = LdSubmenu(name)
      submenu.setName(name)
      self.selected_action = submenu

      # top left display reserved for submenu back button
      submenu.action.images["dis1L"] = ldApp.back_but_path
      submenu.action.actions["dis1L"] = LdAction(action_type="back", action="back")

      self.action_selected.emit(self.selected_action)
    else:
      print("no action selected, this is a bug and shouldn't happen', please report to the developer")
    super().accept()

  def reject(self):
    if self.selected_action is None:  # reset button has been pressed and no other action has been set
      self.action_selected.emit(LdAction())
    super().reject()


class ConfigImgDialog (QDialog):
  image_selected = pyqtSignal(str)

  def __init__(self, parent):
    QDialog.__init__(self, parent)
    self.setModal(True)
    self.setWindowTitle("Configure image to be displayed")

    self.user_img = QLineEdit(self)
    self.user_img.setClearButtonEnabled(True)
    ldApp = QApplication.instance()
    value = ldApp.current_menu().images[parent.objectName()]
    self.user_img.setText(value)

    path_select_but = QPushButton("Open file selector ...", self)
    path_select_but.clicked.connect(self.path_selection_popup)
    path_select_but.setFocus()

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
    if filename and ok:
      path = Path(filename)
      self.user_img.setText(str(path))
      self.but_box.button(QDialogButtonBox.Ok).setDefault(True)
      self.but_box.button(QDialogButtonBox.Ok).setFocus()

  def accept(self):
    self.image_selected.emit(self.user_img.text())
    super().accept()

  def reject(self):
    super().reject()


class ConfigSubmenuDialog(QDialog):

  submenu_configured = pyqtSignal(ldw.LdSubmenu)

  # 1st parent is ConfigActionDialog that opened the config submenu dialog, 
  # parent_key_id is the key in the current workspace that led to opening the config submenu dialog
  def __init__(self, parent, submenu_name=""):
    QDialog.__init__(self, parent)
    self.setModal(True)
    self.submenu = ldw.SubmenuConfigurationWidget(self, "test")

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

