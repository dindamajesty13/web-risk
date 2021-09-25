from lib.database import db_connect

def getUsers(username, password):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM public.users WHERE email='{username}' and password='{password}'")
        data = cur.fetchone()
        return data