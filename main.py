# Create a web application project “ Hospital Management system “ using python
# Flask with the following web pages and route
#
# 1. Route ( / )  is for the Admin login page . Create a responsive
# web page by using HTML CSS BOOTSTRAP with the following fields in the form .
# Username password and login button . If the username is equals to admin and
# password is equals to 12345 , then redirect to the route /dashboard
#
# 2. Route ( / dashboard)  is for the patient registration page .
# Create a responsive web page by using HTML CSS BOOTSTRAP with the
#     following fields in the form . name , mobile number , age , address  ,
#     date of birth ,place , pincode and register button . Store the data to the SQLite database
#
# 3. Route ( / search )  is for the patient search page . Create a
# responsive web page by using HTML CSS BOOTSTRAP with the following
# fields in the form . Mobile number and search  button . Retrieve
# all the patient data corresponding to the mobile number and display it
#
# 4. Route ( / delete )  is for the patient deletion . Create a
# responsive web page by using HTML CSS BOOTSTRAP with the following
# fields form . Mobile  number and delete  button . Delete the corresponding patient data from database
#
# 5. Route ( / viewall )  is for viewing all the patient page .
# Create a responsive web page by using HTML CSS BOOTSTRAP and display all the patient data in table form
#
# 6. Route ( / update ) . This is for edit the patient data based on the mobile number search
#
# 7.Should need a navigation bar in the dashboard page which contains
# Add patient , search , edit , delete

from flask import Flask, render_template, request, redirect
import sqlite3

con = sqlite3.connect('PatientManagement.db', check_same_thread=False)

cursor = con.cursor()

listOfTables = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='PATIENT'").fetchall()

if listOfTables:
    print("Table Already Exists ! ")
else:
    con.execute(''' CREATE TABLE PATIENT(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT,
                            PHONE TEXT,
                            AGE INTEGER,
                            ADDRESS TEXT,
                            DOB TEXT,
                            PLACE TEXT,
                            PINCODE TEXT ); ''')
    print("Table has created")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        getUsername = request.form["uname"]
        getPswd = request.form["pswd"]

        # print(getUsername)
        # print(getPswd)
        if getUsername == "admin" and getPswd == "12345":
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        getName = request.form["name"]
        getPhone = request.form["mno"]
        getAge = request.form["age"]
        getAddress = request.form["address"]
        getDob = request.form["dob"]
        getPlace = request.form["place"]
        getPincode = request.form["pincode"]

        print(getName)
        print(getPhone)
        print(getAge)
        print(getAddress)
        print(getDob)
        print(getPlace)
        print(getPincode)
        try:
            data = (getName, getPhone, getAge, getAddress, getDob, getPlace, getPincode)
            insert_query = '''INSERT INTO PATIENT(NAME,PHONE,AGE,ADDRESS,DOB,PLACE,PINCODE) 
                                VALUES (?,?,?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            con.commit()
            print("Patients Data added successfully")
            return redirect("/view")

        except Exception as e:
            print(e)

    return render_template("register.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        getPhone = request.form["mno"]
        print(getPhone)
        try:
            cursor.execute("SELECT * FROM PATIENT WHERE PHONE = " + getPhone)
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Phone number")
            else:
                print(len(result))
                return render_template("search.html", patient=result, status=True)
        except Exception as e:
            print(e)

    return render_template("search.html", patient=[])


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        getPhone = request.form["phone"]
        print(getPhone)
        try:
            con.execute("DELETE FROM PATIENT WHERE PHONE=" + getPhone)
            print("SUCCESSFULLY DELETED!")
            con.commit()
            return redirect("/view")
        except Exception as e:
            print(e)
    return render_template("delete.html")


@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        getPhone = request.form["phone"]
        print(getPhone)
        try:
            cursor.execute("SELECT * FROM PATIENT WHERE PHONE=" + getPhone)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            if len(result) == 0:
                print("Invalid PHONE number")
            else:
                print(len(result))
            return render_template("update.html", patients=result, status=True)

        except Exception as e:
            print(e)

    return render_template("update.html")


@app.route("/viewupdate", methods=['GET', 'POST'])
def viewupdate():
    if request.method == "POST":
        getName = request.form["name"]
        getPhone = request.form["mno"]
        getAge = request.form["age"]
        getAddress = request.form["address"]
        getDob = request.form["dob"]
        getPlace = request.form["place"]
        getPincode = request.form["pincode"]
    try:
        data = (getName, getAge, getAddress, getDob, getPlace, getPincode, getPhone)
        insert_query = '''UPDATE PATIENT SET NAME = ?,AGE=?,ADDRESS=?,DOB=?,PLACE=?,PINCODE=?
                           where PHONE = ?'''

        cursor.execute(insert_query, data)
        print("SUCCESSFULLY UPDATED!")
        con.commit()
        return redirect("/view")
    except Exception as e:
        print(e)

    return render_template("update.html", patients=result, status=True)


# def update():
#     if request.method == "POST":
#         getMobilno = request.form["mobno"]
#         print(getMobilno)
#         try:
#             curr.execute("SELECT* FROM PATIENTSDETAILS WHERE Mobilenumber=" + getMobilno)
#             print("SUCCESSFULLY SELECTED!")
#             result = curr.fetchall()
#             if len(result) == 0:
#                 print("Invalid Mobile Number")
#             else:
#                 print(result)
#                 return redirect("/viewupdate")
#         except Exception as e:
#             print(e)
#
#     return flask.render_template("update.html")
#
#
# @app.route("/viewupdate", methods=['GET', 'POST'])
# def viewupdate():
#     if request.method == "POST":
#         getName = request.form["Name"]
#         getMobilno = request.form["mobno"]
#         getAge = request.form["age"]
#         getAddress = request.form["addr"]
#         getDob = request.form["DOB"]
#         getPlace = request.form["place"]
#         getPincode = request.form["pincd"]
#
#         print(getName)
#         print(getMobilno)
#         print(getAge)
#         print(getAddress)
#         print(getDob)
#         print(getPlace)
#         print(getPincode)
#         try:
#             query = "UPDATE PATIENTSDETAILS SET Name='" + getName + "',Mobilenumber=" + getMobilno + ",Age=" + getAge + ",Address='" + getAddress + "',Dob=" + getDob + ",Place='" + getPlace + "',Pincode=" + getPincode + " WHERE Mobilenumber=" + getMobilno
#             print(query)
#             curr.execute(query)
#             print("SUCCESFULLY UPDATED!")
#             con.commit()
#             return redirect('/Viewall')
#         except Exception as e:
#             print(e)
#     return flask.render_template("viewupdate.html")
#

@app.route("/view")
def View():
    cursor.execute("SELECT * FROM PATIENT")
    result = cursor.fetchall()
    return render_template("view.html", patients=result)


if __name__ == "__main__":
    app.run(debug=True)
