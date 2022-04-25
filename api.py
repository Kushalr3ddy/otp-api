from flask import Flask
from flask import request
from flask import jsonify
from flask_restful import Api, Resource
import random
import secrets

app = Flask(__name__)
api=Api(app)
@app.route('/')
def root():
    return 'root of api'

def otp():
    set = "1234567890"
    otp = ""
    set_ = []

    for _ in set:
        set_.append(_)

    while len(otp) < 4:
        otp += random.choice(set_)
    
    return otp


#txnId = secrets.token_hex(10)
class returnjson(Resource):
    def get(self):
        data={
            "otp": otp(), 
            "txnId":secrets.token_hex(10)
        }
        return data
  
api.add_resource(returnjson,'/otp')

app.run()