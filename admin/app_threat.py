from lib.database import db_connect


def getAppThreat():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM public.app_threat ORDER BY id_app ASC")
        data = cur.fetchall()
        return data

def insertAppThreat(id_app, id_threat):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO public.app_threat (id_app, id_threat) VALUES ('{id_app}', '{id_threat}')")
    return True


def updateAppThreat(id_app, id_threat):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE public.app_threat SET id_threat='{id_threat}' WHERE public.app_threat.id_app='{id_app}')")
    return True


def deleteAppThreat(id_app):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM public.app_threat WHERE public.app_threat.id_app='{id_app}'")
    return True
