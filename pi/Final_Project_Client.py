from bluedot.btcomm import BluetoothClient

import RPi.GPIO as GPIO
import time
from time import sleep

import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)

GPIO.output(2, GPIO.HIGH)
GPIO.output(3, GPIO.HIGH)
GPIO.output(22, GPIO.LOW)
GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
#GPIO.output(22, GPIO.HIGH)
#GPIO.output(23, GPIO.HIGH)
#GPIO.output(24, GPIO.HIGH)
def pzem():
    sensor = serial.Serial(
    #                       port='/dev/PZEM_sensor',
                            port='/dev/ttyUSB0',
                            baudrate=9600,
                            bytesize=8,
                            parity='N',
                            stopbits=1,
                            xonxoff=0
                            )

    master = modbus_rtu.RtuMaster(sensor)
    master.set_timeout(2.0)
    master.set_verbose(True)

    data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

    voltage = data[0] / 10.0 # [V]
    current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
    power = (data[3] + (data[4] << 16)) / 10.0 # [W]
    energy = data[5] + (data[6] << 16) # [Wh]
    frequency = data[7] / 10.0 # [Hz]
    powerFactor = data[8] / 100.0
    alarm = data[9] # 0 = no alarm
    localtime = time.asctime( time.localtime(time.time()) )
    n = localtime.split(' ')
    for i in n:
        if i == '':
            n.remove('')
            break
    localtime = ''
    for i in n:
        localtime += i + ' '
    pzem_data = str(power)+' '+localtime[:-1]+' '+str(round(time.time()))+' '
    
    try:
        master.close()
        if sensor.is_open:
            sensor.close()
    except:
        pass
    return pzem_data

def data_received(data):
    if data == 'g':
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
    elif data == 'y':
        GPIO.output(22, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.LOW)
    elif data == 'r':
        GPIO.output(22, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.HIGH)
    else: 
        print(data)

c = BluetoothClient("B8:27:EB:DC:1F:E6", data_received)

while(True):
    pzem_data = pzem()
    c.send(pzem_data)
    sleep(1)

while (True):
    pass


