from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'BloodLink_DBMS123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodbank.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/findDonors')
def find_donor():
    return render_template('findDonor.html')

@app.route('/donateBlood')
def donate():
    return render_template('donate.html')
    


def create_db(app, db):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db(app, db)
    app.run(debug=True,port=5500)