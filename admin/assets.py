from lib.database import db_connect

def getAssets():
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM public.list_asset ORDER BY id ASC")
        data = cur.fetchall()
        return data


def insertAsset(id_app, application_name):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO public.list_asset (id_app, application_name) VALUES ('{id_app}', '{application_name}')")
    return True


def updateAsset(id_app, application_name):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE public.list_asset SET application_name='{application_name}' WHERE public.list_asset.id_app='{id_app}'")
    return True


def deleteAsset(id_app):
    conn = db_connect()
    with conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM public.list_asset WHERE public.list_asset.id_app='{id_app}'")
    return True
