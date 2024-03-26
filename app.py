from flask import Flask, render_template, url_for, redirect, request, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BloodLink_DBMS123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodbank.db'
db = SQLAlchemy(app)

# --------- Database Models --------- #

# --- Admin Table --- #
class Admin(db.Model):
    __tablename__ = 'admin'
    AdminID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)

# --- User Table --- #
class User(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    UserType = db.Column(db.String(20), nullable=False) # Donor/Recipient
    RegistrationDate = db.Column(db.DateTime, nullable=False, default=datetime.now())

# --- Donors Table --- #
class Donor(db.Model):
    __tablename__ = 'donors'
    DonorID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    BloodGroup = db.Column(db.String(5), nullable=False)
    LastDonationDate = db.Column(db.Date)
    ContactNumber = db.Column(db.String(15))
    Address = db.Column(db.String(255))

# --- Recipients Table --- #
class Recipient(db.Model):
    __tablename__ = 'recipients'
    RecipientID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    BloodGroup = db.Column(db.String(5), nullable=False)
    MedicalHistory = db.Column(db.Text)
    ContactNumber = db.Column(db.String(15))
    Address = db.Column(db.String(255))
    RequestStatus = db.Column(db.Boolean, nullable=False) # True:Fulfilled, False:Pending


# --------- App Routes --------- #
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
    # create_db(app, db)
    app.run(debug=True,port=5500)