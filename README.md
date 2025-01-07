# loupedeckapp

Loupedeck live configuration application for linux. 

## Goal

This is an attemps to provide Linux platforms with something similar to what the original loupedeck app offer on Windows and MacOS platform.

## Current state

Can program touchbutton images and can configure shell commands to be executed when a touchbutton or an encoder is pressed
Can save images and commands to a profile file, can restore the profile, restoring will update the GUI and load back images to the loupedeck device 

## Pre-requisite

You will need to allow the device to be accessible for a linux group your linux user is in, to do so add a udev rule in your system.
On my system I created it in /etc/udev/rules.d/99-loupedeck-live.rules.
Then as root user add the following content to the file

```
SUBSYSTEM=="tty", ATTRS{idProduct}=="0004", ATTRS{idVendor}=="2ec2", GROUP="plugdev", MODE="0660"
```

Be sure your user is indeed in the `plugdev` group for this to work properly.


