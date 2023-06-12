import time

from flask import session
# from __trade_history__ import generate_Dummy_Trade_History
# from __electricity_data__ import generate_Dummy_Electricity_Data
from __room_data__ import generate_Dummy_Room_Data
import sys
sys.path.append("..")

from utility.insert_Data import insert_Many_Into_Consumer_Dashboard, insert_Many_Into_Consumer_History, insert_Many_into_Consumer_Monitor



def gen_and_insert(user_id, type):
    while True:
        # Histroy_Data = []
        # Electricity_Data = []
        Room_Data = []

        # val = 3

        # while (val > 0):
        # name, email, energy_trade = generate_Dummy_Trade_History()
        # Histroy_Data.append({
        #     "user_id": user_id,
        #     "full_name": name,
        #     "email": email,
        #     "wh_hour_price": energy_trade
        # })

        # trades, energy_electricity, cost, other, grants, rejected = generate_Dummy_Electricity_Data()
        # Electricity_Data.append({
        #         "total_trades" : trades,
        #         "average_wh_hour": energy_electricity,
        #         "average_cost_hour": cost,
        #         "some_other_stats": other,
        #         "access_grants": grants,
        #         "access_rejected": rejected,
        #         "user_id": user_id
        #         })

        lis = generate_Dummy_Room_Data(user_id)
        Room_Data.extend(lis)

        # val -= 1

        # insert_Many_Into_Consumer_Dashboard(Electricity_Data)
        # insert_Many_Into_Consumer_History(Histroy_Data)
        print(Room_Data)
        insert_Many_into_Consumer_Monitor(Room_Data, type)
        # print(Room_Data)
        
        # Electricity_Data.clear()
        # Histroy_Data.clear()
        Room_Data.clear()

        print("Post complete.")
        time.sleep(6)

# consumer
# gen_and_insert('1a06b542-5f57-445e-b544-3b17c482d87a', 'consumer')

# producer
gen_and_insert('48a6cc6b-93c7-4a31-b0c9-bef7b27675bb', 'producer')
