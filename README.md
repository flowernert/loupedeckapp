# loupedeckapp

Loupedeck live configuration application for linux. 

## Goal

This is an attemps to provide Linux platforms with something similar to what the original loupedeck app offers on Windows and MacOS platform.

## Current status

The following features are implemented, tested and functional on my Loupedeck Live device. Feedback from users would be highly appreciated at this point.

Can program touchbutton images and can configure actions to be executed when a touchbutton or an encoder is pressed/rotated.

At this point of the development the actions available are 

* execute shell commands

* send a hotkey shorto the OS

* open a submenu on the Loupedeck device, which can hold itself other commands

Can save images and actions to a profile file, can restore the profile, restoring will update the GUI and load back images to the loupedeck device.

Workspaces concept implemented on physical buttons 0-7

## Currently working on

Packaging the app for layman users being able to install and use it without hassle

## Next features on roadmap

### Next features in priority

* Implement a handler to get the currently focused app from the desktop manager and alter the current workspace based on it.

* Use left display to show where you are in the workspace/submenu hierarchy

### Next by order or priority

* Implement a configurator for left/right display, allowing to use them as a unique display or split them into several buttons

* Provide a few ready-to-use workspace profiles for lazy users

* Fancier GUI


## Pre-requisite

You will need to allow the device to be accessible for a linux group your linux user is in, to do so add a udev rule in your system.
On my system I created it in /etc/udev/rules.d/99-loupedeck-live.rules.
Then as root user add the following content to the file

```
SUBSYSTEM=="tty", ATTRS{idProduct}=="0004", ATTRS{idVendor}=="2ec2", GROUP="plugdev", MODE="0660"
```

Be sure your user is indeed in the `plugdev` group for this to work properly.

## Dependencies

This projects depends on the following libraries, this means it won't work if you don't install them beforehand on your system

`PyQt5`, directly installable from most Linux OS repositories

[`Loupedeck`](https://github.com/devleaks/python-loupedeck-live) python library from Devleaks to interface with the device

[`pyautogui`](https://github.com/asweigart/pyautogui) library from Asweigart to send hotkeys to the system

`python-xlib`is required from `pyautogui` on Linux platforms and is likely to be installable from your OS repositories

