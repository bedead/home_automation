import os
from supabase import create_client, Client
from dotenv import load_dotenv
import csv
import os

from routes.data_generator.triple_des import decrypt_Text

load_dotenv()


SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
    # print(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


def fetch_data():
    table_name = 'load_profiling_data'
    query = supabase.table(table_name=table_name).select('*').execute()
    return query.data

data = fetch_data()

headers = ['id','created_at','load_type','volt','frequency','power_factor','current','power','energy']
filename = 'load_profiling_data.csv'
decrypt = ['id','created_at','load_type']
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    for each in data:
        row = []
        for key, values in each.items():
            if (key in decrypt):
                row.append(values)
            else:
                new_val = decrypt_Text(str(values))
                row.append(new_val)
        writer.writerow(row)
        