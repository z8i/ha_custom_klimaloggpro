# Home Assistant Custom Component for TFA KlimaLogg Pro

TFA KlimaLogg Pro custom component to use with Home Assistant.

# Experimental! Prototype!

# Installation
Add this repository as a [custom repository](https://hacs.xyz/docs/navigation/settings#custom-repositories) of category Integration.
URL: ```https://github.com/z8i/ha_custom_klimaloggpro```

# USB Device!
TFA KlimaLogg Pro includes an USB Transceiver, which is used by this integration.
So the stick needs to be physically present in the Home Assistant Installation.

Tested and works under following circumstances:
[Manual Home Assistant Installation](https://www.home-assistant.io/docs/installation/raspberry-pi/) on a Raspberry Pi with Raspberry Pi OS (Raspbian)
USB-access is configured for user access:

It needs usb access to work properly, maybe you need to grant usb access
to the USB-Transceiver by 
* adding the user to plugdev group  
  `sudo adduser <username> plugdev` 
* add following rule to `/etc/udev/rules.d/50-usb-perms.rules`:  
  `SUBSYSTEM=="usb", ATTRS{idVendor}=="6666", ATTRS{idProduct}=="5555", GROUP="plugdev", MODE="0660"`

To check for success: 
```bash
  lsusb 
  Bus 001 Device 004: ID 6666:5555 Prototype product Vendor ID 
  # should show the klimlogg receiver, here bus 001 device 004 
  ls -l /dev/bus/usb/001/004 
  # expected output would be 
  crw-rw-rw- 1 root plugdev 189, 3 Dec 21 21:52 /dev/bus/usb/001/004
  # now group plugdev can access the device and everything should work
```

# More Info
This integration uses [kloggpro-Module]https://github.com/z8i/kloggpro) from [PyPI](https://pypi.org/project/kloggpro).

Do you like to test this integration? Please do! Let me know, if it works, or raise an [issue](https://github.com/z8i/ha_custom_klimaloggpro/issues)
