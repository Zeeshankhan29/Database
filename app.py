from flask import Flask, request,jsonify,render_template
import mysql.connector as conn
import pymongo as py
import pandas as pd


app = Flask(__name__)


@app.route('/xyz',methods=['GET','POST'])
def call():
        return 'this is my call fdkjflkdjflksdkjflksdfunction'


@app.route('/abccc',methods=['GET','POST'])
def call2():
    if request.method =='GET':
        a= request.json['num1']
        b= request.json['num2']
        result = a+b
        return jsonify( result)

@app.route('/calculator',methods =['GET','POST'])
def call3():
    a=request.json['num1']
    b=request.json['num2']
    c=request.json['Operation']
    if c == 'add':
        res =a +b
    elif c =='sub':
        res = a-b
    elif c == 'Mul':
        res = a*b
    return jsonify(res)




if __name__ =='__main__':
    app.run(port =500)