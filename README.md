# loupedeckapp

Loupedeck live configuration application for linux. 

## Goal

This is an attemps to provide Linux platforms with something similar to what the original loupedeck app offer on Windows and MacOS platform.

## Current status

Can program touchbutton images and can configure actions(shell commands or hotkey) to be executed when a touchbutton or an encoder is pressed/rotated

Can save images and actions to a profile file, can restore the profile, restoring will update the GUI and load back images to the loupedeck device 

Workspaces concept implemented on physical buttons 0-7

## Next features on roadmap

### In priority

* Implement a submenu feature, allowing to display a sub-workspace by pressing a touchdisplay action. 
    
    It must implements a return back control that restore the previous workspace context
    
    It must be able to temporary alter the actions and images of each control on the device.
    
    Maybe use left display to show where you are in the workspace/submenu hierarchy

* Implement a handler to get the currently focused app from the desktop manager and alter the current workspace based on it.

### Next by order or priority

Implement a configurator for left/right display, allowing to use them as a unique display or split them into several buttons

Provide a few ready-to-use workspace profiles for lazy users

Fancier GUI


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

