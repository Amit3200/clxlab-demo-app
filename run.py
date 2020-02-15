#amit3200 github
import json
import time
import base64
import requests
from cryptography.fernet import Fernet
from datetime import datetime,timedelta
from flask import Flask, render_template, redirect, url_for, request,jsonify,make_response
app = Flask(__name__)
 
#not recommended to give but just for demonstration
KEY="Ht1EaxLc6vijk-QW9VFg206b0JGPIG5vH54yP3-HOKs="

  
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return "hello world"

@app.route("/accounts/signup")
def sign_up_render():
    return render_template("sign_up.html")

@app.route("/accounts/login")
def log_in_render():
    return render_template("log_in.html")

@app.route("/accounts/login/db",methods=["POST"])
def login_check():
    global KEY
    f = Fernet(KEY)
    with open("sampleDB.json","r+") as user_data:
        try:
            db_content=json.load(user_data)
        except:
            db_content=[]
    if request.method=="POST":
        obj_response = request.form
        email=obj_response["email"]
        password=obj_response["password"]
        for ele in db_content:
            if ele["email"]==email and f.decrypt(bytes(ele["password"][2:-1],'utf-8'))==bytes(password,'utf-8'):
                welcome_msg="Hi "+ele["first_name"]+", Welcome Back"
                resp=make_response(render_template("profile.html",msg=welcome_msg))
                resp.set_cookie("login_status","valid")
                resp.set_cookie("username",ele["first_name"])
                time.sleep(2)
                return resp
        error_msg="In-Correct Credentials!"
        return render_template("msg_template_viewer.html",msg=error_msg)
    msg="Error Occured During Logging In"
    return render_template("msg_template_viewer.html",msg=msg)
        
@app.route("/accounts/signup/db",methods=["POST"])
def account_create():
    global KEY
    f = Fernet(KEY)
    with open("sampleDB.json","r+") as user_data:
        try:
            db_content=json.load(user_data)
        except:
            db_content=[]
    if request.method=="POST":
        obj_response = request.form
        person_obj={}
        person_obj["first_name"]=obj_response["fname"]
        person_obj["last_name"]=obj_response["lname"]
        person_obj["password"]=str(f.encrypt(bytes(obj_response["password"],'utf-8')))
        person_obj["email"]=obj_response["email"]
        person_obj["phone"]=obj_response["phone"]
        for ele in db_content:
            if ele["email"]==person_obj["email"] or ele["phone"]==person_obj["phone"]:
                error_msg="User with email or phone number already exists"
                return render_template("msg_template_viewer.html",msg=error_msg)
        db_content.append(person_obj)
        with open("sampleDB.json","w+") as user_data:
            json.dump(db_content,user_data)
        msg="Account Created Successfully!"
        return render_template("msg_template_viewer.html",msg=msg)
    msg="Error Occured During Account Creation"
    return render_template("msg_template_viewer.html",msg=msg)

@app.route("/accounts/logout")
def logout():
    resp = make_response(render_template('index.html'))
    resp.set_cookie("login_status",expires=0)
    return resp

@app.errorhandler(404)
def not_found(e): 
  return render_template("msg_template_viewer.html",msg="404 error! Page Not Found") 