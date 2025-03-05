from serial import Serial
from time import sleep

from database import Database

class VoltageReader:

    def __init__(self, arduino: Serial, db: Database):
        self.arduino = arduino
        self.db = db
        
    def read_voltages(self):
        arduino = self.arduino
        arduino.reset_output_buffer()
        arduino.reset_input_buffer()

        db = self.db

        while True:
            data = arduino.readline()
            voltage = data.decode().strip().split()
            if len(voltage) > 0:
                print(f"v1: {voltage[0]}, v2: {voltage[1]}, diff: {voltage[2]}\n") 
                db.add_voltage(pre_shunt=float(voltage[0]), post_shunt=float(voltage[1]))

        print("Exitted")
