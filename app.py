from flask import Flask

from admin.app_threat import getAppThreat, insertAppThreat, deleteAppThreat
from admin.login import getAdmin
from admin.vulnerability import getVulnerability, insertVulnerability, deleteVulnerability, updateVulnerability, \
    getCountVulnerability
from admin.threat import getThreat, insertThreat, deleteThreat, updateThreat, getCountThreat
from admin.assets import getAssets, insertAsset, deleteAsset, updateAsset
from flask import render_template, request, redirect, url_for, flash, session
import hashlib

from admin.vulnerability_avg import getVulnerabilityAVG, insertVulnerabilityAVG, deleteVulnerabilityAVG
from modules.bobot_aset import getBobotAssets, insertBobotAsset, deleteBobotAsset, updateBobotAsset, getCountData, \
    getCountAsset
from modules.kozlov import getNilaiKozlov, deleteKozlov, insertKozlov
from modules.login import getUsers
from modules.saat_usulan import getSaatUsulan, getCountSaatUsulan, insertSaatUsulan, updateSaatUsulan, deleteSaatUsulan
from modules.sebelum_usulan import getThreatWeight, getNilaiSebelumUsulan, insertSebelumUsulan, deleteSebelumUsulan
from modules.setelah_usulan import getSetelahUsulan, insertSetelahUsulan, deleteSetelahUsulan, updateSetelahUsulan
from modules.shareeful import getNilaiShareeful, deleteShareeful, insertShareeful

app = Flask(__name__)
app.secret_key = 'many random bytes'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        password_hash = hashlib.md5(password.encode())
        account = getUsers(username, password_hash.hexdigest())
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = username
            # Redirect to home page
            return redirect(url_for('index_bobot_aset'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            # Show the login form with message (if any)
            return render_template('login_user.html', msg=msg)

    if request.method == 'GET':
        if 'loggedin' in session and session['loggedin'] == True:
            return redirect(url_for('index_bobot_aset'))
        return render_template('login_user.html')

@app.route('/admin/home', methods=['GET', 'POST'])
def home_admin():
    if 'loggedin_admin' in session:
        id_app = getAssets()
        data_app_threat = getAppThreat()
        data_vulnerability_avg = getVulnerabilityAVG()
        data_hitung_avg = hitungAVG(data_vulnerability_avg)

        final = hitungVulnerability(data_app_threat, data_hitung_avg)
        average = []
        for data in id_app:
            average.append(final[data[0]]['average'])

        data_vulnerability_avg = getVulnerabilityAVG()

        final_data = hitungAVG(data_vulnerability_avg)

        threat_data = getThreat()
        threat_avg = []
        for data in threat_data:
            threat_avg.append(final_data[data[0]]['average'])

        count_asset = getCountAsset()
        count_threat = getCountThreat()
        count_vuln = getCountVulnerability()

        return render_template('home.html', final=average, id_app=id_app, threat_data=threat_data, final_data=threat_avg, count_asset=count_asset[0][0], count_threat=count_threat[0][0], count_vuln=count_vuln[0][0])
    return redirect(url_for('login'))

@app.route('/bobot_aset')
def index_bobot_aset():
    if 'loggedin' in session:
        id_app = getAssets()
        data_bobot_aset = getBobotAssets()
        email = session['username']
        count_data = getCountData(email)
        count_asset = getCountAsset()

        return render_template('bobot_aset.html', data_bobot_aset=data_bobot_aset, id_app=id_app,count_data=count_data[0][0], count_asset=count_asset[0][0])

    return redirect(url_for('home'))

@app.route('/admin/bobot_aset')
def index_calculate_aset():
    if 'loggedin_admin' in session:
        data_bobot_aset = getBobotAssets()

        return render_template('calculate_aset.html', data_bobot_aset=data_bobot_aset)

    return redirect(url_for('login'))

@app.route('/bobot_aset/insert', methods = ['POST'])
def insert_bobot_aset():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        email = request.form['email']
        id_app = request.form['id_app']
        criteria_1 = request.form['criteria_1']
        criteria_2 = request.form['criteria_2']
        criteria_3 = request.form['criteria_3']
        insertBobotAsset(email, id_app, criteria_1, criteria_2, criteria_3)
    return redirect(url_for('index_bobot_aset'))

@app.route('/bobot_aset/delete/<string:id_app>', methods = ['GET'])
def delete_bobot_aset(id_app):
    flash("Record Has Been Deleted Successfully")
    email = 'user@gmail.com'
    deleteBobotAsset(id_app, email)
    return redirect(url_for('index_bobot_aset'))

@app.route('/bobot_aset/update',methods=['POST','GET'])
def update_bobot_aset():

    if request.method == 'POST':
        email = session['username']
        id_app = request.form['id_app']
        criteria_1 = request.form['criteria_1']
        criteria_2 = request.form['criteria_2']
        criteria_3 = request.form['criteria_3']
        updateBobotAsset(email, id_app, criteria_1, criteria_2, criteria_3)
        flash("Data Updated Successfully")
        return redirect(url_for('index_bobot_aset'))

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        password_hash = hashlib.md5(password.encode())
        account = getAdmin(username, password_hash.hexdigest())
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin_admin'] = True
            session['admin'] = username
            # Redirect to home page
            return redirect(url_for('home_admin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            # Show the login form with message (if any)
            return render_template('login.html', msg=msg)

    if request.method == 'GET':
        if 'loggedin_admin' in session and session['loggedin_admin'] == True:
            return redirect(url_for('home_admin'))
        return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('home'))

@app.route('/admin/logout')
def logout_admin():
    # Remove session data, this will log the user out
   session.pop('loggedin_admin', None)
   session.pop('id', None)
   session.pop('admin', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/admin/vulnerability')
def index():
    if 'loggedin_admin' in session:
        data_vulnerability = getVulnerability()
        return render_template('vulnerability.html', data_vulnerability=data_vulnerability)
    return redirect(url_for('login'))

@app.route('/admin/vulnerability/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id_vulnerability = request.form['id_vulnerability']
        vulnerability_name = request.form['vulnerability_name']
        vulnerability_level = request.form['vulnerability_level']
        insertVulnerability(id_vulnerability, vulnerability_name, vulnerability_level)
        return redirect(url_for('index'))

@app.route('/admin/vulnerability/delete/<string:id_vulnerability>', methods = ['GET'])
def delete(id_vulnerability):
    flash("Record Has Been Deleted Successfully")
    deleteVulnerability(id_vulnerability)
    return redirect(url_for('index'))

@app.route('/admin/vulnerability/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_vulnerability = request.form['id_vulnerability']
        vulnerability_name = request.form['vulnerability_name']
        vulnerability_level = request.form['vulnerability_level']
        updateVulnerability(id_vulnerability, vulnerability_name, vulnerability_level)
        flash("Data Updated Successfully")
        return redirect(url_for('index'))

@app.route('/admin/threat')
def index_threat():
    if 'loggedin_admin' in session:
        data_threat = getThreat()
        return render_template('threat.html', data_threat=data_threat)
    return redirect(url_for('login'))

@app.route('/admin/threat/insert', methods = ['POST'])
def insert_threat():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id_threat = request.form['id_threat']
        threat_type = request.form['threat_type']
        threat_weight = request.form['threat_weight']
        insertThreat(id_threat, threat_type, threat_weight)
        return redirect(url_for('index_threat'))

@app.route('/admin/threat/delete/<string:id_threat>', methods = ['GET'])
def delete_threat(id_threat):
    flash("Record Has Been Deleted Successfully")
    deleteThreat(id_threat)
    return redirect(url_for('index_threat'))

@app.route('/admin/threat/update',methods=['POST','GET'])
def update_threat():

    if request.method == 'POST':
        id_threat = request.form['id_threat']
        threat_type = request.form['threat_type']
        threat_weight = request.form['threat_weight']
        updateThreat(id_threat, threat_type, threat_weight)
        flash("Data Updated Successfully")
        return redirect(url_for('index_threat'))

@app.route('/admin/asset')
def index_asset():
    if 'loggedin_admin' in session:
        data_asset = getAssets()
        return render_template('asset.html', data_asset=data_asset)
    return redirect(url_for('login'))

@app.route('/admin/asset/insert', methods = ['POST'])
def insert_asset():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id_app = request.form['id_app']
        application_name = request.form['application_name']
        insertAsset(id_app, application_name)
        return redirect(url_for('index_asset'))

@app.route('/admin/asset/delete/<string:id_app>', methods = ['GET'])
def delete_asset(id_app):
    flash("Record Has Been Deleted Successfully")
    deleteAsset(id_app)
    return redirect(url_for('index_asset'))

@app.route('/admin/asset/update',methods=['POST','GET'])
def update_asset():

    if request.method == 'POST':
        id_app = request.form['id_app']
        application_name = request.form['application_name']
        updateAsset(id_app, application_name)
        flash("Data Updated Successfully")
        return redirect(url_for('index_asset'))

def hitungAVG(data_vulnerability_avg):
    unique_id_threat_sum = {}
    unique_id_threat_avg = {}
    unique_id_threat_data_len = {}
    unique_id_threat_id_vuln = {}

    for data in data_vulnerability_avg:
        if data[0] in unique_id_threat_sum:
            id_vuln_temp = unique_id_threat_id_vuln[data[0]]
            id_vuln_temp.append(data[1])
            unique_id_threat_sum[data[0]] += data[5]
            unique_id_threat_data_len[data[0]] += 1
            unique_id_threat_id_vuln[data[0]] = id_vuln_temp
        else:
            id_vuln_temp = []
            id_vuln_temp.append(data[1])
            unique_id_threat_sum[data[0]] = data[5]
            unique_id_threat_data_len[data[0]] = 1
            unique_id_threat_id_vuln[data[0]] = id_vuln_temp

    for id_threat, id_vuln_list in unique_id_threat_id_vuln.items():
        unique_id_threat_id_vuln[id_threat] = ', '.join(id_vuln_list)

    for id_threat, value in unique_id_threat_sum.items():
        unique_id_threat_avg[id_threat] = round(unique_id_threat_sum[id_threat] / unique_id_threat_data_len[id_threat], 1)

    final_threat_avg_and_id_vuln = {}
    for id_threat in unique_id_threat_avg:
        final_threat_avg_and_id_vuln[id_threat] = {
            'average': unique_id_threat_avg[id_threat],
            'id_vulnerability': unique_id_threat_id_vuln[id_threat]
        }

    return final_threat_avg_and_id_vuln

@app.route('/admin/vulnerability_avg')
def index_vulnerability_avg():
    if 'loggedin_admin' in session:
        data_vulnerability_avg = getVulnerabilityAVG()

        final_data = hitungAVG(data_vulnerability_avg)

        threat_data = getThreat()
        vulnerability_data = getVulnerability()

        return render_template('vulnerability_avg.html', data_vulnerability_avg=final_data, threat_data=threat_data, vulnerability_data=vulnerability_data)
    return redirect(url_for('login'))

@app.route('/admin/vulnerability_avg/insert', methods = ['POST'])
def insert_vulnerability_avg():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id_threat = request.form['id_threat']
        id_vulnerability = request.form.getlist('id_vulnerability')
        for i in id_vulnerability:
            insertVulnerabilityAVG(id_threat, i)
        return redirect(url_for('index_vulnerability_avg'))

@app.route('/admin/vulnerability_avg/update', methods=['POST'])
def update_vulnerability_avg():
    id_threat = request.form['id_threat']
    id_vulnerability = request.form.getlist('id_vulnerability')
    deleteVulnerabilityAVG(id_threat)
    for i in id_vulnerability:
        insertVulnerabilityAVG(id_threat, i)
    flash("Data Updated Successfully")
    return redirect(url_for('index_vulnerability_avg'))

@app.route('/admin/vulnerability_avg/delete/<string:id_threat>', methods = ['GET'])
def delete_vulnerabily_avg(id_threat):
    flash("Record Has Been Deleted Successfully")
    deleteVulnerabilityAVG(id_threat)
    return redirect(url_for('index_vulnerability_avg'))

def hitungVulnerability(data_app_threat, data_hitung_avg):
    data_threat = {}
    data_id_threat = []
    data_value_threat = []
    for row in data_hitung_avg:
        data_id_threat.append(row)
        data_value_threat.append(data_hitung_avg[row]['average'])
        data_threat[row] = data_hitung_avg[row]['average']

    unique_id_app_id_threat = {}
    data_sum_threat = {}
    data_len_threat = {}
    threat_avg = {}

    for data in data_app_threat:
        if data[0] in unique_id_app_id_threat:
            id_threat_temp = unique_id_app_id_threat[data[0]]
            id_threat_temp.append(data[1])
            unique_id_app_id_threat[data[0]] = id_threat_temp
            if data[1] in data_id_threat:
                data_sum_threat[data[0]] += data_threat[data[1]]
                data_len_threat[data[0]] += 1
        else:
            id_threat_temp = []
            id_threat_temp.append(data[1])
            unique_id_app_id_threat[data[0]] = id_threat_temp
            if data[1] in data_id_threat:
                data_sum_threat[data[0]] = data_threat[data[1]]
                data_len_threat[data[0]] = 1

    for id_app, id_threat_list in unique_id_app_id_threat.items():
        unique_id_app_id_threat[id_app] = ', '.join(id_threat_list)

    for id_app, value in data_sum_threat.items():
        threat_avg[id_app] = round(data_sum_threat[id_app] / data_len_threat[id_app], 2)

    final = {}
    for id_app in unique_id_app_id_threat:
        final[id_app] = {
            'id_threat': unique_id_app_id_threat[id_app],
            'average': threat_avg[id_app]
        }
    return final

@app.route('/admin/app_threat')
def index_app_threat():
    if 'loggedin_admin' in session:
        data_app_threat = getAppThreat()
        data_vulnerability_avg = getVulnerabilityAVG()
        data_hitung_avg = hitungAVG(data_vulnerability_avg)

        final = hitungVulnerability(data_app_threat, data_hitung_avg)

        app_data = getAssets()
        threat_data = getThreat()

        return render_template('app_threat.html', data_app_threat = final, threat_data = threat_data, app_data = app_data)
    return redirect(url_for('login'))

@app.route('/admin/app_threat/insert', methods = ['POST'])
def insert_app_threat():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id_app = request.form['id_app']
        id_threat = request.form.getlist('id_threat')
        for i in id_threat:
            insertAppThreat(id_app, i)
        return redirect(url_for('index_app_threat'))

@app.route('/admin/app_threat/update', methods=['POST'])
def update_app_threat():
    id_app = request.form['id_app']
    id_threat = request.form.getlist('id_threat')
    deleteAppThreat(id_app)
    for i in id_threat:
        insertAppThreat(id_app, i)
    flash("Data Updated Successfully")
    return redirect(url_for('index_app_threat'))

@app.route('/admin/app_threat/delete/<string:id_app>', methods = ['GET'])
def delete_app_threat(id_app):
    flash("Record Has Been Deleted Successfully")
    deleteAppThreat(id_app)
    return redirect(url_for('index_app_threat'))

@app.route('/admin/before_migrating')
def index_before_migrating():
    data_sebelum_usulan = getNilaiSebelumUsulan()
    data_app_threat = getAppThreat()
    data_vulnerability_avg = getVulnerabilityAVG()
    data_hitung_avg = hitungAVG(data_vulnerability_avg)
    vulnerability = hitungVulnerability(data_app_threat, data_hitung_avg)
    return render_template('before_migrating.html', data_sebelum_usulan=data_sebelum_usulan, vulnerability=vulnerability)


@app.route('/sebelum_usulan')
def index_sebelum_usulan():
    if 'loggedin' in session:
        data_sebelum_usulan = getNilaiSebelumUsulan()
        data_app_threat = getAppThreat()
        data_vulnerability_avg = getVulnerabilityAVG()
        data_hitung_avg = hitungAVG(data_vulnerability_avg)
        vulnerability = hitungVulnerability(data_app_threat, data_hitung_avg)

        return render_template('sebelum_usulan.html', data_sebelum_usulan = data_sebelum_usulan, vulnerability=vulnerability)
    return redirect(url_for('home'))

@app.route('/sebelum_usulan/insert', methods=['POST'])
def insert_sebelum_usulan():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        email = session['username']
        deleteSebelumUsulan(email)
        final_data = hitungResikoSebelumUsulan()
        for datas in final_data['data']:
            for data in datas:
                email_user = session['username']
                th1 = datas[data]['probabilitas_threat']['TH-01']
                th2 = datas[data]['probabilitas_threat']['TH-02']
                th3 = datas[data]['probabilitas_threat']['TH-03']
                th4 = datas[data]['probabilitas_threat']['TH-04']
                th5 = datas[data]['probabilitas_threat']['TH-05']
                th6 = datas[data]['probabilitas_threat']['TH-06']
                th7 = datas[data]['probabilitas_threat']['TH-07']
                th8 = datas[data]['probabilitas_threat']['TH-08']
                th9 = datas[data]['probabilitas_threat']['TH-09']
                th10 = datas[data]['probabilitas_threat']['TH-10']
                th11 = datas[data]['probabilitas_threat']['TH-11']
                risk_value = datas[data]['hasil_akhir']
                id_app = data
                insertSebelumUsulan(email_user, th1, th2, th3, th4, th5, th6, th7, th8, th9, th10, th11, risk_value,
                                    id_app)
        return redirect(url_for('index_sebelum_usulan'))

def hitungResikoSebelumUsulan():
    global hasil_akhir
    threat_weight = getThreatWeight()
    bobot_aset  = getBobotAssets()
    data_app_threat = getAppThreat()
    data_vulnerability_avg = getVulnerabilityAVG()
    data_hitung_avg = hitungAVG(data_vulnerability_avg)
    data_app_threat_vulnerability = hitungVulnerability(data_app_threat, data_hitung_avg)
    data_threat = getThreat()

    nilai_bobot_aset = {}
    id_app_bobot_aset = []
    data_id_app = {}
    unique_id_app_sum = {}
    sum_risk_value = {}

    for data in bobot_aset:
        id_app_bobot_aset.append(data[0])
        nilai_bobot_aset[data[0]] = data[4]

    for i in threat_weight:
        if i[0] in id_app_bobot_aset:
            sum_th = round(i[2] * nilai_bobot_aset[i[0]] / 100, 2)
            if i[0] in data_id_app:
                id_app_temp = data_id_app[i[0]]
                id_app_temp.append(i[1])
                data_id_app[i[0]] = id_app_temp
                unique_id_app_sum[i[0]] += sum_th
            else:
                id_app_temp = []
                id_app_temp.append(i[1])
                data_id_app[i[0]] = id_app_temp
                unique_id_app_sum[i[0]] = sum_th

            for id_app, value in unique_id_app_sum.items():
                sum_risk_value[id_app] = value + data_app_threat_vulnerability[i[0]]['average']

            hasil_akhir = {}
            for id_app in unique_id_app_sum:
                hasil_akhir[id_app] = sum_risk_value[id_app]

    dict_sum_th = {}

    for i in threat_weight:
        if i[0] in dict_sum_th:
            list_temp_th = dict_sum_th[i[0]]
            dict_temp_th = {}
            if i[1] in data_id_app[i[0]]:
                dict_temp_th[i[1]] = round(i[2] * nilai_bobot_aset[i[0]] / 100, 2)
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th
            else:
                dict_temp_th[i[1]] = 0
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th
        else:
            list_temp_th = []
            dict_temp_th = {}
            if i[1] in data_id_app[i[0]]:
                dict_temp_th[i[1]] = round(i[2] * nilai_bobot_aset[i[0]] / 100, 2)
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th
            else:
                dict_temp_th[i[1]] = 0
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th


    list_id_threat = [i[0] for i in data_threat]

    final_sum_th = {}

    for k, v in dict_sum_th.items():
        dict_temp_th_2 = {}
        dict_temp_th_sum = {}
        for dict_data in v:
            for a, b in dict_data.items():
                dict_temp_th_2[a] = b

        for i in list_id_threat:
            if i in dict_temp_th_2:
                continue
            else:
                dict_temp_th_2[i] = 0

        for id_threat, sum in sorted(dict_temp_th_2.items()):
            dict_temp_th_sum[id_threat] = sum

        final_sum_th[k] = dict_temp_th_sum

    list_data_final = []

    for key, value in data_id_app.items():
        temp_dict = {}
        temp_dict[key] = {
            'probabilitas_threat': final_sum_th[key],
            'bobot': nilai_bobot_aset[key],
            'hasil_akhir': hasil_akhir[key]
        }
        list_data_final.append(temp_dict)

    final_data = {
        'data': list_data_final
    }

    return final_data

@app.route('/admin/saat_usulan')
def index_during_migration():
    if 'loggedin_admin' in session:
        id_app = getAssets()
        data_saat_usulan = getSaatUsulan()

        final_data = hitungDataSaatUsulan(data_saat_usulan)

        return render_template('during_migration.html', data_saat_usulan=data_saat_usulan, final_data=final_data, id_app=id_app)
    return redirect(url_for('login'))

@app.route('/saat_usulan')
def index_saat_usulan():
    if 'loggedin' in session:
        id_app = getAssets()
        data_saat_usulan = getSaatUsulan()
        email = session['username']
        count_data = getCountSaatUsulan(email)

        final_data = hitungDataSaatUsulan(data_saat_usulan)

        return render_template('saat_usulan.html', data_saat_usulan=data_saat_usulan, final_data=final_data, id_app=id_app, count_data=count_data[0][0])
    return redirect(url_for('home'))

@app.route('/saat_usulan/insert', methods = ['POST'])
def insert_saat_usulan():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        email = request.form['email']
        id_app = request.form['id_app']
        criteria_1 = request.form['criteria_1']
        criteria_2 = request.form['criteria_2']
        criteria_3 = request.form['criteria_3']
        criteria_4 = request.form['criteria_4']
        criteria_5 = request.form['criteria_5']
        insertSaatUsulan(email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5)
    return redirect(url_for('index_saat_usulan'))

@app.route('/saat_usulan/delete/<string:id_app>', methods = ['GET'])
def delete_saat_usulan(id_app):
    flash("Record Has Been Deleted Successfully")
    email = session['username']
    deleteSaatUsulan(id_app, email)
    return redirect(url_for('index_saat_usulan'))

@app.route('/saat_usulan/update',methods=['POST','GET'])
def update_saat_usulan():

    if request.method == 'POST':
        email = session['username']
        id_app = request.form['id_app']
        criteria_1 = request.form['criteria_1']
        criteria_2 = request.form['criteria_2']
        criteria_3 = request.form['criteria_3']
        criteria_4 = request.form['criteria_4']
        criteria_5 = request.form['criteria_5']
        updateSaatUsulan(email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5)
        flash("Data Updated Successfully")
        return redirect(url_for('index_saat_usulan'))

def hitungDataSaatUsulan(data_saat_usulan):
    data_unique_id_app = {}

    final_data = hitungResikoSebelumUsulan()
    data_final = {}
    sum_data_risk = {}

    for datas in final_data['data']:
        for data in datas:
            data_final[data] = datas[data]['hasil_akhir']

    for data in data_saat_usulan:
        if data[0] not in data_unique_id_app:
            sum_data = data_final[data[0]] + data[6]
            sum_data_risk[data[0]] = round(sum_data / 2, 2)
    final_data = {}
    for id_app in sum_data_risk:
        final_data[id_app] = {
            'risk_value': sum_data_risk[id_app]
        }
    return final_data

def hitungDataSetelahUsulan(data_setelah_usulan):
    final_data = hitungResikoSebelumUsulan()

    data_final = {}

    for datas in final_data['data']:
        for data in datas:
            data_final[data] = datas[data]['hasil_akhir']

    hasil_data = {}

    for data in data_setelah_usulan:
        if data[0] not in hasil_data:
            hasil_data[data[0]] = round((data_final[data[0]] + data[6]) / 2, 2)

    final = {}
    for id_app in hasil_data:
        final[id_app] = {
            'risk_value': hasil_data[id_app]
        }

    return final

@app.route('/admin/setelah_usulan')
def index_after_migration():
    if 'loggedin_admin' in session:
        id_app = getAssets()
        data_setelah_usulan = getSetelahUsulan()

        final = hitungDataSetelahUsulan(data_setelah_usulan)

        return render_template('after_migrating.html', data_setelah_usulan=data_setelah_usulan, final=final, id_app=id_app)
    return redirect(url_for('login'))

@app.route('/setelah_usulan')
def index_setelah_usulan():
    if 'loggedin' in session:
        id_app = getAssets()
        data_setelah_usulan = getSetelahUsulan()
        email = session['username']
        count_data = getCountSaatUsulan(email)

        final_data = hitungResikoSebelumUsulan()

        data_final = {}

        for datas in final_data['data']:
            for data in datas:
                data_final[data] = datas[data]['hasil_akhir']

        hasil_data = {}

        for data in data_setelah_usulan:
            if data[0] not in hasil_data:
                hasil_data[data[0]] = round((data_final[data[0]] + data[6])/2, 2)

        final = {}
        for id_app in hasil_data:
            final[id_app] = {
                'risk_value':hasil_data[id_app]
            }


        return render_template('setelah_usulan.html', data_setelah_usulan=data_setelah_usulan, final=final, id_app=id_app, count_data=count_data[0][0])
    return redirect(url_for('home'))

@app.route('/setelah_usulan/insert', methods = ['POST'])
def insert_setelah_usulan():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        email = request.form['email']
        id_app = request.form['id_app']
        criteria_1 = request.form['criteria_1']
        criteria_2 = request.form['criteria_2']
        criteria_3 = request.form['criteria_3']
        criteria_4 = request.form['criteria_4']
        criteria_5 = request.form['criteria_5']
        insertSetelahUsulan(email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5)
    return redirect(url_for('index_setelah_usulan'))

@app.route('/setelah_usulan/delete/<string:id_app>', methods = ['GET'])
def delete_setelah_usulan(id_app):
    flash("Record Has Been Deleted Successfully")
    email = session['username']
    deleteSetelahUsulan(id_app, email)
    return redirect(url_for('index_setelah_usulan'))

@app.route('/setelah_usulan/update',methods=['POST','GET'])
def update_setelah_usulan():

    if request.method == 'POST':
        email = session['username']
        id_app = request.form['id_app']
        criteria_1 = request.form['criteria_1']
        criteria_2 = request.form['criteria_2']
        criteria_3 = request.form['criteria_3']
        criteria_4 = request.form['criteria_4']
        criteria_5 = request.form['criteria_5']
        updateSetelahUsulan(email, id_app, criteria_1, criteria_2, criteria_3, criteria_4, criteria_5)
        flash("Data Updated Successfully")
        return redirect(url_for('index_setelah_usulan'))

def hitungResikoShareeful():
    global hasil_akhir
    threat_weight = getThreatWeight()
    bobot_aset  = getBobotAssets()
    data_threat = getThreat()

    nilai_bobot_aset = {}
    id_app_bobot_aset = []
    data_id_app = {}
    unique_id_app_sum = {}

    for data in bobot_aset:
        id_app_bobot_aset.append(data[0])
        nilai_bobot_aset[data[0]] = data[4]

    for i in threat_weight:
        if i[0] in id_app_bobot_aset:
            sum_th = round(i[2] * nilai_bobot_aset[i[0]] / 100, 2)
            if i[0] in data_id_app:
                id_app_temp = data_id_app[i[0]]
                id_app_temp.append(i[1])
                data_id_app[i[0]] = id_app_temp
                unique_id_app_sum[i[0]] += sum_th
            else:
                id_app_temp = []
                id_app_temp.append(i[1])
                data_id_app[i[0]] = id_app_temp
                unique_id_app_sum[i[0]] = sum_th

            hasil_akhir = {}
            for id_app in unique_id_app_sum:
                hasil_akhir[id_app] = unique_id_app_sum[id_app]

    dict_sum_th = {}

    for i in threat_weight:
        if i[0] in dict_sum_th:
            list_temp_th = dict_sum_th[i[0]]
            dict_temp_th = {}
            if i[1] in data_id_app[i[0]]:
                dict_temp_th[i[1]] = round(i[2] * nilai_bobot_aset[i[0]] / 100, 2)
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th
            else:
                dict_temp_th[i[1]] = 0
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th
        else:
            list_temp_th = []
            dict_temp_th = {}
            if i[1] in data_id_app[i[0]]:
                dict_temp_th[i[1]] = round(i[2] * nilai_bobot_aset[i[0]] / 100, 2)
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th
            else:
                dict_temp_th[i[1]] = 0
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th


    list_id_threat = [i[0] for i in data_threat]

    final_sum_th = {}

    for k, v in dict_sum_th.items():
        dict_temp_th_2 = {}
        dict_temp_th_sum = {}
        for dict_data in v:
            for a, b in dict_data.items():
                dict_temp_th_2[a] = b

        for i in list_id_threat:
            if i in dict_temp_th_2:
                continue
            else:
                dict_temp_th_2[i] = 0

        for id_threat, sum in sorted(dict_temp_th_2.items()):
            dict_temp_th_sum[id_threat] = sum

        final_sum_th[k] = dict_temp_th_sum

    list_data_final = []

    for key, value in data_id_app.items():
        temp_dict = {}
        temp_dict[key] = {
            'probabilitas_threat': final_sum_th[key],
            'bobot': nilai_bobot_aset[key],
            'hasil_akhir': hasil_akhir[key]
        }
        list_data_final.append(temp_dict)

    final_data = {
        'data': list_data_final
    }

    return final_data

@app.route('/shareeful')
def index_shareeful():
    if 'loggedin' in session:
        email = session['username']
        count_data = getCountData(email)
        data_shareefull = getNilaiShareeful()

        return render_template('shareeful.html', count_data=count_data[0][0], data_shareefull=data_shareefull)
    return redirect(url_for('home'))

@app.route('/shareeful/insert', methods = ['POST'])
def insert_shareeful():
    if request.method == "POST":
        flash("Data Calculated Successfully")
        email = session['username']
        deleteShareeful(email)
        final_data = hitungResikoShareeful()
        for datas in final_data['data']:
            for data in datas:
                email_user = session['username']
                th1 = datas[data]['probabilitas_threat']['TH-01']
                th2 = datas[data]['probabilitas_threat']['TH-02']
                th3 = datas[data]['probabilitas_threat']['TH-03']
                th4 = datas[data]['probabilitas_threat']['TH-04']
                th5 = datas[data]['probabilitas_threat']['TH-05']
                th6 = datas[data]['probabilitas_threat']['TH-06']
                th7 = datas[data]['probabilitas_threat']['TH-07']
                th8 = datas[data]['probabilitas_threat']['TH-08']
                th9 = datas[data]['probabilitas_threat']['TH-09']
                th10 = datas[data]['probabilitas_threat']['TH-10']
                th11 = datas[data]['probabilitas_threat']['TH-11']
                risk_value = datas[data]['hasil_akhir']
                id_app = data
                insertShareeful(email_user, th1, th2, th3, th4, th5, th6, th7, th8, th9, th10, th11, risk_value,id_app)

        return redirect(url_for('index_shareeful'))

@app.route('/admin/report')
def index_report():
    if 'loggedin_admin' in session:
        asset = getAssets()

        data_sebelum = {}
        data_sebelum_usulan = getNilaiSebelumUsulan()
        for i in data_sebelum_usulan:
            data_sebelum[i[0]] = i[13]

        data_saat_usulan = getSaatUsulan()

        final_data = hitungDataSaatUsulan(data_saat_usulan)

        data_setelah_usulan = getSetelahUsulan()

        final = hitungDataSetelahUsulan(data_setelah_usulan)

        return render_template('report.html', asset=asset, data_sebelum_usulan=data_sebelum, data_saat_usulan = final_data, data_setelah_usulan=final)
    return redirect(url_for('login'))

def hitungResikoKozlov():
    global hasil_akhir
    threat_weight = getThreatWeight()
    bobot_aset  = getBobotAssets()
    data_threat = getThreat()
    data_app_threat = getAppThreat()
    data_vulnerability_avg = getVulnerabilityAVG()
    data_hitung_avg = hitungAVG(data_vulnerability_avg)
    data_app_threat_vulnerability = hitungVulnerability(data_app_threat, data_hitung_avg)

    nilai_bobot_aset = {}
    id_app_bobot_aset = []
    data_id_app = {}
    unique_id_app_sum = {}
    len_id_th_tempt = {}
    sum_risk_value = {}

    for data in bobot_aset:
        id_app_bobot_aset.append(data[0])
        nilai_bobot_aset[data[0]] = data[4]

    for i in threat_weight:
        if i[0] in id_app_bobot_aset:
            sum_th = round(data_app_threat_vulnerability[i[0]]['average'] * i[2] * nilai_bobot_aset[i[0]] / 100, 2)
            if i[0] in data_id_app:
                id_app_temp = data_id_app[i[0]]
                id_app_temp.append(i[1])
                data_id_app[i[0]] = id_app_temp
                unique_id_app_sum[i[0]] += sum_th
                len_id_th_tempt[i[0]] += 1
            else:
                id_app_temp = []
                id_app_temp.append(i[1])
                data_id_app[i[0]] = id_app_temp
                unique_id_app_sum[i[0]] = sum_th
                len_id_th_tempt[i[0]] = 1

            for id_app, value in unique_id_app_sum.items():
                sum_risk_value[id_app] = round(value / len_id_th_tempt[id_app], 2)

            hasil_akhir = {}
            for id_app in unique_id_app_sum:
                hasil_akhir[id_app] = sum_risk_value[id_app]

    dict_sum_th = {}

    for i in threat_weight:
        if i[0] in dict_sum_th:
            list_temp_th = dict_sum_th[i[0]]
            dict_temp_th = {}
            if i[1] in data_id_app[i[0]]:
                dict_temp_th[i[1]] = round(data_app_threat_vulnerability[i[0]]['average'] * i[2] * nilai_bobot_aset[i[0]] / 100, 2)
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th
            else:
                dict_temp_th[i[1]] = 0
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th
        else:
            list_temp_th = []
            dict_temp_th = {}
            if i[1] in data_id_app[i[0]]:
                dict_temp_th[i[1]] = round(data_app_threat_vulnerability[i[0]]['average'] * i[2] * nilai_bobot_aset[i[0]] / 100, 2)
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th
            else:
                dict_temp_th[i[1]] = 0
                list_temp_th.append(dict_temp_th)
                dict_sum_th[i[0]] = list_temp_th


    list_id_threat = [i[0] for i in data_threat]

    final_sum_th = {}

    for k, v in dict_sum_th.items():
        dict_temp_th_2 = {}
        dict_temp_th_sum = {}
        for dict_data in v:
            for a, b in dict_data.items():
                dict_temp_th_2[a] = b

        for i in list_id_threat:
            if i in dict_temp_th_2:
                continue
            else:
                dict_temp_th_2[i] = 0

        for id_threat, sum in sorted(dict_temp_th_2.items()):
            dict_temp_th_sum[id_threat] = sum

        final_sum_th[k] = dict_temp_th_sum

    list_data_final = []

    for key, value in data_id_app.items():
        temp_dict = {}
        temp_dict[key] = {
            'probabilitas_threat': final_sum_th[key],
            'bobot': nilai_bobot_aset[key],
            'hasil_akhir': hasil_akhir[key]
        }
        list_data_final.append(temp_dict)

    final_data = {
        'data': list_data_final
    }

    return final_data

@app.route('/admin/kozlov')
def index_admin_kozlov():
    if 'loggedin_admin' in session:
        data_kozlov = getNilaiKozlov()
        data_app_threat = getAppThreat()
        data_vulnerability_avg = getVulnerabilityAVG()
        data_hitung_avg = hitungAVG(data_vulnerability_avg)
        vulnerability = hitungVulnerability(data_app_threat, data_hitung_avg)

        return render_template('admin_kozlov.html', data_kozlov=data_kozlov, vulnerability=vulnerability)
    return redirect(url_for('login'))

@app.route('/admin/shareeful')
def index_admin_shareeful():
    if 'loggedin_admin' in session:
        data_shareeful = getNilaiShareeful()

        return render_template('admin_shareeful.html', data_shareeful=data_shareeful)
    return redirect(url_for('login'))

@app.route('/kozlov')
def index_kozlov():
    if 'loggedin' in session:
        email = session['username']
        count_data = getCountData(email)
        data_kozlov = getNilaiKozlov()
        data_app_threat = getAppThreat()
        data_vulnerability_avg = getVulnerabilityAVG()
        data_hitung_avg = hitungAVG(data_vulnerability_avg)
        vulnerability = hitungVulnerability(data_app_threat, data_hitung_avg)

        return render_template('kozlov.html', count_data=count_data[0][0], data_kozlov=data_kozlov, vulnerability=vulnerability)
    return redirect(url_for('home'))

@app.route('/kozlov/insert', methods = ['POST'])
def insert_kozlov():
    if request.method == "POST":
        flash("Data Calculated Successfully")
        email = session['username']
        deleteKozlov(email)
        final_data = hitungResikoKozlov()
        for datas in final_data['data']:
            for data in datas:
                email_user = session['username']
                th1 = datas[data]['probabilitas_threat']['TH-01']
                th2 = datas[data]['probabilitas_threat']['TH-02']
                th3 = datas[data]['probabilitas_threat']['TH-03']
                th4 = datas[data]['probabilitas_threat']['TH-04']
                th5 = datas[data]['probabilitas_threat']['TH-05']
                th6 = datas[data]['probabilitas_threat']['TH-06']
                th7 = datas[data]['probabilitas_threat']['TH-07']
                th8 = datas[data]['probabilitas_threat']['TH-08']
                th9 = datas[data]['probabilitas_threat']['TH-09']
                th10 = datas[data]['probabilitas_threat']['TH-10']
                th11 = datas[data]['probabilitas_threat']['TH-11']
                risk_value = datas[data]['hasil_akhir']
                id_app = data
                insertKozlov(email_user, th1, th2, th3, th4, th5, th6, th7, th8, th9, th10, th11, risk_value,id_app)

        return redirect(url_for('index_kozlov'))

@app.route('/admin/perbandingan')
def index_perbandingan():
    if 'loggedin_admin' in session:
        asset = getAssets()

        global list_shareeful
        data_shareeful = hitungResikoShareeful()
        data_kozlov = hitungResikoKozlov()

        shareeful = {}
        for datas in data_shareeful['data']:
            for data in datas:
                shareeful[data] = datas[data]['hasil_akhir']

        print(shareeful)

        kozlov = {}

        for datas in data_kozlov['data']:
            for data in datas:
                kozlov[data] = datas[data]['hasil_akhir']

        print(kozlov)

        data_sebelum = {}
        data_sebelum_usulan = getNilaiSebelumUsulan()
        for i in data_sebelum_usulan:
            data_sebelum[i[0]] = i[13]

        data_saat_usulan = getSaatUsulan()

        final_data = hitungDataSaatUsulan(data_saat_usulan)

        data_setelah_usulan = getSetelahUsulan()

        final = hitungDataSetelahUsulan(data_setelah_usulan)

        return render_template('perbandingan.html', asset=asset, data_shareeful = shareeful, data_kozlov=kozlov, data_sebelum = data_sebelum, data_saat_usulan = final_data, data_setelah_usulan=final)

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
