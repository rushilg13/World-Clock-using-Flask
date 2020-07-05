from flask import Flask, redirect, render_template, url_for, request
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clock.db'
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    clock1=[]
    if request.method=='POST':
        new_city=request.form.get('city')
        if new_city:
            new_city_obj=City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()
    #url='https://www.amdoren.com/api/timezone.php?api_key=HLFE8nDcRSFmzyExDi3kHLwjRQEQAD&loc={}'  
    url='http://api.timezonedb.com/v2.1/get-time-zone?key=92HA2WJ8HPXP&format=json&by=zone&zone=America/{}'
    cities = City.query.all()
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        print(r)
        clock={
            'zoneName':r['zoneName'],
            'Time':r['formatted'],
            'countryName': r['countryName'],
        }
        clock1.append(clock)
    return render_template('clock.html', clock1=clock1)

if __name__=='__main__':
    app.run(debug=True)