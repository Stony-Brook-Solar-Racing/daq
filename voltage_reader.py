class VoltageReader:

    def __init__(arduino: Serial, db: db):
        self.arduino = arduino
        
    def read_voltages(self):
        arduino.reset_output_buffer()
        arduino.reset_input_buffer()

        while true:
            sleep(1)
            arduino = self.arduino
            data = arduino.readline()
            voltage = data.decode().strip().split()
            print(voltage)

        print("Exitted")
