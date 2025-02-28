from glob import glob
from serial import Serial, SerialException
import sys
import logging

from Volatage_reader import VoltageReader
# Constants
BAUDRATE = 9600

logging.basicConfig(
    filename="/var/log/daq/daq.log",
    filemode='w+',
    level=logging.INFO
)

class Setup:
    def __setup_arduino(self):
        if sys.platform == "linux":
            ports = glob("/dev/ttyASM*")
        elif sys.platform.startswith('win'):
            ports = [f"COM{i}" for i in range(10)]
        else:
           raise Exception("Platform not supported")

        for port in ports:
            try:
                self.arduino = Serial(port=port, baudrate=BAUDRATE, timeout=TIMEOUT)
            except(OSError, SerialException) as err:
                logging.error(err)
        
        if self.arduino == None:


    def __init__(self):

        



