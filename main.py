from random import randint
import sqlite3 as sql
from email.message import EmailMessage
import moviepy.editor as mp
import string,random,smtplib

from cryptocode import encrypt,decrypt
from flask import Flask,render_template, request,make_response,redirect,jsonify

app = Flask(__name__,static_folder="./static")
app.config["UpVd"] = ["./static/Vd"]
def rs(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)

def sandEmail(email,verificationNumber):
        msg = EmailMessage()
        msg.set_content(f"This is your verification code {verificationNumber} \nDo not give it to anyone.\nThe code expires after 15 minutes\n\n\nIf you are not the one who sent this message, ignore it\n\n\n\nThanks\n thistube team")
        msg['Subject'] = 'Your verification code to login to thistube website'
        msg['From'] = "thistube6@gmail.com"
        msg['To'] = email
        server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
        server.login("thistube6@gmail.com","eswwjbszgaprlbif")
        server.send_message(msg)


@app.route("/")
def home():
    con = sql.connect("./thistube.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Videos")
    selectAll = cur.fetchall()
    con.close
    try:
        IdTheUser = decrypt(request.cookies.get("token"),"id")
    except:
           ""
    singup = 'singup'
    if not request.cookies.get("token"):
              return render_template("home.html",login = "login",singupAndLogout=singup,select = selectAll)

    return render_template("home.html",IdTheUser = IdTheUser,singupAndLogout="logout",select = selectAll)


@app.route("/watch=<id>")
def show_Videos(id):
    con = sql.connect("./thistube.db")
    cur = con.cursor()
    cur.execute("""SELECT id,Video,nameVideo,Description FROM Videos WHERE id = ?""",(id,))
    row = [cur.fetchone()]

    if not row:
        return None
    return render_template("view-Video.html",views=row)

@app.route("/singup",methods=(["GET","POST"]))
def singup():
    if not request.cookies.get("tt"):
        token = request.cookies.get("token")

        if not token:

            if request.method == "GET":
                return render_template("singup.html")
            
            elif request.method == "POST":
                con = sql.connect("thistube.db")
                cur = con.cursor()
                email = request.form["email"]
                username = request.form["username"]
                password = request.form["password"]
                device = request.headers.get('User-Agent')
                ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
 
                cur.execute("""SELECT email FROM Users WHERE email = ?""",(str(email),))
                row = cur.fetchall()

                if str(row) == f"[('{email}',)]":
                    return render_template("singup.html",errorEmail="This email or phone number is already in use. Please use another email or phone number")
               
                elif str(row) == "[]":
                            rendem = randint(0,999999)
                            tt = encrypt(f"{rendem}","verify")
                            ee = encrypt(str(email),"verify")
                            uu = encrypt(str(username),"verify")
                            pp = encrypt(str(password),"verify")
                            ii = encrypt(str(ip_addr),"verify")
                            dd = encrypt(str(device),"verify")


                            vl = ('vv','ee',"uu",'pp')
                            resp = make_response(redirect("/singup=verify"))
                            resp.set_cookie("tt",tt,900)
                            resp.set_cookie("ee",ee,900)
                            resp.set_cookie("uu",uu,900)
                            resp.set_cookie("pp",pp,900)
                            resp.set_cookie("ii",ii,900)
                            resp.set_cookie("dd",dd,900)


                            sandEmail(email,rendem)
                            return resp
        
        else:
              return redirect("/")
    
    else:
           return redirect("/singup=verify")
@app.route("/singup=verify",methods=(["GET","POST"]))
def verify():
            if not request.cookies.get("tt"):  
                        return redirect("/singup")  
            
            elif request.method == "POST":
                    verificationNumber = request.form["verificationNumber"]  
            
                    if str(verificationNumber) == decrypt(request.cookies.get("tt"),"verify"):
                            rand = randint(0,9999999999)
                            id = rand
                            email = decrypt(request.cookies.get("ee"),"verify")
                            username = decrypt(request.cookies.get("uu"),"verify")
                            password = decrypt(request.cookies.get("pp"),"verify")
                            device = decrypt(request.cookies.get("pp"),"verify")
                            ip_addr = decrypt(request.cookies.get("ii"),"verify")

                            con = sql.connect("thistube.db")
                            cur = con.cursor()
                            cur.execute("INSERT INTO Users (id,email,username,password) VALUES (?,?,?,?)",(id,email,username,encrypt(password,"OP/kUjA5pXo=*2rY5jLFp8PhprgYRZOyAcg==*z44OSUT63phbdq0f6Qc4nw==*ZsfpsLqEf2YOVp9lAyjoYA==")))
                            cur.execute("INSERT INTO devices (idUser,device,ip_addr) VALUES (?,?,?)",(id,device,ip_addr))

                            con.commit()
                            con.close
                            resp = make_response(redirect("/"))
                            token = str(encrypt(str(id),"id"))
                            resp.set_cookie('token',token)
                            resp.delete_cookie("tt")
                            resp.delete_cookie("ee")
                            resp.delete_cookie("uu")
                            resp.delete_cookie("pp")
                            resp.delete_cookie("ii")
                            return resp
                    return render_template("verificationNumber.html",errorVerificationNumber="The verification number you entered is incorrect. Re-enter it")
            
            elif request.method == "GET":
                      return render_template("verificationNumber.html")

@app.route("/login",methods=(["GET","POST"]))
def login():
        token = request.cookies.get("token")
        mt = request.method
        
        if not token:
        
                if mt == "GET":
                        return render_template("login.html")
        
                elif mt == "POST":
                        con = sql.connect("thistube.db")
                        cur = con.cursor()
                        email = request.form["email"]
                        password = request.form["password"]
                        cur.execute("""SELECT id,password FROM Users WHERE email = ?""",(str(email),))
                        row = [cur.fetchone()]
        
                        try:
        
                                for i in row:
        
                                    if decrypt(str(i[1]),"OP/kUjA5pXo=*2rY5jLFp8PhprgYRZOyAcg==*z44OSUT63phbdq0f6Qc4nw==*ZsfpsLqEf2YOVp9lAyjoYA==") == password:
                                                resp = make_response(redirect("/"))
                                                token = str(encrypt(str(i[0]),"id"))
                                                resp.set_cookie('token',token)
                                                return resp
        
                                    else:
                                                return render_template("login.html",errorEmailOrPassword="Check your email or password")
        
                        except TypeError:
                                  return render_template("login.html",errorEmailOrPassword="Check your email or password")

        
        else:
            return redirect("/")
        



@app.route("/upload_file=<idTheUser>",methods=(["GET","POST"]))
def upload_file(idTheUser):
    if request.method == 'POST':
        con = sql.connect("thistube.db")
        cur = con.cursor()
        rand = randint(0,9999999999)
        f = request.files['video']
        f.save(f"./static/Vd/{rand}.mp4")
        Ph = "None"
        idTheUser = decrypt(request.cookies.get("token"),"id")
        nameVideo = request.form['name-Video']
        Description = request.form['Description']
        clip = mp.VideoFileClip(f"./static/Vd/{rand}.mp4")

        
        if int(len(nameVideo)) >= 41 and int(len(Description)) >= 1500:     
                ErrorDescription = ("You added a video description of 1500 characters!!")
                ErrorNameVideo = ("The name of the video you entered is more than 40 characters!!")
                con.close
                return render_template("upload-file.html",errorNameVideo=ErrorNameVideo,errorDescription=ErrorDescription)
                 
            
        elif int(len(Description)) >= 1500:
                con.close
                return render_template("upload-file.html", errorDescription="You added a video description of 1500 characters!!")

        elif int(len(nameVideo)) <= 4:
                con.close
                return render_template("upload-file.html", errorNameVideo="The name of the video you entered is less than 5 characters!!")
            

        elif int(len(nameVideo)) >= 41:
                con.close
                return render_template("upload-file.html", errorNameVideo="The name of the video you entered is more than 40 characters!!")

        elif int(clip.duration) <= int(60.0):
               print(1)

        else:    
                cur.execute("INSERT INTO Videos (id,Video,photo,nameVideo,Description,IdTheUser) VALUES (?,?,?,?,?,?)",(rand,(f"./static/Vd/{rand}.mp4"),Ph,nameVideo,Description,idTheUser))
                con.commit()
                con.close
                return render_template("upload-file.html", msg="Files has beed uploaded successfully")    
    return render_template("upload-file.html", msg="Please choose a file",idTheUser=idTheUser)
@app.route("/upload_file=",methods=(["GET","POST"]))
def errorLogin():
    return redirect("/login")
@app.route('/logout', methods=["GET"])
def logout():
    r = make_response(redirect('/'))
    r.delete_cookie('token')
    return r

if __name__ == '__main__':
    app.run(debug=True)