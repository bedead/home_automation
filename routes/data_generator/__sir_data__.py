import random
import time
import csv

def generate_Dummy_Room_Data():
    # all loads
    loads = ['Load 1', 'Load 2','Load 3','Load 4','Green Load', 'GTI','Invertor','Grid']

    data = []
    current_total = 0
    power_total = 0
    for a in loads:
        load_type = str(a)
        # Generate random energy consumption per hour for a room
        v = random.randint(225, 235)
        f = random.randint(45, 55)
        pf = round(random.uniform(0.85, 0.95), 1)
        i = random.randint(1,4)
        p = round(v*i*pf, 1)

        current_total += i
        power_total += p

        data.append([
            load_type,v,f,pf,i,p, round(current_total, 1),round(power_total,1),
        ])

    return data

def dump_Data_To_CSV(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

filename = 'dummy_data.csv'
val = 5
Room_Data = []

while (val >= 0):
    lis = generate_Dummy_Room_Data()
    Room_Data.append(['load_type','volt','frequency','power_factor','current','power','current_total','power_total'])
    Room_Data.extend(lis)

    val -= 1
dump_Data_To_CSV(Room_Data, filename)
print(Room_Data)
print("CSV file generated in local directory")