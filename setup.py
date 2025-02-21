from glob import glob
from serial import Serial, SerialException
import sys
import logging

from Volatage_reader import VoltageReader
# Constants
BAUDRATE = 9600

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
        except(OSError, SerialException):
            return 0;
