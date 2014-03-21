import serial
import time

port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=2.0,bytesize=8,stopbits=1)
port.flushInput()
port.flushOutput()
time.sleep(2)
port.write("ATZ\r")
time.sleep(2)
re=port.read(10)
print ("DATA"+re)
f = open("obd1.txt","w")

def flush():
    port.flushInput()
    port.flushOutput()

def one(rcv):
    r=rcv.split('\r',1)
    v=r[1]
    v=v[6:-3]
    vspeed=int(v,16)   
    return vspeed
    
def two(rcv):
    r=rcv.split('\r',1)
    v=r[1]
    v=v[6:-3]
    a=int(v[0:2],16)
    b=int(v[2:4],16)
    return {'A':a,'B':b}
    
def speed():
    flush()
    port.write("010D\r")
    rcv = port.readline()
    #f.write("\n"+repr(r))
    vspeed = one(rcv)
    f.write("\nVehicle Speed: " + repr(vspeed)+"Km/H.")
    
def rpm():
    flush()
    port.write("0103\r")
    rcv = port.readline()
    #f.write("\n"+ repr(rcv))
    rpm=two(rcv)
    a=rpm['A']; b=rpm['B']
    r=(a*256+b)/4   
    f.write("\nEngine RPM:" + repr(r) +"rpm.")
    
    #f.write a
    #f.write b
    
def cooltemp():
    flush()
    port.write("015C\r")
    rcv = port.readline()
    tmp=one(rcv)
    t=tmp-40
    f.write("\nEngine Coolant Temp.:" + repr(t)+" degree Celsius.")
    

def intaketemp():
    flush()
    port.write("010F\r")
    rcv = port.readline()
    tmp = one(rcv)
    tmp = tmp - 40
    f.write("\nIntake Air Temp: "+repr(tmp)+" degree Celsius.")
 
def throttle():
    flush()
    port.write("0111\r")
    rcv = port.readline()
    thr=one(rcv)
    thr=thr*100/255
    f.write("\nThrottle position:"+repr(thr)+" %.")
     
def runtime():
    flush()
    port.write("010F\r")
    rcv = port.readline()
    rt=two(rcv)
    a=rt['A']; b=rt['B']
    time = a*256 + b
    f.write("Run Time since Engine start: "+repr(time)+" seconds")

def engineload():
    flush()
    port.write("0104\r")
    rcv = port.readline()
    lv=one(rcv)
    elv=lv*100/255
    f.write("Calculated Engine Load Value: "+repr(elv)+" %")

def distance(): #Distance travelled since codes cleared
    flush()
    port.write("0131\r")
    rcv=port.readline()
    dis=two(rcv)
    a=dis['A']; b=dis['B']
    dt=a*256 + b
    f.write("Distance travelled since codes cleared: "+repr(dt)+" Km" )

def ambient():
    flush()
    port.write("0146\r")
    rcv = port.readline()
    a=one(rcv)
    a = a - 40
    f.write("Ambient Air Temp: "+repr(a)+" degree Celsius")
#Does not humidity and other parameters of the environment

def fuelrate():
    flush()
    port.write("015E\r")
    rcv=port.readline()
    v=two(rcv)
    a=v['A']; b=v['B']
    rate = (a*256+b)*(0.05)
    f.write("Engine Fuel Rate: "+repr(rate)+" L/h")

def battery():
    flush()
    port.write("015B\r")
    rcv = port.readline()
    v=one(rcv)
    time = v*100/255
    f.write("Hybrid battery remaining life: "+repr(time)+" %")

def shortterm():
    flush()
    port.write("0106\r")
    rcv = port.readline()
    st = one(rcv)
    st = ((st-128)/128)*100
    f.write ("Short term fuel bank: "+repr(st)+" %")

def longterm():
    flush()
    port.write("0108\r")
    rcv = port.readline()
    lt = one(rcv)
    lt = ((lt-128)/128)*100
    f.write ("Long term fuel bank: "+repr(lt)+" %")

def fuellevel():
    flush()
    port.write("012F\r")
    rcv = port.readline()
    fl = one(rcv)
    fl = fl*100/255
    f.write("Fuel level input: "+repr(fl)+" %")

while True:
    speed()
    rpm()
    cooltemp()
    intaketemp()
    throttle()
  #  runtime()
    engineload()
    distance()
    ambient()
#    fuelrate()
    battery()
#    fueleconomy()
    shortterm()
    longterm()
    fuellevel()

"""    f.write("\nFuel Level:" + repr(rcv))
    port.flushOutput()
    port.flushInput()
    port.write("010F\r")
    time.sleep(2)
    rcv = port.readline()
    f.write("\nRun time since engine start:"+repr(rcv))
    port.flushOutput()
    port.flushInput()
    port.write("0146\r")
    time.sleep(2)
    rcv = port.readline()
    f.write("\nAmnient Air temp:"+repr(rcv))
def fueleconomy():
    flush()
    port.write("010D\r")
    rcv = port.readline()
    vspeed = one(rcv)
    flush()
    port.write("0110\r")
    rcv = port.readline()
    f=two(rcv)
    a = f['A']; b = f['B']
    maf = (a*256 + b)/100
    mpg = (7.107*vspeed)/maf
    f.write ("Instantaneous fuel economy is: "+repr(mpg)+" MPG")



"""   

