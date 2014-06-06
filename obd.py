#Developed and Maintained By Sarthak Jain
#IF you find any bugs, mail to - sarthak.7386@gmail.com
import serial
import time

port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.025,bytesize=8,stopbits=1)

def flush():
    port.flushInput()
    port.flushOutput()
    
flush()
flush()

port.write("ATDP\r")
rcv = port.readline()
print("Supported OBD II Protocol is "+repr(rcv))

def one(rcv): # Calculating the decimal value of 1 byte hexadecimal numbers
    r=rcv.split('\r',1)
    v=r[1]
    print("\n"+v)
    v=v[6:-3] # A substring from index 6 to -3 including both - Python indexing start from 0
    vspeed=int(v,16)   
    return vspeed
    
def two(rcv): #Calculating the decimal value of 2 bytes hexadecimal numbers
    r=rcv.split('\r',1)
    v=r[1]
    #bol = pid_supported(v)
    #if bol != 'false'
    v=v[6:-3]
    a=int(v[0:2],16)
    b=int(v[3:5],16)
    return {'A':a,'B':b}
    
def speed():
    flush()
    port.write("010D\r")
    rcv = port.readline()
    #print("\n"+repr(r))
    vspeed = one(rcv)
    print("\nVehicle Speed: " + repr(rcv)+"Km/H.")
    return vspeed
    
def rpm():
    flush()
    port.write("010C\r")
    rcv = port.readline()
    print("\n"+ repr(rcv))
    r=two(rcv)
    a=r['A']; b=r['B']
    rpm=(a*256+b)/4   
    print("\nEngine RPM:" + repr(rpm) +"rpm.")
    return rpm    
    #print a
    #print b
    
def cooltemp():
    flush()
    port.write("015C\r")
    rcv = port.readline()
    tmp=one(rcv)
    t=tmp-40
    print("\nEngine Coolant Temp.:" + repr(t)+" degree Celsius.")
    

def intaketemp():
    flush()
    port.write("010F\r")
    rcv = port.readline()
    tmp = one(rcv)
    tmp = tmp - 40
    print("\nIntake Air Temp: "+repr(tmp)+" degree Celsius.")
 
def throttle():
    flush()
    port.write("0111\r")
    rcv = port.readline()
    thr=one(rcv)
    thr=thr*100/255
    print("\nThrottle position:"+repr(thr)+" %.")
     
def runtime():
    flush()
    port.write("010F\r")
    rcv = port.readline()
    rt=two(rcv)
    a=rt['A']; b=rt['B']
    time = a*256 + b
    print("\nRun Time since Engine start: "+repr(time)+" seconds")

def engineload():
    flush()
    port.write("0104\r")
    rcv = port.readline()
    lv=one(rcv)
    elv=lv*100/255
    print("\nCalculated Engine Load Value: "+repr(elv)+" %")

def distance(): #Distance travelled since codes cleared
    flush()
    port.write("0131\r")
    rcv=port.readline()
    dis=two(rcv)
    a=dis['A']; b=dis['B']
    dt=a*256 + b
    print("\nDistance travelled since codes cleared: "+repr(dt)+" Km" )

def ambient():
    flush()
    port.write("0146\r")
    rcv = port.readline()
    a=one(rcv)
    a = a - 40
    print("\nAmbient Air Temp: "+repr(a)+" degree Celsius")
#Does not humidity and other parameters of the environment

def fuelrate():
    flush()
    port.write("015E\r")
    rcv=port.readline()
    v=two(rcv)
    a=v['A']; b=v['B']
    rate = (a*256+b)*(0.05)
    print("\nEngine Fuel Rate: "+repr(rate)+" L/h")

def battery():
    flush()
    port.write("015B\r")
    rcv = port.readline()
    v=one(rcv)
    time = v*100/255
    print("\nHybrid battery remaining life: "+repr(time)+" %")

def fueleconomy():# maf sensor supported
    flush()
    vspeed = speed()
    flush()
    port.write("0110\r")
    rcv = port.readline()
    f=two(rcv)
    a = f['A']; b = f['B']
    maf = (a*256 + b)/100
    mpg = (7.107*vspeed)/maf
    print ("\nInstantaneous fuel economy is: "+repr(mpg)+" MPG")

def fuel_economy():
    flush()
    port.write("010B\r")
    rcv = port.readline()
    imap = one(rcv)
    maf = (imap/120)*(0.85)*4*(28.97)/(8.314)
    print maf
    vspeed = speed()
    mpg = (7.107*vspeed)/maf    
    print ("\nInstantaneous fuel economy is:"+repr(mpg)+" MPG")
    
def shortterm():
    flush()
    port.write("0106\r")
    rcv = port.readline()
    st = one(rcv)
    st = ((st-128)/128)*100
    print ("\nShort term fuel bank: "+repr(st)+" %")

def longterm():
    flush()
    port.write("0108\r")
    rcv = port.readline()
    lt = one(rcv)
    lt = ((lt-128)/128)*100
    print ("\nLong term fuel bank: "+repr(lt)+" %")

def fuel_consum():
    flush()
    rp = rpm()
    th = throttle()

    
while True:
    speed()
#    rpm()
    cooltemp()
    intaketemp()
    throttle()
#    runtime()
    engineload()
#    distance()
    ambient()
#    fuelrate()
    battery()
   # fueleconomy()
#    fuel_economy()
    shortterm()
    longterm()
    print("\n\n")

