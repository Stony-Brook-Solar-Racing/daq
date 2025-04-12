from serial import Serial
from time import sleep

from database import Database
from daq_redis import DAQRedis

class VoltageReader:

    def __init__(self, arduino: Serial, db: Database, redis: DAQRedis):
        self.arduino = arduino
        self.db = db
        self.redis = redis
        
    def read_voltages(self) -> None:
        arduino = self.arduino
        arduino.reset_output_buffer()
        arduino.reset_input_buffer()

        db = self.db
        redis = self.redis

        while True:
            data = arduino.readline()
            voltage = data.decode().strip().split()
            if len(voltage) > 0:
                print(f"v1: {voltage[0]}, v2: {voltage[1]}") # , diff: {voltage[2]}\n") 
                db.add_voltage(pre_shunt=float(voltage[0]), post_shunt=float(voltage[1]))
                ttd = self.calc_ttd(0, 0);
                battery = self.calc_battery(0, 34, 38)
                print(f"ttd: {ttd}, battery: {battery}")
                redis.set_value("ttd", ttd)
                redis.set_value("battery", battery)

        print("Exitted")

    def calc_ttd(self, capacity, curr) -> float:
        return capactiy/curr

    def calc_current(self, v1, v3, res) -> float:
        return ((v3-v1)/res)*1000

    def calc_battery(self, v, min_v, max_v) -> int:
        return int((max_v-v)/(max_v-min_v))
