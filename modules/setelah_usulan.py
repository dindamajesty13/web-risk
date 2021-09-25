from lib.database import db_connect

def getSetelahUsulan():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5, ((public.nilai_resiko_setelah_usulan.criteria_1*0.30) + (public.nilai_resiko_setelah_usulan.criteria_2*0.20) + (public.nilai_resiko_setelah_usulan.criteria_3*0.10) + (public.nilai_resiko_setelah_usulan.criteria_4*0.25) + (public.nilai_resiko_setelah_usulan.criteria_5*0.15)) as result_assessment FROM public.nilai_resiko_setelah_usulan WHERE email = 'user@gmail.com' ORDER BY id_app ASC")
        data = cur.fetchall()
        return data

def getCountSetelahUsulan(email):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"select count(email) from public.nilai_resiko_setelah_usulan where email = '{email}'")
        data = cur.fetchall()
        return data

def insertSetelahUsulan(email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO public.nilai_resiko_setelah_usulan (email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5) VALUES ('{email}','{id_app}', '{criteria_1}', '{criteria_2}', '{criteria_3}', '{criteria_4}', '{criteria_5}')")
    return True

def updateSetelahUsulan(email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE public.nilai_resiko_setelah_usulan SET criteria_1='{criteria_1}', criteria_2='{criteria_2}', criteria_3='{criteria_3}', criteria_4='{criteria_4}', criteria_5='{criteria_5}' WHERE public.nilai_resiko_setelah_usulan.id_app='{id_app}' AND public.nilai_resiko_setelah_usulan.email='{email}'")
    return True

def deleteSetelahUsulan(id_app, email):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM public.nilai_resiko_setelah_usulan WHERE public.nilai_resiko_saat_usulan.id_app='{id_app}' AND public.nilai_resiko_saat_usulan.email='{email}'")
    return True
