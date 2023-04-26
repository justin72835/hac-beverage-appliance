import csv
from datetime import datetime
import os
import time

def test(data):
    # create new directory to store csv files if 'temp_data' does not already exist
    dir_path = os.path.join(os.getcwd(), 'temp_data')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # create csv for current cycle temp data
    header = ['Time', 'Temperature (C)']
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H.%M.%S")
    file_path = os.path.join(dir_path, dt_string + '_data.csv')
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(data)

# arbitrary numbers, delay to make sure datetime changes between file creation
test([1, 2])
time.sleep(2)
test([3, 4])