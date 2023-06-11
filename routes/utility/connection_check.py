import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

supabase_: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)

table_name = 'private_data'
row = {
    'user_id': '',
    'private_key': user_private_key_hex,
}
print(supabase_.table(table_name=table_name).select('*').execute())