## GPS logger tool for UNCC MEGR3241 Advanced Motorsports Instrumentation.
Mac McAlpine
111 Motorsports Research, UNC Charlotte USA

This Python script is logging 10hz of GPS position from GPSD. Later to be used with megalog viewer to determine performance metrics.
m8n ublox gps units are sent the magic packets to enable 10hz output.

###Usage:
Simply run sudo python gpslog2.py to start recording

Press control C to stop. You may need to hold the keys down.

The logfile is writen into ./megr3241-x-x-x-x.csv

Copy the file to a USB drive and analyze the data with a PC using megalogviewer.

Log file is a CSV file. The first line has the header.

Have fun!


