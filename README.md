# CROPP
Directory containing software for the CubeSat Research of Plant Platforms (CROPP) student design project.

### Python UI
"cropp_tkinter_ui.py" is the central component of all the software and allows for all system functions to be handled in one user interface. Functions include monitoring a live camera feed, monitoring temperature, pressure, humidity, and CO2 data, controlling the plant watering system, controlling the lights, and controlling the fans/ventilation. The plant watering system is controlled via sending commands to a Tic T500 Stepper Motor Controller. The temperature, pressure, humidity, and CO2 data is gathered and transmitted by an Adafruit multi-sensor, and all other functionalities are performed by sending instructions to Arduino Uno microcontrollers.

### Arduino/Adafruit Programs
"flow_meter_default.ino", "relay_lights_fan_control.ino", and "Payload_Sensor_Code.ino" are all Arduino programs that interface with the main "cropp_tkinter_ui.py" program to allow for control and monitoring of the previously mentioned subsystems.
 
### CROPP Software Showcase
Video showcasing all the software in action, including the user interface and the physical apparatus it controls. Visit https://drive.google.com/file/d/1v9CHCOqzct9a3TIqTwErZQ4D_ea-ftN1/view?usp=sharing
