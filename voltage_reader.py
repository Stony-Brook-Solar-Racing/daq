from serial import Serial
from time import sleep

class VoltageReader:

    def __init__(self, arduino: Serial, db):
        self.arduino = arduino
        
    def read_voltages(self):
        arduino = self.arduino
        arduino.reset_output_buffer()
        arduino.reset_input_buffer()

        while True:
            data = arduino.readline()
            voltage = data.decode().strip().split()
            if len(voltage) > 0:
                print(f"v1: {voltage[0]}, v2: {voltage[1]}, diff: {voltage[2]}") 

        print("Exitted")
