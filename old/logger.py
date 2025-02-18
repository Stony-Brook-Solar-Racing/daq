from threading import Event, Thread
import time
import glob
from serial import Serial, SerialException
from voltage_reader import VoltageReader
import sys 

reading_thread = None
BAUDRATE = 9600
TIMEOUT = 1.5
MEASUREMENTS = 2


class Logger:
    
    app_root = None

    def __setup_arduino(self):
        if sys.platform == 'linux':
            ports = glob.glob('/dev/ttyACM*')
        elif sys.platform.startswith('win'):
            ports = [f'COM{i}' for i in range(10)]
        else:
            raise Exception('Platform not supported')
        
        # try all ports on platform
        for port in ports:
            try:
                self.arduino = Serial(port=port, baudrate=BAUDRATE, timeout=TIMEOUT)
            except (OSError, SerialException):
                pass
        
        if self.arduino == None:
            raise Exception('Arduino not found')

    def __init__(self):
        self.stop_event = Event()

        # setup arduino
        self.__setup_arduino()
        # setup the VoltageReader and start a thread that reads
        # and updates measurements
        v_data = VoltageReader(self.arduino, MEASUREMENTS, app=None)
        Logger.reading_thread = Thread(target=v_data.read_voltages)
        Logger.reading_thread.start()
    
    def stop_handler(self):
        # print(s, t)
        print('Stopping reads...')
        self.stop_event.set()
        VoltageReader.stop_reading.set()
        Logger.reading_thread.join()
        # Logger.app_root.destroy()
        
    # def setup(self):

        # defines DISPLAY variable for tkinter if needed
        # if os.environ.get('DISPLAY','') == '':
        #     print('no display found. Using :0.0')
        #     os.environ.__setitem__('DISPLAY', ':0.0')
        
        # Logger.app_root = tk.Tk()
        # app = DisplayApp(Logger.app_root, 3)
        
        

if __name__ == '__main__':
    logger = Logger()
    logger.setup()

    # keeps the program running without polling
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logger.stop_handler()
