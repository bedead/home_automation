import ast
import csv
import time
import random
import os
from datetime import datetime
# from pymongo import MongoClient
import psutil
import schedule
from routes.data_generator.triple_des import encrypt_Text
from routes.utility.insert_Data import insert_Many_into_Consumer_Monitor

def import_data():
    print("Importing data from local csv file to the supabase cloud")
    for i in range(0,4):
        print('.', end='')
    # Open CSV file and read rows into a list of dictionaries
    with open('data.csv', 'r') as csvfile:
        
        data_lines = csv.reader(csvfile)

        new_data = []
        count = 0
        for line in data_lines:
            for each_dict in line:
                d = ast.literal_eval(each_dict)
                # di = json.loads(each_dict)
                new_data.append(d)
            print(new_data)
            insert_Many_into_Consumer_Monitor(data=new_data, type='consumer')        
            new_data.clear()


        # Print number of inserted documents
        print("Inserted {} documents into the supabase".format(count))

    # Write log message and flush to disk
    log_file.write("Data imported to supabase database db...\n")
    log_file.flush()

# Clear the data file after successful import
    open('data.csv', 'w').close()


# Function to generate data
def generate_data(user_id):
        try:
            while True:
                # Generate random timestamp between 2021-01-01 and 2023-12-31
                # all rooms
                loads = ['Load 1', 'Load 2','Load 3','Load 4','Green Load', 'GTI','Invertor','Grid']

                data = []
                current_total = 0
                power_total = 0
                for a in loads:
                    cipher_load_type = encrypt_Text(str(a))
                    # Generate random energy consumption per hour for a room
                    v = random.randint(225, 235)
                    f = random.randint(45, 55)
                    pf = round(random.uniform(0.85, 0.95), 1)
                    i = random.randint(1,4)
                    p = round(v*i*pf, 1)

                    current_total += i
                    power_total += p

                    # encryption of values
                    cipher_v = encrypt_Text(str(v)); cipher_f = encrypt_Text(str(f))
                    cipher_pf = encrypt_Text(str(pf)); cipher_i = encrypt_Text(str(i))
                    cipher_p = encrypt_Text(str(p)); cipher_current_total = encrypt_Text(str(round(current_total, 1)))
                    cipher_power_total = encrypt_Text(str(round(power_total, 1)))

                    data.append({
                        "load_type": cipher_load_type,
                        "volt": cipher_v,
                        "frequency": cipher_f,
                        "power_factor": cipher_pf,
                        "current": cipher_i,
                        "power": cipher_p,
                        "current_total": cipher_current_total,
                        "power_total": cipher_power_total,
                        "user_id": user_id
                    })
                    # Print the data
                    # print(f"Room: {current_room}, Energy: {a_energy_consumption} wh/hour, Temp: {a_temp} C")

                # return data
                # for each_ in data:
                csv_writer.writerow(data)
                data_file.flush() # Ensure data is written to file
                print(f'Data generated: {data}')
                time.sleep(1) # Wait for 1 second
        except KeyboardInterrupt as e:
            print('Data generation interrupted by user')


# Function to check storage status and trigger data import if full
def check_storage():
    disk_usage = psutil.disk_usage("/")
    if disk_usage.percent >= 90:
    # Storage is full, trigger data import
        import_data()


# Function to check storage of the data file
def check_data_file_storage():
    file_size = os.path.getsize("data.csv") 
    # Get the size of the data file in bytes
    if file_size >= 1e9: # 1e9 bytes = 1GB
    # Data file is too large, trigger data import
        import_data()
# Schedule storage check and data import every 5 minutes

# Set up CSV writer
data_file = open('data.csv', 'w', newline='')
csv_writer = csv.writer(data_file)
# Set up log file
log_file = open("log.txt", "a")
log_file.write("Program started at {}\n".format(datetime.now()))
log_file.flush() # Flush the write operation to the log file

schedule.every(5).minutes.do(check_storage)
schedule.every(5).minutes.do(check_data_file_storage)
# Generate data
generate_data('1a06b542-5f57-445e-b544-3b17c482d87a')
# Run the scheduler
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print('Program interrupted by user')
    # Import data before exiting the program
    import_data()


# Close the CSV file
data_file.close()

# Close the log file
log_file.write("Program ended at {}\n".format(datetime.now()))
log_file.close()
