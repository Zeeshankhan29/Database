from flask import Flask, request,jsonify,render_template
import mysql.connector as conn
import pymongo as py
import pandas as pd


app = Flask(__name__)

@app.route('/xyz',methods=['POST'])
def test2():
    return 'this is the test2 function with get methods specified'



@app.route('/xxyyzz')
def test3():
   # if request.method =='GET':
    a=request.json['num1']
    b=request.json['num2']
    result = a+b
    return jsonify(result)

@app.route('/calculator',methods=['GET','POST'])
def cal():
    if request.method=='POST':
        a = request.json['num1']
        b = request.json['num2']
        operation = request.json['operation']
        if operation == 'Add':
            result = a + b
            res = 'the sum of '+ str(a)+ ' & ' + str(b)+ ' is ' + str(result)
        elif operation == 'Sub':
            result = a - b
            res = 'the difference of '+ str(a)  + ' & '+ str(b)+ ' is ' + str(result)
        elif operation == 'Div':
            result = a / b
            res = 'the Division of ' + str(a)+ ' & '  + str(b) + ' is ' + str(result)
        elif operation == 'Mul':
            result = a * b
            res = 'the Division of ' + str(a)+ ' & '  + str(b) + ' is ' + str(result)

        return jsonify(res)

@app.route('/fetch',methods=['GET','POST'])
def mysql():
    mydb = conn.connect(host='localhost', user='root', passwd='snzk@#1329')
    cursor = mydb.cursor(dictionary=True)
    #cursor.execute('show databases')
    cursor.execute('use dress_data')
    #cursor.execute('show tables')
    cursor.execute('select * from dress1')
    result =cursor.fetchall()
    return jsonify(result)



@app.route('/calloncondition',methods=['GET','POST'])
def mysql3():
    a = request.args.get('value')
    mydb = conn.connect(host='localhost', user='root', passwd='snzk@#1329')
    cursor = mydb.cursor()
    cursor.execute('use dress_data')
    cursor.execute('select * from dress1 where Price = (%s)',(a,))
    result =cursor.fetchall()
    return jsonify(result)

@app.route('/mysqlpostman',methods=['GET','POST'])
def mysql2():
    if request.method == 'POST':
        a = request.json['std']
        b = str(request.json['last_name'])
        c = str(request.json['first_name'])
        try:
            mydb = conn.connect(host='localhost', user='root', passwd='snzk@#1329')
            cursor = mydb.cursor()
            cursor.execute('use dress_data')
            cursor.execute('create table khan(std int , last_name varchar(20),first_name varchar(20))')
        except:
            mydb = conn.connect(host='localhost', user='root', passwd='snzk@#1329')
            cursor = mydb.cursor()
            cursor.execute('use dress_data')
            cursor.execute('insert into khan values (%s,%s,%s)',(a,b,c,))
            mydb.commit()
            cursor.execute('select * from khan')
            result =cursor.fetchall()
            return jsonify(result)


@app.route('/',methods=['GET','POST'])
def web22():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/mysqlhtml',methods=['GET','POST'])
def web():
    if request.method == 'POST':
        a=dict(request.form.items())
        a1 = a['Employee_id']
        b1 = a['First_name']
        c1 = a['Last_name']
        d1 = a['Email_id']
        f1=  a['Salary']
        try:
            mydb = conn.connect(host='localhost', user='root', passwd='snzk@#1329')
            cursor = mydb.cursor()
            cursor.execute('use dress_data')
            cursor.execute('create table Employee_details1(Employee_id int , First_name varchar(50),Last_name varchar(50),Email_id varchar(50) ,Salary int)')
            mydb.close()
        except:
            mydb = conn.connect(host='localhost', user='root', passwd='snzk@#1329')
            cursor = mydb.cursor()
            cursor.execute('use dress_data')
            cursor.execute(f'insert into Employee_details1 values({a1},"{b1}","{c1}","{d1}",{f1})')
            mydb.commit()
            df=pd.read_sql('select * from Employee_details1',mydb)
            column_name=df.columns
            data=[[df.loc[i,col] for col in df.columns] for i in range(len(df))]
            return render_template('result.html',columns =column_name,data1=data)



@app.route('/mongodb',methods=['GET','POST'])
def mong():
    if request.method == 'GET':
        l=[]
        key1=request.json['key1']
        value1=request.json['value1']
        key2=request.json['key2']
        value2=request.json['value2']
        client = py.MongoClient("mongodb+srv://mongodb:mongodb@cluster0.gc1mb.mongodb.net/?retryWrites=true&w=majority")
        db = client['sudh1']
        col = db['ineuron1']
        dic=[{key1:value1},{key2:value2}]
        col.insert_many(dic)
    return jsonify('executed completely')



@app.route('/browser',methods=['GET','POST'])
def browser():
    db=request.args.get('database_name')
    table = request.args.get('table_name')
    mydb = conn.connect(host='localhost', user='root', passwd='snzk@#1329',database=db)
    cursor = mydb.cursor(dictionary=True)
    #cursor.execute('use {}'.format(db))
    cursor.execute('select * from {}'.format(table))
    res = cursor.fetchall()
    return jsonify(res)

@app.route('/br',methods=['GET','POST'])
def ch():
    a=request.args.get('name')
    b=request.args.get('mobile')
    c= request.args.get('email')
    return 'this is the check of {} and mobile number {} and my {}'.format(a,b,c)


@app.route('/tester')
def rider():
    search=request.args.get('search')
    No=request.args.get('No_of_pages')
    return jsonify('https://www.flipkart.com/search?q={}&page={}'.format(search,No))

if __name__ =='__main__':
    app.run(port=8000)