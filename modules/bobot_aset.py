from lib.database import db_connect

def getBobotAssets():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT id_app, criteria_1, criteria_2, criteria_3, ((public.bobot_aset.criteria_1*0.3) + (public.bobot_aset.criteria_2*0.4) + (public.bobot_aset.criteria_3*0.3)) as result_assessment FROM public.bobot_aset WHERE email = 'user@gmail.com' ORDER BY id_app ASC")
        data = cur.fetchall()
        return data

def getCountData(email):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"select count(email) from public.bobot_aset where email = '{email}'")
        data = cur.fetchall()
        return data

def getCountAsset():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"select count(id_app) from public.list_asset")
        data = cur.fetchall()
        return data

def insertBobotAsset(email, id_app, criteria_1, criteria_2, criteria_3):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO public.bobot_aset (email, id_app, criteria_1, criteria_2, criteria_3) VALUES ('{email}','{id_app}', '{criteria_1}', '{criteria_2}', '{criteria_3}')")
    return True

def updateBobotAsset(email, id_app, criteria_1, criteria_2, criteria_3):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE public.bobot_aset SET criteria_1='{criteria_1}', criteria_2='{criteria_2}', criteria_3='{criteria_3}' WHERE public.bobot_aset.id_app='{id_app}' AND public.bobot_aset.email='{email}'")
    return True

def deleteBobotAsset(id_app, email):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM public.bobot_aset WHERE public.bobot_aset.id_app='{id_app}' AND public.bobot_aset.email='{email}'")
    return True
