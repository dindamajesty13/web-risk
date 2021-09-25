from lib.database import db_connect


def getThreat():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM public.threat ORDER BY id_threat ASC")
        data = cur.fetchall()
        return data

def getCountThreat():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(id_threat) FROM public.threat")
        data = cur.fetchall()
        return data

def insertThreat(id_threat, threat_type, threat_weight):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO public.threat (id_threat, threat_type, threat_weight) VALUES ('{id_threat}', '{threat_type}', '{threat_weight}')")
    return True


def updateThreat(id_threat, threat_type, threat_weight):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE public.threat SET threat_type='{threat_type}', threat_weight='{threat_weight}' WHERE public.threat.id_threat='{id_threat}'")
    return True


def deleteThreat(id_threat):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM public.threat WHERE public.threat.id_threat='{id_threat}'")
    return True
