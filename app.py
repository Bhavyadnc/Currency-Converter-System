from flask import Flask, render_template, request, redirect, flash, make_response
from datetime import date, datetime
from flask.helpers import flash
from flask.json import jsonify
from flask.sessions import NullSession
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy.orm import backref

app = Flask(__name__)
app.secret_key = "abc"
API_KEY = 'NJD8IW2H09D8VWC6'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///converter1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    hist = db.relationship('History', backref='owner')
    # date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Email %r>' % self.email

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_curr = db.Column(db.String(200), nullable=False)
    to_curr = db.Column(db.String(500), nullable=False)
    date_conv = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<From_curr %r>' % self.from_curr


@app.route("/", methods=["GET","POST"])
def login():
    if "currUser" not in request.cookies:
        if request.method == 'POST':
            emailLogin = request.form["email"]
            passwordLogin = request.form["password"]
            user = User.query.filter_by(email=emailLogin).first()

            if user == None:    
                new_user = User(email=request.form["email"], password=request.form["password"])
                db.session.add(new_user)
                db.session.commit()

                resp = make_response(redirect("/converter"))  
                resp.set_cookie('currUser',str(new_user.id))  
                return resp

            else:
                if user.password == passwordLogin:
                    resp = make_response(redirect("/converter"))  
                    resp.set_cookie('currUser',str(user.id))  
                    return resp
                else:
                    flash("Wrong Password",category="warning")
                    return render_template("index.html", isHidden="")

        return render_template("index.html", isHidden="isHidden")
    else:
        return redirect("/converter")
 
@app.route('/converter', methods=['GET', 'POST'])
def converter():
    if "currUser" in request.cookies:
        if request.method == 'POST':
            try:
                amount = request.form['amount']
                amount = float(amount)
                from_c = request.form['from_c']
                to_c = request.form['to_c']
                # 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=demo'
                url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey={}'.format(
                    from_c, to_c, API_KEY)
                response = requests.get(url=url).json()
                rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
                rate = float(rate)
                result = rate * amount
                from_c_code = response['Realtime Currency Exchange Rate']['1. From_Currency Code']
                from_c_name = response['Realtime Currency Exchange Rate']['2. From_Currency Name']
                to_c_code = response['Realtime Currency Exchange Rate']['3. To_Currency Code']
                to_c_name = response['Realtime Currency Exchange Rate']['4. To_Currency Name']
                time = response['Realtime Currency Exchange Rate']['6. Last Refreshed']

                userId = request.cookies.get('currUser')
                user = User.query.filter_by(id=userId).first()
                item = History(from_curr=from_c_code,to_curr=to_c_code,date_conv=time, amount=rate, owner=user)
                db.session.add(item)
                db.session.commit()
                
                return render_template('converter.html', result=round(result, 2), amount=amount,
                                    from_c_code=from_c_code, from_c_name=from_c_name,
                                    to_c_code=to_c_code, to_c_name=to_c_name, time=time)
            except Exception as e:
                return '<h1>Bad Request : {}</h1>'.format(e)

        else:
            return render_template('converter.html')
    else:
        return redirect("/")


@app.route("/history")
def history():
    if "currUser" in request.cookies:
        userId = request.cookies.get("currUser")
        user = User.query.filter_by(id=userId).first()
        allHistory = user.hist

        return render_template("history.html", history=allHistory)
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie('currUser', '', expires=0)
    return resp


if __name__ == "__main__":
    app.run(debug=True)