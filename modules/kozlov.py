from lib.database import db_connect

def getNilaiKozlov():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT public.bobot_aset.id_app, ((public.bobot_aset.criteria_1*0.3) + (public.bobot_aset.criteria_2*0.4) + (public.bobot_aset.criteria_3*0.3)) as result_assessment, th1, th2,	th3,	th4,	th5,	th6,	th7,	th8,	th9,	th10,	th11,	risk_value FROM public.bobot_aset JOIN public.nilai_resiko_kozlov ON public.bobot_aset.email = public.nilai_resiko_kozlov.email AND public.bobot_aset.email = 'user@gmail.com' AND public.bobot_aset.id_app = public.nilai_resiko_kozlov.id_app ORDER BY id_app ASC")
        data = cur.fetchall()
        return data

def getThreatWeight():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"select id_app, public.app_threat.id_threat, threat_weight from public.app_threat join public.threat on public.app_threat.id_threat = public.threat.id_threat order by id_app ASC")
        data = cur.fetchall()
        return data

def insertKozlov(email, th1, th2, th3, th4, th5, th6, th7, th8, th9, th10, th11, risk_value, id_app):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO public.nilai_resiko_kozlov (email, th1, th2, th3, th4, th5, th6, th7, th8, th9, th10, th11, risk_value, id_app) VALUES ('{email}', '{th1}', '{th2}', '{th3}', '{th4}', '{th5}', '{th6}', '{th7}', '{th8}', '{th9}', '{th10}', '{th11}', '{risk_value}', '{id_app}');")
    return True

def updateBobotAsset(email, id_app, criteria_1, criteria_2, criteria_3):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE public.bobot_aset SET criteria_1='{criteria_1}', criteria_2='{criteria_2}', criteria_3='{criteria_3}' WHERE public.bobot_aset.id_app='{id_app}' AND public.bobot_aset.email='{email}'")
    return True

def deleteKozlov(email):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM public.nilai_resiko_kozlov WHERE public.nilai_resiko_kozlov.email='{email}'")
    return True
