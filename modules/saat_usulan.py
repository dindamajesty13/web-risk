from lib.database import db_connect

def getSaatUsulan():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5, ((public.nilai_resiko_saat_usulan.criteria_1*0.40) + (public.nilai_resiko_saat_usulan.criteria_2*0.20) + (public.nilai_resiko_saat_usulan.criteria_3*0.15) + (public.nilai_resiko_saat_usulan.criteria_4*0.15) + (public.nilai_resiko_saat_usulan.criteria_5*0.10)) as result_assessment FROM public.nilai_resiko_saat_usulan WHERE email = 'user@gmail.com' ORDER BY id_app ASC")
        data = cur.fetchall()
        return data

def getCountSaatUsulan(email):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"select count(email) from public.nilai_resiko_saat_usulan where email = '{email}'")
        data = cur.fetchall()
        return data

def insertSaatUsulan(email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO public.nilai_resiko_saat_usulan (email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5) VALUES ('{email}','{id_app}', '{criteria_1}', '{criteria_2}', '{criteria_3}', '{criteria_4}', '{criteria_5}')")
    return True

def updateSaatUsulan(email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE public.nilai_resiko_saat_usulan SET criteria_1='{criteria_1}', criteria_2='{criteria_2}', criteria_3='{criteria_3}', criteria_4='{criteria_4}', criteria_5='{criteria_5}' WHERE public.nilai_resiko_saat_usulan.id_app='{id_app}' AND public.nilai_resiko_saat_usulan.email='{email}'")
    return True

def deleteSaatUsulan(id_app, email):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM public.nilai_resiko_saat_usulan WHERE public.nilai_resiko_saat_usulan.id_app='{id_app}' AND public.nilai_resiko_saat_usulan.email='{email}'")
    return True
