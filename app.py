# from crypt import methods
from enum import Flag
import json
from sys import flags
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
import jinja2
from bson.objectid import ObjectId
import smtplib
import math, random
import pymongo
# import localStorage
app = Flask(__name__)

# client = pymongo.MongoClient(
#     "mongodb+srv://VP:psi2002@forum.fo2zbdg.mongodb.net/?retryWrites=true&w=majority")
client = pymongo.MongoClient(
    "mongodb+srv://VP:psi2002@forum.fo2zbdg.mongodb.net/test")

db= client.get_database('forum')
data=db['posts']
comments = db['comments']
users = db['users']

currPID = ''
umail = ''
uname = ''
upass = ''
otp = ''
# flag='0'
"""
CREATE TABLE threads(post VARCHAR(500), title VARCHAR(50), id INT, userName VARCHAR(50), userEmail varchar(50), comments varchar(500), postID int);
"""

# comments = {}

def generateOTP() :
 
    # Declare a string variable 
    # which stores all string
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[math.floor(random.random() * length)]
 
    return OTP

# def sendMail():
    

def checkuser(mail):
    if(users.find_one({'email':mail})):
        return True
    else:
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        mail =  request.form.get('email')
        print(mail)
        if(checkuser(mail)):
            passw = request.form.get('upass')
            udata = users.find_one({'email': mail})
            print(udata)
            if(udata):
                if(udata['password'] == passw):
                    dt= data.find()
                    return render_template('home.html', data = dt)
                else:
                    err = 'wrong password'
                    return render_template('login.html', logerr = err)
            else:
                return render_template('login.html', uerr = 'No such email found!')
    return render_template('login.html')

@app.route('/sendMail', methods=['GET', 'POST'])
def sendMail():
    global otp
    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.login("aditya.jaiswal15974@sakec.ac.in", "Aditya@10")
    otp = generateOTP()
    print(otp)
    message = f"{otp}"
    server.sendmail("aditya.jaiswal15974@sakec.ac.in", umail, message)
    # otp = ''
    server.quit()
    return redirect(url_for("verify"))

@app.route('/verify')
def verify():
    global otp
    if request.method=='POST':
        totp =  request.form.get("otp")
        print(totp)
        if(otp == totp):
            # print(otp)
            # print(request.form.get("otp"))
            # print(uname)
            # print(umail)
            # print(upass)
            users.insert_one({
                'name': uname,
                'email': umail,
                'password': upass,
            })
            return redirect(url_for("main"))
        else:
            err = 'Incorrect OTP!'
            return render_template('signup.html', oterr = err)
    return render_template("otp.html", name = uname)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global umail
    global uname
    global upass
    # global flag
    email= request.form.get('umail')
    pass1 = request.form.get('upass')
    pass2 = request.form.get('upass1')
    # flag=localStorage.key('flag');
    # print(flag)
    print(f"email:{email}")
    print(pass1)
    if request.method=='POST':
        if(not checkuser(email)):
            if(pass1==pass2):
                uname = request.form.get('uname')
                umail = email
                upass = pass1
                # users.insert_one({
                #     'name': request.form.get('uname'),
                #     'email': email,
                #     'password': pass1,
                # })
                # dt = data.find()
                # return render_template('home.html', data=dt) #previously working
                return redirect(url_for("sendMail"))
            else:
                wrongpass = 'The password do not match! Please enter again!'
                return render_template('signup.html', perr = wrongpass)
        else:
            exist='User with that email already exists!'
            return render_template('signup.html', exist = exist)
        
    return render_template('signup.html')
    
@app.route('/main')
def main():
    dt = data.find()
    return render_template('home.html', data=dt)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        data.insert_one({
            'title': request.form.get('title1'),
            'desc': request.form.get('post'),
            'pid' : request.form.get('postid'),
            'uid' : request.form.get('uid'),
        })
        dt = data.find()
        return render_template('home.html', data = dt)
    return render_template('create.html')

@app.route('/thread', methods=['GET', 'POST'])
def thread():
    global currPID 
    global comments

    if request.method == 'POST':
        # adding a comment
        cuid = int(request.form.get('id1'))
        # comments[cuid] = request.form.get('comments')
        # data.update_one({'Postid': currPID},
        # {"$set":{
        #     # 'cid' : int(request.form.get('id1')),
        #     # 'userName' : request.form.get('user'),
        #     'comments' : comments,
        # }})
        comments.insert_one({
            'pid' : currPID,
            'cid' : cuid,
            'name' : request.form.get('user'),
            'comment' : request.form.get('comments'),
        })


        dt =  data.find_one({'postid': ObjectId(currPID)})
        comms = comments.find({'pid' : currPID})
        return render_template('thread.html',com=comms, data =  dt)
        
    currPID = request.args.get('connectID')
    # print(currPID)
    dt = data.find_one({'_id': ObjectId(currPID)})
    print(dt)
    comms = comments.find({'pid' : currPID})
    return render_template('thread.html',com=comms, data = dt)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    

    delid  =  request.args.get('conId')
    print(delid)

    comments.delete_one({ '_id': ObjectId(delid) })
    comms = comments.find({'pid' : currPID})
    dt =  data.find_one({'postid': ObjectId(currPID)})
    print(currPID)
    return render_template('thread.html',com = comms, data=dt)

    # comms = comments.find({'pid' : currPID})
    # dt =  data.find_one({'postid': currPID})
    # return render_template('thread.html',com = comms, data=data)

if __name__=="__main__":
    app.run(debug = True)