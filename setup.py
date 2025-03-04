from glob import glob
from serial import Serial, SerialException
import sys
import logging

from voltage_reader import VoltageReader
# Constants
BAUDRATE = 9600
"""
logging.basicConfig(
    filename="/var/log/daq/daq.log",
    filemode='w+',
    level=logging.INFO
)
"""
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
            print("Arduino not found\n")
            print("Retrying in 5 seconds...")
            sleep(5)
            self.__setup_arduino

    def __setup_db(self):
        db = ''

    def __init__(self):
        self.__setup_db()
        self.__setup_arduino()
        print("Got here")
        voltage_reader = VoltageReader(self.arduino, db)
        logging.info("Starting voltage reader")
        voltage_reader.read_voltages()
