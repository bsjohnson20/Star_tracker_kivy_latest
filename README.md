This is my computer science project, despite being called a star tracker it doesn't actually do that, instead it controls a nodemcu which sends I2C signals to an Arduino which controls a stepper motor in a barn door tracker. 

The main goals were that it was designed to imitate an IOT controller app such as Google home or nest hub. Though my skills are limited I have came far, though I wished I had learnt kotlin as that's way more effective for coding an app since Google supports it.

Anyway the basic functions:

Generates a list of registered devices using a dictionary stored in devices.json or something.
Each device will have it's own control setup depending on whether it's a v1, v2 or v3 etc.
Has a button panel to tell a device to step forward, back or stop. As well as having a speed slider which is a percentage.
Able to add a device, change the device's theme using kivymds colour picker widget.
Can check whether a device is online by pinging the device, though this doesn't seem to work on android, though I'm not sure.
