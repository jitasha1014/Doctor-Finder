import pymysql

def make_connection():
    con =pymysql.connect(host="localhost", user="root", passwd="", port=3306 ,db="jitasha", autocommit=True)

    cur=con.cursor()
    return cur

def check_photo(email):
    cur = make_connection()
    cur.execute("SELECT * FROM photodata where email='" + email + "'")
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo

def get_admin_name(email):
    cur=make_connection()
    cur.execute("select * from admindata where email='"+email+"'")
    n=cur.rowcount
    name="no"
    if n>0:
        row=cur.fetchone()
        name=row[0]
    return name

def get_hospital_name(email):
    cur=make_connection()
    cur.execute("select * from hosdata where email='"+email+"'")
    n=cur.rowcount
    name="no"
    if n>0:
        row=cur.fetchone()
        name=row[0]
    return name

def get_doctors(email):
    cur = make_connection()
    cur.execute("SELECT * FROM drdata where email_of_hospital='"+email+"'")
    data=cur.fetchall()
    return data
