OBD
===

In this repository, I have added two files namely - obd.py and file.py which aims to fetch real time data from the car such as Vehicle Speed, Engine Rpm etc. using their standard OBD-II PIDs.

Hardware used - OBD II UART Board, Raspberry Pi, OBD to DB9 cable, Laptop.
Software Libraries - pyserial library written in python (which encapsulates all the code required to transfer the data through a serial port).

After connecting the required hardware to Raspberry Pie, now you have to enter the serial port no (for ex - /dev/USB0) in your obd.py file.
You can check the serial port no by typing the following command in terminal - "dmesg | grep tty".

Finally you have to run the python file by writing "python filename" in the terminal. obd.py will print the output to the terminal whereas file.py will store the output to a specified file.
