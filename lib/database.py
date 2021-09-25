import psycopg2

def db_connect():
    host = 'ec2-34-232-191-133.compute-1.amazonaws.com'
    database = 'daudm96pnqgqr7'
    user = 'umxqcnplleinrk'
    password = '31c80ef7ca7f40f36300adc5207f3709e1baa1b25700e3545240f95aaef67bf5'
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    return conn