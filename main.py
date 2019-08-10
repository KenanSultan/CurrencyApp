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
    ferq = db.Column(db.String(10))

    def __repr__(self):
        return '<Currency %r>' % self.valyuta

class DateForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_date = db.Column(db.String(10))
    second_date = db.Column(db.String(10))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/currency', methods = ['GET', 'POST'])
def currency():
    today = date.today().strftime("%Y-%m-%d")
    if request.method == 'POST':
        first_date = request.form.get('date1')
        second_date = request.form.get('date2')

        old_date_info = DateForm.query.first()
        if old_date_info:
            db.session.delete(old_date_info)
        date_info = DateForm(first_date = first_date, second_date = second_date)
        db.session.add(date_info)
        db.session.commit()
        
        date1 = ".".join(first_date.split('-')[::-1])
        date2 = ".".join(second_date.split('-')[::-1])
        date1_list = myFunctions.listFromCbar(date1)
        date2_list = myFunctions.listFromCbar(date2)
        view_list = list()
        
        for index, value in enumerate(date2_list):
            valyuta = value[1].text
            kod = value.attrib['Code']
            kurs = value[2].text
            deqiq_ferq = float(value[2].text) - float(date1_list[index][2].text)
            if deqiq_ferq > 0:
                ferq = 'arrow-up'
            elif deqiq_ferq < 0:
                ferq = 'arrow-down'
            else:
                ferq = 'dot-circle'

            old_currency_details = CurrencyForm.query.filter_by(kod = kod).first()
            if old_currency_details:
                 db.session.delete(old_currency_details)
            currency_details = CurrencyForm(valyuta = valyuta, kod = kod, kurs = kurs, ferq = ferq)
            db.session.add(currency_details)
            db.session.commit()

            view_list.append({
                'valyuta' : valyuta,
                'kod' : kod,
                'kurs' : kurs,
                'ferq' : ferq
            })

        return render_template('currency.html', content = {'view_list': view_list, 'today': today, 'first_date': first_date, 'second_date': second_date})

    elif request.method == 'GET':

        view_list = CurrencyForm.query.all()
        
        if len(view_list):
            date_info = DateForm.query.first()
            return render_template('currency.html', content = {'view_list': view_list, 'today': today, 'first_date': date_info.first_date, 'second_date': date_info.second_date})
        else:
            todayForCbar = date.today().strftime("%d.%m.%Y")
            content = myFunctions.listFromCbar(todayForCbar)

            view_list = [{
                'valyuta': val[1].text,
                'kod': val.attrib['Code'],
                'kurs': val[2].text,
                'ferq': 0
            } for val in content]

        return render_template('currency.html', content = {'view_list': view_list, 'today': today, 'first_date': today, 'second_date': today})
        

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)