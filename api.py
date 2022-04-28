from flask import Flask
from flask import request
from flask import Response
from twilio.rest import Client
import requests
from flask_restful import Api, Resource
import random
import secrets
import cred
import json
import hashlib

app = Flask(__name__)
api=Api(app)

def cowin_otp():
    pass

def otp():
    set = "1234567890"
    otp = ""
    set_ = []

    for _ in set:
        set_.append(_)

    while len(otp) < 4:
        otp += random.choice(set_)
    
    return otp



##### flask routes
@app.route('/')
def root():
    return 'root of api'


@app.route('/test')
def test():
    return ""
    
@app.route('/otp')
def gen_otp():
    
    phone= request.args.get('phone')

    body ={"mobile":phone}
    headers={"accept":"application/json"}
    re = requests.post(url="https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP",headers=headers,json=body)
    if re.status_code == 200:
        print("")
    
    if(re.status_code == 400):
        if("OTP Already Sent" in re.text):
            print("otp already sent wait for 3 mins")
            return "otp already sent wait for 3 mins",400

    print(re.text)
    try:
        data = json.loads(re.text)
        print(data["txnId"])
        data={phone:data["txnId"]}
        data=json.dumps(data,indent=4)
        with open("data.json","w") as f:
            f.write(data)

    except Exception as e:
        print(e)
        return otp

@app.route('/cowin-verify')
def func():
    otp  = request.args.get("otp")
    phone  = request.args.get("phone")
    
    result = hashlib.sha256(otp.encode())
    result = result.hexdigest()

    with open("data.json","r")as f:
        data= json.load(f)


    headers = {
        'accept': 'application/json',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
    }

    json_data = {
        'otp': result,
        'txnId': data[phone],
    }

    response = requests.post('https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP', headers=headers, json=json_data)
    print(response.status_code)

    if(response.status_code ==200):
        print("otp verified")
        return

    if("Beneficiary Not Registered" in response.text):
        print("otp verified")

    print(response.text)
    return Response(status=200)


@app.route('/otp-verify')
def verify():
    phone= request.args.get('phone')
    otp = request.args.get("otp")
    with open("data.json","r") as f:
        json_data = json.load(f)
    if(otp == json_data["phone"]):
        return "OK",200
    else:
        return "Error",400
#txnId = secrets.token_hex(10)

@app.route('/get-otp')
def send_otp():
    phone= request.args.get('phone')

    account_sid = cred.twilio_sid
    auth_token = cred.twilio_auth_token
    client = Client(account_sid, auth_token)
    actual_otp = otp()
    phone = f"+91{phone}"

    message = client.messages.create(
            body=actual_otp,
            from_='+18542012736',
            to=phone
        )
    
    data ={phone:otp}

    json_data = json.dumps(data,indent=4)
    
    with open("data.json","w") as file:
        file.write(json_data)

    print(message.body)
    print(message.sid)
    
    
    
app.run(host="0.0.0.0",port=80)