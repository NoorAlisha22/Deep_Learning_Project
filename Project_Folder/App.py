from flask import Flask, render_template, flash, request, session, send_file
import pickle
import numpy as np
import mysql.connector
import sys
from keras.preprocessing import image
import webbrowser

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/NewDoctor")
def NewDoctor():
    return render_template('NewDoctor.html')


@app.route("/DoctorLogin")
def DoctorLogin():
    return render_template('DoctorLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/DoctorInfo")
def DoctorInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb  ")
    data = cur.fetchall()
    return render_template('DoctorInfo.html', data=data)


@app.route("/ADRemove")
def ADRemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from doctortb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Doctor  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb  ")
    data = cur.fetchall()
    return render_template('DoctorInfo.html', data=data)


@app.route("/AURemove")
def AURemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from regtb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('User  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/ADrugInfo")
def ADrugInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  apptb   ")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  drugtb   ")
    data1 = cur.fetchall()
    return render_template('ADrugInfo.html', data=data, data1=data1)


@app.route("/newdoct", methods=['GET', 'POST'])
def newdoct():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']
        specialist = request.form['Specialist']

        uname = request.form['uname']
        password = request.form['password']

        locat = request.form['locat']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctortb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','" + specialist + "','" + uname + "','" + password + "','" + locat + "')")
        conn.commit()
        conn.close()
        flash('Doctor  Register Successfully')
        return render_template('DoctorLogin.html')


@app.route("/doctlogin", methods=['GET', 'POST'])
def doctlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['ename'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from doctortb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('DoctorLogin.html', data=data)
        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('DoctorHome.html', data=data)


@app.route("/DoctorHome")
def DoctorHome():
    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb where username='" + username + "' ")
    data = cur.fetchall()
    return render_template('DoctorHome.html', data=data)


@app.route("/DAppoitmentInfo")
def DAppoitmentInfo():
    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
    data1 = cur.fetchall()

    return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/Accept")
def Accept():
    id = request.args.get('id')
    session["rid"] = id
    return render_template('AcceptLink.html')


@app.route("/appointment1", methods=['GET', 'POST'])
def appointment1():
    if request.method == 'POST':
        urllink = request.form['urllink']

        if urllink == "":
            urllink = "None"

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute(
            "update   apptb set status='Accept',urlLink='" + urllink + "' where id='" + session["rid"] + "'")
        conn.commit()
        conn.close()

        flash('Appointment Status  Update  Successfully!')

        username = session['ename']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
        data1 = cur.fetchall()

        return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/Reject")
def Reject():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cursor = conn.cursor()
    cursor.execute(
        "update apptb set status='Reject' where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Appointment Status  Update  Successfully!')

    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
    data1 = cur.fetchall()

    return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/AssignDrug")
def AssignDrug():
    id = request.args.get('id')
    st = request.args.get('st')
    session['apid'] = id
    if st == "Accept":
        return render_template('DAssignDrug.html')
    else:
        flash("Appointment Reject")
        username = session['ename']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
        data1 = cur.fetchall()

        return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/drugs", methods=['GET', 'POST'])
def drugs():
    if request.method == 'POST':

        date = request.form['date']
        minfo = request.form['minfo']
        oinfo = request.form['oinfo']
        amount = request.form['amount']

        file = request.files['file']
        file.save("static/upload/" + file.filename)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM apptb where  id='" + session['apid'] + "'")
        data = cursor.fetchone()

        if data:
            uname = data[1]
            mobile = data[2]
            email = data[3]
            dname = data[4]

        else:

            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  drugtb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + dname + "','" +
            minfo + "','" + oinfo + "','" + file.filename + "','" + date + "','" + amount + "','NotPaid')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM drugtb where DoctorName='" + dname + "' ")
        data = cur.fetchall()
        return render_template('DrugsInfo.html', data=data)


@app.route("/DrugsInfo")
def DrugsInfo():
    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM drugtb where DoctorName='" + username + "' ")
    data = cur.fetchall()
    return render_template('DrugsInfo.html', data=data)


@app.route('/download')
def download():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM drugtb where  id = '" + str(id) + "'")
    data = cursor.fetchone()
    if data:
        status = data[10]
        if status == "Paid":
            filename = "static\\upload\\" + data[7]

            return send_file(filename, as_attachment=True)
        else:
            flash('Not Paid')
            uname = session['uname']
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
            data = cur.fetchall()
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
            data1 = cur.fetchall()
            return render_template('UDrugsInfo.html', data=data, data1=data1)

    else:
        return 'Incorrect username / password !'


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']

        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')
        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb where username='" + uname + "'  ")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route("/Predict")
def Predict():
    return render_template('Predict.html')


@app.route("/otos", methods=['GET', 'POST'])
def otos():
    if request.method == 'POST':
        import tensorflow as tf
        import cv2

        file = request.files['file']
        file.save('static/upload/Test.jpg')
        fname = 'static/upload/Test.jpg'
        img1 = cv2.imread('static/upload/Test.jpg')
        dst = cv2.fastNlMeansDenoisingColored(img1, None, 10, 10, 7, 21)
        noi = 'static/upload/noi.jpg'

        cv2.imwrite(noi, dst)

        import warnings
        warnings.filterwarnings('ignore')

        model = tf.keras.models.load_model('Model/model.h5')
        img = image.load_img('static/upload/Test.jpg', target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize

        prediction = model.predict(img_array)
        ind = np.argmax(prediction)

        if ind == 0:
            print("aom")
            out = "aom"
            session['Ans'] = 'Yes'
        elif ind == 1:
            print("csom")
            out = "csom"
            session['Ans'] = 'Yes'
        elif ind == 2:
            print("earwax")
            out = "earwax"
            session['Ans'] = 'Yes'
        elif ind == 3:
            print("normal")
            out = "normal"
            session['Ans'] = 'No'
        elif ind == 4:
            print("otitisexterna")
            out = "otitisexterna"
            session['Ans'] = 'Yes'
        elif ind == 5:
            print("tympanoskleros")
            out = "tympanoskleros"
            session['Ans'] = 'Yes'

        return render_template('Answer.html', result=out, org=fname, noi=noi)


@app.route("/ViewDoctor", methods=['GET', 'POST'])
def ViewDoctor():
    if request.method == 'POST':

        ans = session['Ans']

        if ans == 'Yes':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb  ")
            data = cur.fetchone()
            if data is None:
                uname = session['uname']

                flash('No Doctor Found!')
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM regtb where username='" + uname + "' ")
                data = cur.fetchall()

                return render_template('UserHome.html', data=data)



            else:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM doctortb  ")
                data = cur.fetchall()
                return render_template('ViewDoctor.html', data=data)




        else:
            uname = session['uname']
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + uname + "' ")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


@app.route("/Appointment")
def Appointment():
    dname = request.args.get('id')
    session['dname'] = dname

    return render_template('Appointment.html')


@app.route("/appointment", methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        dname = session['dname']
        uname = session['uname']
        date = request.form['date']
        info = request.form['info']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM regtb where  UserNAme='" + uname + "'")
        data = cursor.fetchone()

        if data:
            mobile = data[3]
            email = data[2]


        else:

            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  apptb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + dname + "','" + date + "','" + info + "','waiting','None')")
        conn.commit()
        conn.close()

        uname = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
        data1 = cur.fetchall()
        return render_template('UDrugsInfo.html', data=data, data1=data1)


@app.route("/ujoin")
def ujoin():
    uname = session['uname']
    id11 = request.args.get('id')
    print(id11)
    if id11 != "None":

        webbrowser.open(id11)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
        data = cur.fetchall()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
        data1 = cur.fetchall()
        return render_template('UDrugsInfo.html', data=data, data1=data1)
    else:
        flash('No Link Provide')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
        data = cur.fetchall()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
        data1 = cur.fetchall()
        return render_template('UDrugsInfo.html', data=data, data1=data1)


@app.route("/UDrugsInfo")
def UDrugsInfo():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
    data1 = cur.fetchall()
    return render_template('UDrugsInfo.html', data=data, data1=data1)


@app.route("/payment")
def payment():
    asid = request.args.get('id')
    amt = request.args.get('amt')
    session['aid'] = asid
    return render_template('Payment.html',amt=amt)



@app.route("/apayment", methods=['GET', 'POST'])
def apayment():
    if request.method == 'POST':

        amt = request.args.get('amt')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cursor = conn.cursor()
        cursor.execute(
            "update   drugtb set Status='Paid' where id='" + session["aid"] + "'")
        conn.commit()
        conn.close()
        uname = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
        data = cur.fetchall()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3otoscopydb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
        data1 = cur.fetchall()
        return render_template('UDrugsInfo.html', data=data, data1=data1)





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
