import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


try:
    response = supabase.table('users').select("*").execute()
    print(len(response.data))
    if len(response.data) == 0:
        data, count = supabase.table('users').insert({"username": "tony", "email": "tony0light@gmail.com"}).execute()
        print(f"trying to create user {data}")
except Exception as e:   
    print(e)

