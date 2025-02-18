# import time
import threading
# import pandas as pd
from serial import Serial
from record import Recording
from display import DisplayApp
from time import sleep
from logger import TIMEOUT

class Readings: 
    
    def __init__(self, adcs, app: DisplayApp) -> None:
        self.sema = threading.Semaphore()
        self.counter = 1
        # self.app = app
        # self.readings = pd.DataFrame()
        # df_index = pd.Index([i for i in range(plots)])

        # self.readings.set_index(df_index)
        # [timestamp, voltage]
        self.readings = [[0] for _ in range(adcs)]

        self.csv_record = Recording(adcs)
    
    def update_readings(self, filtered_data: list):
        # print('filtered:', filtered_data)
        self.sema.acquire()
        try: 
            self.csv_record.write_data(filtered_data)
            # self.app.update_measurements(filtered_data)
        
        except:
            print('Could not update readings')
            self.sema.release()
            # self.shutdown()
        
        self.sema.release()

    def shutdown(self):
        print('Stopping logging')
        self.csv_record.close()

    def use_readings(self, action, lines_data, axs):
        self.sema.acquire()
        action(self.readings, lines_data, axs)
        self.sema.release()
    
    def __str__(self):
        return str(self.readings)

class VoltageReader:

    stop_reading = threading.Event()

    def __init__(self, arduino: Serial, measurements, app: DisplayApp) -> None:
        self.counter = 0
        self.readings = Readings(measurements, app)
        self.arduino = arduino
        self.measurements = measurements
        # self.exp_cols = adcs * 2

    def line_filter(self, v):
        if v != '':
            return True
        return False

    # could set the serial to have no timeout
    def read_voltages(self):
        arduino = self.arduino

        # clear buffer
        sleep(TIMEOUT)
        arduino.reset_output_buffer()
        arduino.reset_input_buffer()

        while not VoltageReader.stop_reading.is_set(): 
            read_lines = []
            while (len(read_lines) < self.measurements):
                line = arduino.readline()
                read_lines.append(line)
            
            lines = [line.decode().strip() for line in read_lines]
            print(lines)            
            filtered_lines = [float(v) for v in filter(self.line_filter, lines)]

            if (len(filtered_lines) == self.measurements):
                self.readings.update_readings(filtered_lines)
            if VoltageReader.stop_reading.is_set():
                break

        self.readings.shutdown()
