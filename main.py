from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import pymysql
import os
import time
from mylib import *
app=Flask(__name__)
app.secret_key="super secret key"
app.config["UPLOAD_FOLDER"]= './static/photos'


@app.route("/", methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        specialised= request.form['T16']
        sql = "select * from hosdata where specialised='" +specialised+ "'"
        cur = make_connection()
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('Search.html', result=result)
    else:
        return render_template('Search.html')


@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="GET"):
        return render_template("login.html")
    else:
        email=request.form["T1"]
        password=request.form["T2"]
        cur = make_connection()
        sql = "select * from logindata where email='" + email + "' AND password='"+password+"'"
        print(sql)
        cur.execute(sql)
        n = cur.rowcount
        print(n)
        if (n == 1):
            data=cur.fetchone()
            ut=data[2] #usertype is at index 2 in table
            #create session
            session["ut"]=ut
            session["email"]=email

            if(ut=="admin"):
                return redirect(url_for("admin_home"))
            elif(ut=="hospital"):
                return redirect(url_for("hospital_home"))
        else:
            return render_template("login.html",data1="Error : Either email or password is incorrect")


@app.route("/logout")
def logout():
    if('ut' in session):
        session.pop('ut',None)
        session.pop('email',None)
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for("welcome"))


@app.route("/error")
def error():
    return render_template("Error.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        specialised= request.form['T16']
        sql = "select * from hosdata where specialised='" +specialised+ "'"
        cur = make_connection()
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('Search.html', result=result)
    else:
        return render_template('Search.html')


@app.route("/admin_home")
def admin_home():
    if('ut' in session):
        ut=session['ut']
        if(ut=='admin'):
            return render_template('AdminHome.html')
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route("/adminreg", methods=["GET","POST"])
def adminreg():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'admin':
            if(request.method=="POST"):
                name=request.form["T1"]
                address=request.form["T2"]
                contact=request.form["T3"]
                email=request.form["T4"]
                password=request.form["T5"]
                confirm=request.form["T6"]
                usertype="admin"
                cur=make_connection()
                a="insert into admindata values('"+name+"', '"+address+"', '"+contact+"', '"+email+"')"
                l="insert into logindata values('"+email+"', '"+password+"', '"+usertype+"')"
                cur.execute(a)
                n=cur.rowcount
                cur.execute(l)
                m=cur.rowcount

                if(n==1 and m==1):
                    msg="Data saved and login created"
                elif(n==1):
                    msg="Only data is saved"
                elif(m==1):
                    msg="Only login is created"
                else:
                    msg="No data saved and no login created"
                return render_template("AdminRegister.html", kota=msg)
            else:
                return render_template("AdminRegister.html")
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

@app.route("/horeg", methods=["GET","POST"])
def horeg():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'admin':
            if(request.method=="POST"):
                hospitalname = request.form["T1"]
                address = request.form["T2"]
                contact = request.form["T3"]
                email = request.form["T4"]
                emergency = request.form["T5"]
                emergencycontact = request.form["T7"]
                ac = request.form["T8"]
                noac = request.form["T10"]
                nogeneral = request.form["T11"]
                opd = request.form["T12"]
                surgery = request.form["T14"]
                specialised = request.form["T16"]
                password=request.form["T17"]
                usertype="hospital"
                cur=make_connection()
                a = "insert into hosdata values('"+hospitalname+"','"+address+"','"+contact+"','"+email+"','"+emergency+"','"+emergencycontact+"','"+ac+"','"+noac+"','"+nogeneral+"','"+opd+"','"+surgery+"','"+specialised+"')"
                l = "insert into logindata values('" + email + "', '" + password + "', '" + usertype + "')"

                cur.execute(a)
                n=cur.rowcount
                cur.execute(l)
                m = cur.rowcount
                if (n == 1 and m == 1):
                    msg = "Data saved and login created"
                elif (n == 1):
                    msg = "Only data is saved"
                elif (m == 1):
                    msg = "Only login is created"
                else:
                    msg = "No data saved and no login created"
                return render_template("HospitalReg.html", Hospital=msg)
            elif (request.method == "GET"):
                return render_template("HospitalReg.html")
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

@app.route('/show_hos')
def show_hos():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'admin':
            cur=make_connection()
            sql="select * from hosdata"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                values=[]
                data=cur.fetchall()

                for d in data:
                    print(d)
                    photo=check_photo(d[3])
                    a=[d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],d[11],photo]
                    values.append(a)
                print(values)
                return render_template("showHos.html",kota=values)
            else:
                return render_template("showHos.html",msg="No data found")
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

@app.route('/admin_profile')
def admin_profile():
    if ('ut' in session):
        ut = session['ut']
        email = session['email']
        if (ut == 'admin'):
            photo = check_photo(email)
            name = get_admin_name(email)
            cur = make_connection()
            cur.execute("select * from admindata where email='" + email + "'")
            result = cur.fetchone()

            return render_template('AdminProfile.html',e=email, photo=photo, name=name, row=result)
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/adminphoto')
def adminphoto():
    return render_template('PhotoUpload_admin.html')


@app.route('/adminphoto1', methods=['GET', 'POST'])
def adminphoto1():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'admin':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cur = make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('PhotoUpload_admin1.html', result="success")
                        else:
                            return render_template('PhotoUpload_admin1.html', result="failure")
                    except:
                        return render_template('PhotoUpload_admin1.html', result="duplicate")
            else:
                return render_template('PhotoUpload_admin.html')
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/adminphoto2', methods=['GET', 'POST'])
def adminphoto2():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'admin':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    filename = secure_filename(file.filename)
                    cur = make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('PhotoUpload_admin1.html', result="success")
                        else:
                            return render_template('PhotoUpload_admin1.html', result="failure")
                    except:
                        return render_template('PhotoUpload_admin1.html', result="duplicate")
            else:
                return render_template('PhotoUpload_admin.html')
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

@app.route('/change_adminphoto')
def change_adminphoto():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'admin':
            photo = check_photo(email)
            cur = make_connection()
            sql = "delete from photodata where email='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n > 0:
                os.remove("./static/photos/" + photo)
                return render_template('Change_AdminPhoto.html', data="success")
            else:
                return render_template('Change_AdminPhoto.html', data="failure")
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

@app.route('/edit_admin', methods=['GET','POST'])
def edit_admin():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'admin':
            if (request.method == "POST"):
                email = request.form["H1"]
                cur=make_connection()
                sql="select * from admindata where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                   data=cur.fetchone()
                   return render_template("editAdmin.html",kota=data)
                else:
                    return render_template("editAdmin.html",msg="No data found")
            else:
                return redirect(url_for('admin_profile'))
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/edit_admin1',methods=["GET","POST"])
def edit_admin1():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'admin':
            if (request.method=="POST"):
                name= request.form["T1"]
                address = request.form["T2"]
                contact = request.form["T3"]
                email = request.form["T4"]

                cur=make_connection()
                sql="update admindata set name='"+name+"', address='"+address+"',contact='"+contact+"' where email='"+email+"'"
                print(sql)
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("editAdmin1.html", vgt="Updated Successfully")
                else:
                    return render_template("editAdmin1.html", vgt="Cannot update")
            else:
                return redirect(url_for('admin_profile'))
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route("/cp_admin",methods=["GET","POST"])
def cp_admin():
    if ('ut' in session):
        ut = session['ut']
        if (ut == 'admin'):
            if(request.method=="GET"):
                return render_template("cp_admin.html")
            else:
                email =session["email"]
                oldpass=request.form["T1"]
                password = request.form["T2"]
                cur = make_connection()
                sql = "update logindata set password='"+password+"' where email='" + email + "' AND password='" + oldpass + "'"
                print(sql)
                cur.execute(sql)
                n = cur.rowcount

                if (n == 1):
                    return render_template("cp_admin.html",msg="Password Changed")
                else:
                    return render_template("cp_admin.html",msg="Password Not Changed")
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route("/hospital_home",methods=["GET","POST"])
def hospital_home():
    if 'ut' in session:
        ut = session['ut']
        if ut == 'hospital':
            return render_template('HospitalHome.html')
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/cp_hospital',methods=["GET","POST"])
def cp_hospital():
    if ('ut' in session):
        ut = session['ut']
        if (ut == 'hospital'):
            if(request.method=="GET"):
                return render_template('cp_hospital.html')
            else:
                oldpasswd=request.form["T1"]
                password=request.form["T2"]
                email=session["email"]
                cur=make_connection()
                sql="update logindata set password='"+password+"' where email='"+email+"' AND password='"+oldpasswd+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("cp_hospital.html",msg="Password Changed")
                else:
                    return render_template("cp_hospital.html",msg="Password Not Changed")
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/hospital_profile')
def hospital_profile():
    if ('ut' in session):
        ut = session['ut']
        email = session['email']
        if (ut == 'hospital'):
            photo = check_photo(email)
            name = get_hospital_name(email)
            cur = make_connection()
            cur.execute("select * from hosdata where email='" + email + "'")
            result = cur.fetchone()
            return render_template('HospitalProfile.html', e=email, photo=photo, name=name,row=result)
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/hospitalphoto')
def hospitalphoto():
    return render_template('PhotoUpload_hospital.html')


@app.route('/hphoto1', methods=['GET', 'POST'])
def hphoto1():
    if 'ut' in session:
        ut = session['ut']

        if ut == 'admin':
            if request.method == 'POST':
                email=request.form["H1"]
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cur = make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return redirect(url_for("show_hos"))
                        else:
                            return render_template('PhotoUpload_hospital1.html', result="failure")
                    except:
                        return render_template('PhotoUpload_hospital1.html', result="duplicate")
            else:
                return render_template('PhotoUpload_hospital.html')
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/hospitalphoto1', methods=['GET', 'POST'])
def hospitalphoto1():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'hospital':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cur = make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('PhotoUpload_hospital1.html', result="success")
                        else:
                            return render_template('PhotoUpload_hospital1.html', result="failure")
                    except:
                        return render_template('PhotoUpload_hospital1.html', result="duplicate")
            else:
                return render_template('PhotoUpload_hospital.html')
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/hospitalphoto2', methods=['GET', 'POST'])
def hospitalphoto2():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'hospital':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    filename = secure_filename(file.filename)
                    cur = make_connection()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('PhotoUpload_hospital1.html', result="success")
                        else:
                            return render_template('PhotoUpload_hospital1.html', result="failure")
                    except:
                        return render_template('PhotoUpload_hospital1.html', result="duplicate")
            else:
                return render_template('PhotoUpload_hospital.html')
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

@app.route('/change_hospitalphoto')
def change_hospitalphoto():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'hospital':
            photo = check_photo(email)
            cur = make_connection()
            sql = "delete from photodata where email='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n > 0:
                os.remove("./static/photos/" + photo)
                return render_template('Change_HospitalPhoto.html', data="success")
            else:
                return render_template('Change_HospitalPhoto.html', data="failure")
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/edit_hos', methods=['GET','POST'])
def edit_hos():
    if(request.method=="POST"):
        email_of_hospital = request.form['H1']
        cur=make_connection()
        sql="select * from hosdata where email='"+email_of_hospital+"' "
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            data=cur.fetchone()
            return render_template("EditHos.html",kota=data)
        else:
            return render_template("EditHos.html",msg="No data found")
    else:
        return redirect(url_for("hospital_profile"))


@app.route('/edit_hos1',methods=["GET","POST"])
def edit_hos1():
    if (request.method=="POST"):
        hospitalname = request.form["T1"]
        address = request.form["T2"]
        contact = request.form["T3"]
        email_of_hospital = request.form['T4']
        emergency = request.form["T5"]
        emergencycontact = request.form["T7"]
        ac = request.form["T8"]
        noac = request.form["T10"]
        nogeneral = request.form["T11"]
        opd = request.form["T12"]
        surgery = request.form["T14"]
        specialised = request.form["T16"]
        cur=make_connection()
        sql="update hosdata set hospitalname='"+hospitalname+"',address='"+address+"',contact='"+contact+"' ,emergency='"+emergency+"', emergencycontact='"+emergencycontact+"',ac= '"+ac+"',noac= '"+noac+"' ,nogeneral='"+nogeneral+"',opd= '"+opd+"',surgery='"+surgery+"' ,specialised='"+specialised+"' where email='"+email_of_hospital+"' "
        print(sql)
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            return render_template("EditHos1.html",vgt="Updated Successfully ")
        else:
            return render_template("EditHos1.html",vgt="Cannot Update")
    else:
        return redirect(url_for('hospital_profile'))


@app.route('/delete_hos', methods=['GET','POST'])
def delete_hos():
    if(request.method=="POST"):
        email=request.form["H1"]
        cur=make_connection()
        sql="select * from hosdata where email='"+email+"' "
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            data=cur.fetchone()
            return render_template("DeleteHos.html",kota=data)
        else:
            return render_template("DeleteHos.html",msg="No data found")
    else:
        return redirect(url_for("show_hos"))


@app.route('/delete_hos1',methods=["GET","POST"])
def delete_hos1():
    if (request.method=="POST"):
        email = request.form["H1"]
        cur=make_connection()
        sql="delete from hosdata where email='"+email+"' "
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            return render_template("DeleteHos1.html",vgt="Delete Successfully ")
        else:
            return render_template("DeleteHos1.html",vgt="Cannot Delete")
    else:
        return redirect(url_for('show_hos'))


@app.route("/drreg", methods=["GET", "POST"])
def drreg():
    if 'ut' in session:
        ut = session['ut']
        e1 = session['email']
        if ut == 'hospital':
            if (request.method=="POST"):
                drname = request.form["T1"]
                personaladdress = request.form["T2"]
                workaddress = request.form["T3"]
                personalcontact = request.form["T4"]
                workcontact = request.form["T5"]
                specialised = request.form["T7"]
                experience = request.form["T8"]
                feerange = request.form["T9"]

                email_of_hospital = e1
                cur=make_connection()
                a = "insert into drdata values('"+drname+"', '"+personaladdress+"', '"+workaddress+"' ,'"+personalcontact+"', '"+workcontact+"', '"+email_of_hospital+"','"+specialised+"', '"+experience+"', '"+feerange+"')"
                cur.execute(a)
                n = cur.rowcount

                if n == 1:
                     return render_template('DoctorReg.html', data="Doctor Added")
                else:
                     return render_template('DoctorReg.html', data="Error: Cannot add doctor")
            else:
                return render_template('DoctorReg.html')
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

@app.route('/show_drs')
def show_drs():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'hospital':
            doctors = get_doctors(email)
            cur=make_connection()
            sql="select * from drdata"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template("showDrs.html", doctors=doctors)
            else:
                return render_template("showDrs.html",msg="No data found")
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))


@app.route('/edit_dr', methods=['GET','POST'])
def edit_dr():
    if(request.method=="POST"):
        email=request.form["H1"]

        cur=make_connection()
        sql="select * from drdata where email='"+email+"' "
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            data=cur.fetchone()
            return render_template("EditDr.html",kota=data)
        else:
            return render_template("EditDr.html",msg="No data found")
    else:
        return redirect(url_for("show_drs"))


@app.route('/edit_dr1',methods=["GET","POST"])
def edit_dr1():
    if (request.method=="POST"):
        drname = request.form["T1"]
        personaladdress = request.form["T2"]
        workaddress = request.form["T3"]
        personalcontact = request.form["T4"]
        workcontact = request.form["T5"]
        email = request.form["T6"]
        specialised = request.form["T7"]
        experience = request.form["T8"]
        feerange = request.form["T9"]

        cur=make_connection()
        sql="update drdata set drname='"+drname+"',personaladdress='"+personaladdress+"',workaddress='"+workaddress+"' ,personalcontact='"+personalcontact+"', workcontact='"+workcontact+"', specialised='"+specialised+"',experience= '"+experience+"',feerange= '"+feerange+"' where email='"+email+"' "
        print(sql)
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            return render_template("EditDr1.html",vgt="Updated Successfully ")
        else:
            return render_template("EditDr1.html",vgt="Cannot Update")
    else:
        return redirect(url_for('show_drs'))


@app.route('/delete_dr', methods=['GET','POST'])
def delete_dr():
    if(request.method=="POST"):
        email=request.form["H1"]

        cur=make_connection()
        sql="select * from drdata where email='"+email+"' "
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            data=cur.fetchone()
            return render_template("DeleteDr.html",kota=data)
        else:
            return render_template("DeleteDr.html",msg="No data found")
    else:
        return redirect(url_for("show_drs"))


@app.route('/delete_dr1',methods=["GET","POST"])
def delete_dr1():
    if (request.method=="POST"):
        email = request.form["H1"]
        cur=make_connection()
        sql="delete from drdata where email='"+email+"' "
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            return render_template("DeleteDr1.html",vgt="Delete Successfully ")
        else:
            return render_template("DeleteDr1.html",vgt="Cannot Delete")
    else:
        return redirect(url_for('show_drs'))




@app.route('/show_admins')
def show_admins():
    if 'ut' in session:
        ut = session['ut']
        email = session['email']
        if ut == 'admin':
            cur=make_connection()
            sql="select * from admindata "
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template("showAdmins.html",kota=data)
            else:
                return render_template("showAdmins.html",msg="No data found")
        else:
            return redirect(url_for('error'))
    else:
        return redirect(url_for('error'))

@app.route('/delete_admin', methods=['GET', 'POST'])
def delete_admin():
    if (request.method == "POST"):
        email = request.form["H1"]

        cur = make_connection()
        sql = "select * from admindata where email='"+email +"' "
        cur.execute(sql)
        n = cur.rowcount
        if (n == 1):
            data = cur.fetchone()
            return render_template("deleteAdmin.html", kota=data)
        else:
            return render_template("deleteAdmin.html", msg="No data found")
    else:
        return redirect(url_for("show_admins"))


@app.route('/delete_admin1', methods=["GET", "POST"])
def delete_admin1():
    if (request.method == "POST"):

        email = request.form["H1"]

        cur = make_connection()
        sql = "delete from admindata where email='" + email + "'"
        print(sql)
        cur.execute(sql)
        n = cur.rowcount
        if (n == 1):
            return render_template("deleteAdmin1.html", vgt="Delete Successfully")
        else:
            return render_template("deleteAdmin1.html", vgt="Cannot delete")
    else:
        return redirect(url_for("show_admins"))


#main fumction
if __name__=="__main__":
    app.run(debug=True)
