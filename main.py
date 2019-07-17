from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import pymysql, myFunctions
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/currency_db'
db = SQLAlchemy(app)

class CurrencyForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valyuta = db.Column(db.String(80))
    kod = db.Column(db.String(10))
    kurs = db.Column(db.Float)
    ferq = db.Column(db.Integer)

    def __repr__(self):
        return '<Currency %r>' % self.valyuta

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/currency', methods = ['GET', 'POST'])
def currency():
    today = date.today().strftime("%Y-%m-%d")
    if request.method == 'POST':
        date1 = ".".join(request.form.get('date1').split('-')[::-1])
        date2 = ".".join(request.form.get('date2').split('-')[::-1])

        view_list = list()
        date1_list = myFunctions.listFromCbar(date1)
        date2_list = myFunctions.listFromCbar(date2)

        for index, value in enumerate(date2_list):
            valyuta = value[1].text,
            kod = value.attrib['Code'],
            kurs = value[2].text,
            deqiq_ferq = float(value[2].text) - float(date1_list[index][2].text)
            if deqiq_ferq > 0:
                ferq = 2
            elif deqiq_ferq < 0:
                ferq = 1
            else:
                ferq = 0

            old_currency_details = CurrencyForm.query.filter_by(kod = kod).first()
            if old_currency_details:
                 db.session.delete(old_currency_details)
            currency_details = CurrencyForm(valyuta = valyuta, kod = kod, kurs = kurs, ferq = ferq)
            db.session.add(currency_details)
            db.session.commit()

            view_list.append({
                'valyuta' : valyuta[0],
                'kod' : kod[0],
                'kurs' : kurs[0],
                'ferq' : ferq
            })

        return render_template('currency.html', content = {'view_list': view_list, 'today': today})

    elif request.method == 'GET':

        view_list = CurrencyForm.query.all()

        if len(view_list):
            return render_template('currency.html', content = {'view_list': view_list, 'today': today})
        else:
            todayForCbar = date.today().strftime("%d.%m.%Y")
            content = myFunctions.listFromCbar(todayForCbar)

            view_list = [{
                'valyuta': val[1].text,
                'kod': val.attrib['Code'],
                'kurs': val[2].text,
                'ferq': 0
            } for val in content]

        return render_template('currency.html', content = {'view_list': view_list, 'today': today})
        

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)