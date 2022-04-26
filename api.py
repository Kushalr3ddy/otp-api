from flask import Flask
from flask import request
#from flask import jsonify
from twilio.rest import Client
import requests
from flask_restful import Api, Resource
import random
import secrets
import cred
import json

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


account_sid = cred.twilio_sid
auth_token = cred.twilio_auth_token
client = Client(account_sid, auth_token)
actual_otp = otp()
message = client.messages.create(
         body=actual_otp,
         from_='+18542012736',
         to='+919035524447'
     )
print(message.body)
print(message.sid)

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
    
    if(re.status_code == 400):
        if("OTP Already Sent" in re.text):
    print(re.text)
    try:
        data = json.loads(re.text)
        print(data["txnId"])
    except Exception as e:
        print(e)
        return otp

#txnId = secrets.token_hex(10)

app.run()