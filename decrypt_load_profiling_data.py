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

"""
Fetching Data: The code defines a function fetch_data() which interacts with a database (presumably Supabase) to retrieve data from the "load_profiling_data" table. The fetched data is stored in the data variable.

Headers and Filename: The code defines a list of headers which represent the column names for the CSV file. The variable filename holds the desired name of the output CSV file ("load_profiling_data.csv").

File Creation and Writing: Using the with statement, the code opens the CSV file named "load_profiling_data.csv" in write mode. It creates a CSV writer and writes the column headers (headers of the CSV table) as the first row in the file.

Processing and Writing Data: For each row of data fetched from the database:

A row list is initialized to hold the values for each column.
The data is iterated through, and if a column's key is in the decrypt list, its value is directly added to the row list. Otherwise, the value is decrypted (presumably using a decrypt_Text() function).
The processed row list is written as a new row in the CSV file.
"""


def fetch_data():
    table_name = "load_profiling_data"
    query = supabase.table(table_name=table_name).select("*").execute()
    return query.data


data = fetch_data()

headers = [
    "id",
    "created_at",
    "load_type",
    "volt",
    "frequency",
    "power_factor",
    "current",
    "power",
    "energy",
]
filename = "load_profiling_data.csv"
decrypt = ["id", "created_at", "load_type"]
with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    for each in data:
        row = []
        for key, values in each.items():
            if key in decrypt:
                row.append(values)
            else:
                new_val = decrypt_Text(str(values))
                row.append(new_val)
        writer.writerow(row)
