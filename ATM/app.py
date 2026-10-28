from flask import Flask,render_template,redirect,request,session,url_for
import json
import random
from mail import send_email

app = Flask(__name__)
app.secret_key = 'atm@26'

def generate_otp():
  return str(random.randint(100000,999999))

def get_data():
  with open('data.json','r') as file:  
    return json.load(file)

def save_data(data):
  with open('data.json','w') as file:
    return json.dump(data,file,indent=4)


@app.route('/')
def base():
  return redirect('/login')

@app.route('/login',methods = ['GET','POST'])
def login():
  info = request.args.get('info')
  if request.method == 'POST':
    acc_num = request.form.get('accnum')
    pin = request.form.get('pin')
    data = get_data()
    users = data["users"]
    for i in users:
      if i["accnum"] == acc_num and i["pin"] == pin:
        session["username"] = i["username"]
        session["id"] = i["id"]
        return redirect('/dashboard')
    return redirect(url_for('login',info = "Invalid Login"))
  return render_template('login.html',info = info)

@app.route('/confirmemail',methods=['POST','GET'])
def confirmemail():
  info = request.args.get('info')
  if request.method == 'POST':
    email = request.form.get('email')
    session['email'] = email
    data = get_data()
    users = data["users"]
    for i in users:
      if i["email"] == email:
        otp = generate_otp()
        session['otp']=otp
        send_email(email,"OTP Verification",f"Hello {i['username']}, your otp : {otp}")
        return redirect(url_for('verify'))
    return redirect(url_for('confirmemail',info="Email is not linked with bankaccount")) 
  return render_template('confirmemail.html',info=info)


@app.route('/verify',methods=['GET','POST'])
def verify():
  info = request.args.get('info')
  if request.method == 'POST':
    otp = request.form.get('otp')
    if otp == session['otp']:
      session.pop('otp')
      return redirect(url_for('setuppin'))
    return redirect(url_for('verify',info='Invalid OTP'))  
  return render_template('verify.html')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
            return redirect(url_for('login',info="Login Again"))
    
    return render_template('dashboard.html',username=session["username"])

@app.route('/setuppin',methods = ['GET','POST'])
def setuppin():
  info = request.args.get('info')
  if request.method == 'POST':
    pin = request.form.get('pin')
    cpin = request.form.get('cpin')
    if pin == cpin:
      data = get_data()
      users = data["users"]
      for i in users:
        if i["email"] == session["email"]:
          session.pop('email')
          i["pin"] = pin
          save_data(data)
          return redirect(url_for('login', info = 'Pin is updated , Login Again'))
    return redirect(url_for('setuppin',info='confirm the pin properly'))      
  return render_template('setuppin.html',info=info)

@app.route('/deposit',methods = ['GET','POST'])
def deposit():
  if 'id' not in session:
    return redirect(url_for('login',info = "Login Again"))

  info = request.args.get('info')
  if request.method == 'POST':
    amount = int(request.form.get('amount'))
    if amount <= 0:
      return redirect(url_for('deposit',info = 'Amount needs to be greater than zero'))
    data = get_data()
    users = data["users"]
    for i in users:
      if i["id"] == session["id"]:
        i["balance"] += amount
        i["history"].append(f'{amount} - Deposited')
        save_data(data)
        return redirect(url_for('checkbalance'))
  return render_template('deposit.html',info = info)

@app.route('/withdraw',methods = ['GET','POST'])
def withdraw():
  if 'id' not in session:
    return redirect(url_for('login',info = "Login Again"))

  info = request.args.get('info')
  if request.method == 'POST':
    amount = int(request.form.get('amount'))
    data = get_data()
    users = data["users"]
    for i in users:
      if i["id"] == session["id"]:
        if 0 <amount <= i["balance"]:
          i["balance"] -= amount
          i["history"].append(f'{amount} - withdraw')
          save_data(data)
          return redirect(url_for('checkbalance'))
        else:
          return redirect(url_for('withdraw',info = "Amount > 0 or insufficient balance"))
  return render_template('withdraw.html',info=info)

@app.route('/transactions')
def transactions():
    if 'id' not in session:
        return redirect(url_for('login',info='login again'))
    data = get_data()
    users = data["users"]
    for i in users:
        if i["id"] == session["id"]:
            history = i["history"]
            return render_template('transactions.html',history = history)

@app.route('/checkbalance')
def checkbalance():
  if "id" not in session:
    return redirect(url_for('login',info="Login Again"))

  data = get_data()
  users = data["users"]
  for i in users:
    if i["id"] == session["id"]:
      balance = i["balance"]
      return render_template('checkbalance.html',balance = balance)

@app.route('/logout')
def logout():
  session.clear()
  return render_template('login.html')

if __name__ == '__main__':
  app.run(debug = True)