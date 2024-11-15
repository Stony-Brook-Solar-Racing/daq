import csv
import os
import time
from datetime import datetime

class Recording:

    def __init__(self, cols) -> None:
        # remove newline when deployed
        # os.path.dirname(os.path.abspath(__file__))
        # dir_path = os.path.dirname(os.path.abspath(__file__))

        if not os.path.exists('./logs'):
            os.mkdir('./logs')
        
        formatted_time = datetime.now().strftime('%m-$d-%Y-%H-%M-%S')

        self.csv = open(f'./logs/{formatted_time}-readings.csv', mode='x', newline='')
        self.csv_writer = csv.writer(self.csv)
        self.cols = cols
        self.setup_csv()
    
    def setup_csv(self):

        header = ['Time']

        for i in range(self.cols):
            header.append(f'Voltage{i+1}')
        self.csv_writer.writerow(header)

    def write_data(self, data):
        row = [time.time()]
        for d in data:
            row.append(d)
            
        # Flushes data out to file immediately
        self.csv_writer.writerow(row)
        self.csv.flush()
        os.fsync(self.csv)

    def close(self):
        self.csv.close()
        print('Closed csv.')
