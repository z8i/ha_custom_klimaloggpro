# TFA KlimaLogg Pro for Home Assistant

TFA KlimaLogg Pro custom component to use with Home Assistant.

## Experimental! Prototype!

# Installation
Use HACS and add this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories) of category Integration.
URL: ```https://github.com/z8i/ha_custom_klimaloggpro```

Installation steps:

1.    Add repo to HACS
2.    Install custom integration " TFA KlimaLogg pro BETA" via HACS
3.    Restart Home Assistant
4.    Go to Settings-Integrations in Home Assistant
5.    Add Integration "Klimalogg".. this takes a while, please be patient!
6.    Select the sensors you have connected to you base station
7.    finish!

During step 5 i usually press the USB buttom some times (hold it a bit), until the base station is connected with the raspberry. If you use HAOS all the custom usb device right management stuff is not neccessary. Once the station is connected, you can see the live data in Home Assistant, the connection will stay permanent. 

# Attention: USB Device!
TFA KlimaLogg Pro weather station includes an USB Transceiver, which is used by this integration.
So the stick needs to be physically connected to the computer which runs Home Assistant.

## Tested and works under following circumstances:
### [Home Assistant Operating System (HAOS)](https://www.home-assistant.io/installation/raspberrypi/#install-home-assistant-operating-system)
Tested on a Raspberry 4 Model B

### [Manual Home Assistant Installation](https://www.home-assistant.io/docs/installation/raspberry-pi/) on a Raspberry Pi with Raspberry Pi OS (Raspbian)
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
This integration uses [kloggpro-Module](https://github.com/z8i/kloggpro) from [PyPI](https://pypi.org/project/kloggpro).

Do you like to test this integration? Please do! Let me know, if it works, or raise an [issue](https://github.com/z8i/ha_custom_klimaloggpro/issues)
