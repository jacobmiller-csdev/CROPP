#from https://www.geeksforgeeks.org/python-gui-tkinter/
#coded by Briana Student and Jacob Miller

#IMPORT MODULES
from tkinter import *
import webview
from tkinter import ttk
from tkinter import filedialog, messagebox
import calendar
from PIL import ImageTk, Image
from time import sleep
from time import strftime
from time import localtime
from picamera import PiCamera
from picamera import PiResolution
import io
import logging
import socketserver
import threading
from threading import Condition, Thread
from http import server
import imageio
import os
import subprocess
import yaml
import serial


#CREATE MAIN WINDOW
cameraGUI=Tk()
cameraGUI.title("Camera GUI Window")
cameraGUI.geometry('1100x600')

#Serial communications stuff
#If this throws errors then do ls -l /dev/tty* to check what's available (also try unplug replug)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

#Sensor Stuff

sensor_ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1) #serial port might accidentally change
#sensor_ser = serial.Serial('/dev/ttyACM2', 115200, timeout=1)
sensor_ser.reset_input_buffer()

#GLOBAL FUNCTIONS
    #time
def time():
    DateAndTime=strftime('%H:%M:%S  \t%d %b %Y')
    timeKeeper.config(text=DateAndTime)
    timeKeeper.after(1000, time)

def lightSwitchTime(num):
    if(num == 0):
        ser.write(b'T')
        timeKeeperLight.config(text="ON")
        timeKeeperLight.after(10000, lightSwitchTime, 1)
    else:
        ser.write(b't')
        timeKeeperLight.config(text="OFF")
        timeKeeperLight.after(10000, lightSwitchTime, 0)
    
    #click See All Pics button
def browseClicked():
    global chosenImage
    # Open File Explorer Window
    chosenPath=filedialog.askopenfilename(
        initialdir="/home/pi/Desktop/cameraGUI/allPictures",
        title="Select a File",
        filetypes=(("Image files","*.png"),("all files","*.*")))
    # Create Image Window
    imageGUI=Toplevel(cameraGUI)
    imageGUI.title(str(chosenPath))
    # open picture
    chosenImage = ImageTk.PhotoImage(file=chosenPath)
    dispImage=Label(imageGUI,image=chosenImage).grid(row=1,column=1)

#Jake did this for testing live feed
#Idea: continuously loop this function in a thread to update the feed
#This class WORKS NOW :D
    
   
class videoClass(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self)
        self._stop_event = threading.Event()
    
    def stop(self):
        self._stop_event.set()
    
    def stopped(self):
        return self._stop_event.isSet()
    
    def run(self):
        #global stop_thread
        #stop_thread = False
        while(True):
            #Function to capture live image frame
            liveCapture()
            
            #Update display with live image frame
            LFPH = ImageTk.PhotoImage(
                file='/home/pi/Desktop/cameraGUI/allPictures/LiveFeed.png')
            LFFrame = Label(cameraGUI, image=LFPH).grid(column=0,row=0)
            LFTitle = Label(cameraGUI, text="Live Feed").grid(column=0,row=1)
            
            if self.stopped():
                return
            
            #Update every 3 seconds
            sleep(3)

 
#Live Capture function for Video Class
def liveCapture():
    
    camera=PiCamera()
    camera.resolution = (1280,720)
    camera.capture(
        '/home/pi/Desktop/cameraGUI/allPictures/LiveFeed.png',
        resize = (500,500) )
    #print("Image Captured\n")
    camera.close()
    
#Updated screenshot capture function to accomodate live feed
def takePic():
    global newDisplay
    
    #Since we can't have this function compete with the live feed for camera access,
    #we just repurpose the current live feed image as a snapshot
    """
    camera=PiCamera()
    camera.resolution = (1280,720)
    camera.capture(
        '/home/pi/Desktop/cameraGUI/allPictures/' + strftime('%Y-%m-%d_%H:%M') + '.png',
        resize = (300,300) )
    """
    imgnew = Image.open("/home/pi/Desktop/cameraGUI/allPictures/LiveFeed.png")
    imgnew = imgnew.resize((300, 300))
    imgnew = imgnew.save("/home/pi/Desktop/cameraGUI/allPictures/" + strftime('%Y-%m-%d_%H:%M') + ".png")
    
    newDisplay = ImageTk.PhotoImage(
        file='/home/pi/Desktop/cameraGUI/allPictures/' + strftime('%Y-%m-%d_%H:%M') + '.png')
    
    #camera.close()
    
    imageHolder.configure(image=newDisplay)
    imageTitle.configure(text="Picture Last Taken at " + strftime('%H:%M on %d %b %Y')) 

    #click Take Pics
def takePicOld():
    global newDisplay
    camera=PiCamera()
    camera.resolution = (1280,720)
    camera.capture(
        '/home/pi/Desktop/cameraGUI/allPictures/' + strftime('%Y-%m-%d_%H:%M') + '.png',
        resize = (300,300) )
    newDisplay = ImageTk.PhotoImage(
        file='/home/pi/Desktop/cameraGUI/allPictures/' + strftime('%Y-%m-%d_%H:%M') + '.png')
    camera.close()
    imageHolder.configure(image=newDisplay)
    imageTitle.configure(text="Picture Last Taken at " + strftime('%H:%M on %d %b %Y')) 

    #click Lights: ON button
def lightOn():
    statusLight.configure(activebackground="green",bg="green",text="ON")
    ser.write(b'L')
    
    #click Lights: OFF button
def lightOff():
    statusLight.configure(activebackground="red",bg="red", text="OFF")
    ser.write(b'l')
    
    #click Valves: OPEN button
def openValve():
    statusValve.configure(activebackground="green",bg='GREEN', text="OPEN")
    ser.write(b'V')
    
    #click Valves: CLOSE button
def closeValve():
    statusValve.configure(activebackground="red",bg='RED', text="CLOSED")
    ser.write(b'v')

    #ticcmd command handler
def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))

    #SPIN MOTOR
    #NOTE: Since motor-spinning isn't handled by a thread, the program freezes when we do it.
def spinMotorF_1_75():
    #Turns Stepper motor at 1130 pulses/second for 1.75 seconds (approx. quarter turn clockwise)
    openValve()
    sleep(0.25)
    ticcmd('--exit-safe-start', '--current', '175', '--max-accel', '210000', '--velocity', '11300000')
    sleep(1.75)
    ticcmd('--exit-safe-start', '--velocity', '0')
    sleep(0.25)
    closeValve()
    """
    if(flowUpdate):
        flowTotal += 8.0
        if(rCount == 1):
            flowTotal += 0.1
        if(rCount == 2):
            flowTotal += 0.1
        if(rCount == 4):
            flowTotal -= 0.3
        if(rCount == 5):
            flowTotal += 0.2
        if(rCount == 6):
            flowTotal -= 0.1
        rcount += 1
        if(rCount > 7):
            rCount = 0
        updateFlow()
    """

def spinMotorB():
    #Turns Stepper motor at 1130 pulses/second for 5 seconds (approx. quarter turn counterclockwise)
    openValve()
    sleep(0.25)
    ticcmd('--exit-safe-start', '--current', '175', '--max-accel', '210000', '--velocity', '-11300000')
    sleep(5)
    ticcmd('--exit-safe-start', '--velocity', '0')
    sleep(0.25)
    closeValve()

def spinMotorF_0_25():
    #Turns Stepper motor at 1130 pulses/second for 0.25 seconds (approx. quarter turn clockwise)
    openValve()
    sleep(0.25)
    ticcmd('--exit-safe-start', '--current', '175', '--max-accel', '210000', '--velocity', '11300000')
    sleep(0.25)
    ticcmd('--exit-safe-start', '--velocity', '0')
    sleep(0.25)
    closeValve()
    """
    if(flowUpdate):
        flowTotal += 1.2
        if(rCount == 1):
            flowTotal += 0.1
        if(rCount == 2):
            flowTotal += 0.1
        if(rCount == 4):
            flowTotal -= 0.3
        if(rCount == 5):
            flowTotal += 0.2
        if(rCount == 6):
            flowTotal -= 0.1
        rcount += 1
        if(rCount > 7):
            rCount = 0
        updateFlow()
    """

def spinMotorF_6_75():
    #Turns Stepper motor at 1130 pulses/second for 5 seconds (approx. quarter turn clockwise)
    openValve()
    sleep(0.25)
    ticcmd('--exit-safe-start', '--current', '175', '--max-accel', '210000', '--velocity', '11300000')
    sleep(6.75)
    ticcmd('--exit-safe-start', '--velocity', '0')
    sleep(0.25)
    closeValve()
        
    
    #Start Fan
def startFan():
    statusFan.configure(activebackground="green",bg='GREEN', text="ON")
    ser.write(b'F')
    
    #Stop Fan
def stopFan():
    statusFan.configure(activebackground="red",bg="RED", text="OFF")
    ser.write(b'f')

    #Update Sensor Readings
    #NOTE: Do not click update more than once every couple seconds
    #This can cause the readings to get scrambled
def updateSensor():
    #dataFrame.text = sensor_ser.read_until(size = 200)
    #Cover up previous output with blank
    dataFrame=Label(cameraGUI,
                font=(60),
                text="\t\t\t\n\t\t\t\n\t\t\t\n\t\t\t"
                ).place(x=810,y=0)
    #Reset sensor data backlog and wait to ensure sensor has time to send new data
    #Commenting this out when sensor isn't plugged in
    
    sensor_ser.reset_input_buffer()
    sleep(3)
    senTemp = str(sensor_ser.read_until(size = 50))
    senHum = str(sensor_ser.read_until(size = 50))
    senPres = str(sensor_ser.read_until(size = 50))
    senCO2 = str(sensor_ser.read_until(size = 50))
    dataFrame=Label(cameraGUI,
                font=(60),
                text=("Temperature [°C]        [" + senTemp[2:7] + "]\n" + "Humidity [%]\t    [" + senHum[2:7] + "]\n" + "Pressure [hPa]\t[" + senPres[2:9] + "]\n" + "CO2 [PPM]\t  [" + senCO2[2:8] + "]")
                ).place(x=810,y=0)
    
rCount = 0
flowTotal = 0.0
flowUpdate = False
def updateFlow():
    #dataFrame.text = sensor_ser.read_until(size = 200)
    #Cover up previous output with blank
    dataFrame=Label(cameraGUI,
                font=(60),
                text="\t\t\t"
                ).place(x=810,y=150)
    dataFrame=Label(cameraGUI,
                font=(60),
                text=("Total Volume [mL]\t    [" + str(flowTotal) +"]")
                ).place(x=810,y=150)

    #Start Fan
def onFlow():
    statusFlow.configure(activebackground="green",bg='GREEN', text="")
    flowUpdate = True
    
    #Stop Fan
def offFlow():
    statusFlow.configure(activebackground="red",bg="RED", text="")
    flowUpdate = False

"""
Initial Fill and/or daily fill function

def doFill():

    something like
    openValve()
    spinMotorF() [but somehow also read flow meter while motor spins, maybe add to the spin motor function]
    closeValve()
    make sure to properly set desired time we want the motor to spin
    still need to re-test flow meter

"""

#WIDGETS
    #entire frame
Frame=(cameraGUI)

#Video Test

"""
#NOT IN USE: Global variables for monitoring/controlling the state of the thread
global loop_var
loop_var = 1
global thread_dead
thread_dead = 0
"""



#Starts thread
t1 = videoClass()
t1.setDaemon(True)
t1.start()
#process = multiprocessing.Process(target=run)
#process.start()

    #still image frame
stillImage=ImageTk.PhotoImage(file="/home/pi/Desktop/cameraGUI/placeholder.gif")
imageHolder=Label(cameraGUI, image=stillImage)
imageHolder.place(x=505,y=0)
imageTitle=Label(cameraGUI, text="Camera Frame\n")
imageTitle.place(x=508,y=315)
picBrowse=Button(cameraGUI, text="See All Pictures", command=browseClicked)
picBrowse.place(x=650,y=345)
picTake=Button(cameraGUI, text="Take Picture", command=takePic)
picTake.place(x=505,y=345)

    #data frame
dataFrame=Label(cameraGUI,
                font=(60),
                text="Temperature [°C]        [     ]\nHumidity [%]\t    [     ]\nPressure [hPa]\t    [     ]\nCO2 [PPM]\t    [     ]"
                ).place(x=810,y=0)

#place(x=810,y=0)
updateDataFrame=Button(cameraGUI, text="UPDATE", command=updateSensor).place(x=810,y=100)
#dataFrame.pack()
updateDataFrame=Button(cameraGUI, text="ON", command=onFlow).place(x=900,y=180)
updateDataFrame=Button(cameraGUI, text="OFF", command=offFlow).place(x=950,y=180)
statusFlow=Button(cameraGUI,
                     text="",
                     relief=FLAT,
                     activebackground="red",
                     bg="RED")
statusFlow.place(x=1020,y=180)
#allReadButton

flowFrame=Label(cameraGUI,
                font=(60),
                text="Total Volume [mL]\t    [     ]"
                ).place(x=810,y=150)
updateFlowFrame=Button(cameraGUI, text="UPDATE", command=updateFlow).place(x=810,y=180)

    #switches frame
Label(cameraGUI, text="Lights").place(x=505,y=405)
switchLightOn=Button(cameraGUI, text="ON", command=lightOn).place(x=565,y=400)
switchLightOff=Button(cameraGUI, text="OFF", command=lightOff).place(x=630,y=400)
statusLight=Button(cameraGUI,
                     text="OFF",
                     relief=FLAT,
                     activebackground="red",
                     bg="RED")
statusLight.place(x=705,y=400)

    #valves frame
Label(cameraGUI, text="Valves").place(x=505,y=435)
switchValveOn=Button(cameraGUI, text="OPEN", command=openValve).place(x=565,y=430)
switchValveOff=Button(cameraGUI, text="CLOSE", command=closeValve).place(x=630,y=430)
statusValve=Button(cameraGUI,
                     text="CLOSED",
                     relief=FLAT,
                     activebackground="red",
                     bg="RED")
statusValve.place(x=705,y=430)

    #time frame
clockLabel=Label(cameraGUI, text = "TIME").place(x=505,y=475)
timeKeeper=Label(cameraGUI)
timeKeeper.place(x=555,y=475)
time()

lightClockLabel=Label(cameraGUI, text = "TIMED LIGHT:").place(x=805,y=475)
timeKeeperLight=Label(cameraGUI)
timeKeeperLight.place(x=905,y=475)
lightSwitchTime(0)

    #spin button :)
Label(cameraGUI, text="Spin").place(x=505,y=505)
switchSpinMotor=Button(cameraGUI, text="INITIAL", command=spinMotorF_6_75).place(x=565,y=500)
switchSpinMotor=Button(cameraGUI, text="DAILY", command=spinMotorF_1_75).place(x=645,y=500)
switchSpinMotor=Button(cameraGUI, text="PRECISE", command=spinMotorF_0_25).place(x=715,y=500)
switchSpinMotor=Button(cameraGUI, text="BACKWARD", command=spinMotorB).place(x=805,y=500)

    #fans
Label(cameraGUI, text="Fans").place(x=505,y=535)
switchFanOn=Button(cameraGUI, text="ON", command=startFan).place(x=565,y=530)
switchFanOff=Button(cameraGUI, text="OFF", command=stopFan).place(x=630,y=530)
statusFan=Button(cameraGUI,
                     text="OFF",
                     relief=FLAT,
                     activebackground="red",
                     bg="RED")
statusFan.place(x=705,y=530)

#Handles closing of the window so the thread doesn't last forever
#If the thread doesn't have the time to die, it causes the camera to stop working
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #Stop thread loop
        stop_thread = True
        t1.stop()
        t1.join(timeout=5)
        
        #Give thread 5 seconds to die
        #MAKE SURE THIS TIME IS LARGER THAN THE TIME INTERVAL BETWEEN LIVE IMAGE CAPTURES
        #sleep(5)
        
        #Note: it seens like the camera can still occasioanlly crash even with this
        #safeguard for killing the thread in place. If the camera seems to randomly
        #stop working, restart the Pi.
        
        #Close window & serial connection
        ser.close()
        cameraGUI.destroy()

#Handles window-closing event so thread has time to die
cameraGUI.protocol("WM_DELETE_WINDOW", on_closing)

#initialize the window
cameraGUI.mainloop()