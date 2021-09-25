from lib.database import db_connect

def getAdmin(username, password):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM public.admin WHERE username='{username}' and password='{password}'")
        data = cur.fetchone()
        return data