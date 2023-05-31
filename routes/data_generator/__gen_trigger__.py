import time

from flask import session
from __trade_history__ import generate_Dummy_Trade_History
from __electricity_data__ import generate_Dummy_Electricity_Data
from __room_data__ import generate_Dummy_Room_Data
import sys
sys.path.append("..")

from utility.insert_Data import insert_Many_Into_Consumer_Dashboard, insert_Many_Into_Consumer_History, insert_Many_into_Consumer_Monitor



def gen_and_insert(user_id):
    while True:
        Histroy_Data = []
        Electricity_Data = []
        Room_Data = []

        val = 5

        while (val > 0):
            name, email, energy_trade = generate_Dummy_Trade_History()
            Histroy_Data.append({
                "user_id": user_id,
                "full_name": name,
                "email": email,
                "wh/hour_price": energy_trade
            })
            time.sleep(2)

            trades, energy_electricity, cost, other, grants, rejected = generate_Dummy_Electricity_Data()
            Electricity_Data.append({
                    "total_trades" :trades,
                    "average_wh/hour": energy_electricity,
                    "average_cost/hour": cost,
                    "some_other_stats": other,
                    "access_grants": grants,
                    "access_rejected": rejected,
                    "user_id": user_id
                    })
            time.sleep(2)

            lis = generate_Dummy_Room_Data(user_id)
            Room_Data.extend(lis)
            time.sleep(2)

            val -= 1

        insert_Many_Into_Consumer_Dashboard(Electricity_Data)
        insert_Many_Into_Consumer_History(Histroy_Data)
        insert_Many_into_Consumer_Monitor(Room_Data)
        
        Electricity_Data.clear()
        Histroy_Data.clear()
        Room_Data.clear()

gen_and_insert('19353ea3-5608-4971-b168-cccf5a9324a7')