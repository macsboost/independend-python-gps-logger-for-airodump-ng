#! /usr/bin/python

# This script is based on GPS Python example Written by Dan Mandle http://dan.mandle.me September 2012
# The main pourpouse of my modification, is to Log GPS position info flat file
# later to be used to track the position of Wifi Client devices like Phones and Laptops
# compared against Airodump CSV file output.
# -This script only captures the GPS data, and is not processing any Airodump output.
# T.D. http://www.dobrotka.sk, 17.1.2015
# https://github.com/ggtd/independend-python-gps-logger-for-airodump-ng

# -----------------Original credits ------------
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

#further modified for megr3241 by Mac McAlpine for the raspberry pi GPS logger project
#11-11-2019
  
import os
from gps import *
from time import *
import time
import threading
import datetime
import math
from time import gmtime, strftime
import setgps10hz

setgps10hz.main()
print("starting GPSD")
os.system("gpsd /dev/ttyACM0")
 
gpsd = None #seting the global variable

time1= None
time2= "placeholder string"

os.system('clear') #clear the terminal (optional)

localtime = time.localtime(time.time())
filename = "./megr3241log-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".csv"
flog = open(filename, 'a')
#flog = open('./gps_log_file', 'a')
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up

    log_string = "TIME,Latitude,Longitude,Altitude,Speed,Heading,Mode\n"
    flog.write(log_string)
    flog.flush()

    while True:
      time1=str(gpsd.fix.time)

      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc

      os.system('clear')

      print
      print ' MEGR3241 10hz GPS Logger'
      print '----------------------------------------'
      print 'latitude      ' , gpsd.fix.latitude
      print 'longitude     ' , gpsd.fix.longitude
      print 'GPS time utc  ' , gpsd.utc
      print '(device) Time:', time1
      print 'GPS Vel(mph)  ' , gpsd.fix.speed*0.621


      if (time1+"" != time2+""): # Check if Second tick changed, if yes, log positon
        time2=str(gpsd.fix.time)
        if (not math.isnan(gpsd.fix.speed)):
          print "Log time!"
          log_string = str(time1)
          #log_string = log_string + "," + str(gpsd.utc)
          #log_string = log_string + "," + str(gpsd.fix.time) 
          log_string = log_string + "," + str(gpsd.fix.latitude) + "," + str(gpsd.fix.longitude)
          log_string = log_string + "," + str(gpsd.fix.altitude*3.28084) + "," + str(gpsd.fix.speed*0.621) + "," + str(gpsd.fix.track) + str(gpsd.fix.mode)
          log_string = log_string + "\n"
          flog.write(log_string)
          flog.flush()
    
    time.sleep(0.075)

 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
  
