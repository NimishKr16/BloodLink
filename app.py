from flask import Flask, render_template, url_for, redirect, request, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BloodLink_DBMS123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodbank.db'
db = SQLAlchemy(app)

# * --------- Database Models --------- #

# --- Admin Table --- #
class Admin(db.Model):
    __tablename__ = 'admin'
    AdminID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<{self.Username} | {self.Password} | {self.Email}>"

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


# * --------- App Routes --------- #
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/findDonors')
def find_donor():
    return render_template('findDonor.html')

@app.route('/donateBlood')
def donate():
    return render_template('donate.html')

# * ----- Signup routes for each user type ------ #
@app.route('/donor/signup', methods=['GET', 'POST'])
def donor_signup():
    ...

@app.route('/recipient/signup', methods=['GET', 'POST'])
def recipient_signup():
    ...


# * ------- Login routes for each user type -------- # 
@app.route('/donor/login', methods=['GET', 'POST'])
def donor_login():
    ...

@app.route('/recipient/login', methods=['GET', 'POST'])
def recipient_login():
    ...

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    admin_username = request.form.get('adminUsername')
    password = request.form.get('adminPassword')
    admin = Admin.query.filter_by(Username=admin_username).first()
    if not admin:
        return "Incorrect username of password"
    if admin and admin.Password == password:
        session['admin_logged_in'] = True
        session['admin_username'] = admin_username
        # Authentication successful
        print("Admin Login Successful!")
        #return render_template('admin_dash.html', username=admin_username)
        return redirect(url_for('admin_dash',admin_username = admin_username))
    else:
        # Authentication failed, redirect back to login page
        return "Incorrect username of password"

# * --- ADMIN DASHBOARD --- #
@app.route('/admin/dashboard/<admin_username>')
def admin_dash(admin_username):
    if 'admin_logged_in' in session and session['admin_logged_in']:
        return render_template('admin_dash.html', username=admin_username)
    else:
        return redirect(url_for('admin_login'))  # Redirect to login if not logged in



# * ---- LOGOUT ROOT ----
@app.route('/logout')
def logout():
    # Clear session variables
    if 'logged_in' in session:
        print("Logged out user")
        session.pop('logged_in', None)
        session.pop('username', None)
    elif 'admin_logged_in' in session:
        print("Logged out Admin")
        session.pop('admin_logged_in', None)
        session.pop('admin_username', None)
    return redirect(url_for('home'))

with app.app_context():
    db.create_all()


# with app.app_context():
#     db.session.add(admin1)
#     db.session.add(admin2)
#     db.session.commit()
#     db.create_all()



def print_admins(app, Admin):
    with app.app_context():
        admins = Admin.query.filter().all()
        for admin in admins:
            print(admin)

if __name__ == '__main__':
    # print_admins(app, Admin)
    app.run(debug=True,port=5500)


# ! ------------ DO NOT HAMPER ADMIN CREDENTIALS --------- :
# * @admin1 = Admin(Username="Admin1", Password="nimish123", Email="nimish@gmail.com")
# * admin2 = Admin(Username="Admin2", Password="archish123", Email="archish@gmail.com")