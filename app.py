from flask import Flask, render_template, url_for, redirect, request, session
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import func
# import flash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'BloodLink_DBMS123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodbank.db'
db = SQLAlchemy(app)

# * ------------- DATABASE MODELS ------------ #

# * --- Admin Table --- #
class Admin(db.Model):
    __tablename__ = 'admin'
    AdminID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<{self.Username} | {self.Password} | {self.Email}>"

# * --- User Table --- #
class User(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    UserType = db.Column(db.String(20), nullable=False) # * Donor/Recipient
    RegistrationDate = db.Column(db.DateTime, nullable=False, default=datetime.now())
    def __repr__(self):
        return f"<{self.Username} | {self.Password} | {self.UserType}>"

# * --- Donors Table --- #
class Donor(db.Model):
    __tablename__ = 'donors'
    DonorID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    BloodGroup = db.Column(db.String(5), nullable=False)
    LastDonationDate = db.Column(db.Date)
    ContactNumber = db.Column(db.String(15))
    Address = db.Column(db.String(255))

    def __repr__(self):
        return f"<{self.UserID} | {self.BloodGroup} | {self.Address}>"

# * --- Donations Table --- #
class Donations(db.Model):
    __tablename__ = 'donations'

    donation_id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.DonorID'),nullable=False)
    blood_type = db.Column(db.String(5),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    donation_date = db.Column(db.Date,nullable=False)

class Appointments(db.Model):
    __tablename__ = 'appointments'

    appoint_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.UserID'),nullable=False)
    appoint_date = db.Column(db.Date,nullable=False)
    bank = db.Column(db.String,nullable=False)

    def __repr__(self):
        return f"<{self.user_id} | {self.bank} | {self.appoint_date}>"

    
with app.app_context():
    db.create_all()
# * --- Recipients Table --- #
class Recipient(db.Model):
    __tablename__ = 'recipients'
    RecipientID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    BloodGroup = db.Column(db.String(5), nullable=False)
    MedicalHistory = db.Column(db.Text)
    ContactNumber = db.Column(db.String(15))
    Address = db.Column(db.String(255))
    RequestStatus = db.Column(db.Boolean, nullable=False) # True:Fulfilled, False:Pending
    def __repr__(self):
        return f"<{self.UserID} | {self.BloodGroup} | {self.Address}>"

# * --- Blood Banks Table --- #
class BloodBank(db.Model):
    __tablename__ = 'blood_banks'

    BloodBankID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Location = db.Column(db.String(100), nullable=False)
    ContactNumber = db.Column(db.String(20), nullable=False)
    InventoryID = db.Column(db.Integer, db.ForeignKey('blood_inventory.InventoryID'))

    def __repr__(self):
        return f'<{self.BloodBankID} | {self.Name} | {self.Location}'

# * --- Blood Inventory Table --- #
class BloodInventory(db.Model):
    __tablename__ = 'blood_inventory'

    InventoryID = db.Column(db.Integer, primary_key=True)
    BloodBankID = db.Column(db.Integer, db.ForeignKey('blood_banks.BloodBankID'))
    BloodType = db.Column(db.String(5), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    DonationDate = db.Column(db.Date, nullable=False)
    ExpirationDate = db.Column(db.Date,nullable=False)
    @classmethod
    def get_total_blood_inventory(cls, blood_bank_id):
        total_blood_inventory = db.session.query(
                cls.BloodType,
                func.sum(cls.Quantity).label('TotalQuantity')
            ).filter_by(BloodBankID=blood_bank_id).group_by(cls.BloodType).all()
            
        return total_blood_inventory

# * -------------------------- APP ROUTES ------------------------ #
    
# * ------------ Check Logged-in ------------ #
def is_logged_in():
    username = None
    if 'logged_in' in session and session['logged_in'] == True:
        username = session['username']
    elif 'admin_logged_in' in session and session['admin_logged_in']==True:
        username = session['admin_username']
    return username

# * ------------ Template App Routes ------------- #
@app.route('/')
def home():
    username = is_logged_in()
    return render_template('home.html',username=username)

@app.route('/findDonors')
def find_donor():
    username = is_logged_in()
    donors = Donor.query.all()
    return render_template('findDonor.html',Donors=donors,username=username)

@app.route('/donateBlood')
def donate():
    username = is_logged_in()
    banks = BloodBank.query.all()
    return render_template('donate.html',username=username,bloodbank=banks)



@app.route('/inventory')
def inventory():
    username = is_logged_in()
    blood_banks = BloodBank.query.all()
    inventory_with_totals = []

    for bank in blood_banks:
        total_inventory = BloodInventory.get_total_blood_inventory(bank.BloodBankID)
        inventory_with_totals.append((bank, total_inventory))

    return render_template('inventory.html', username=username, inventory_with_totals=inventory_with_totals)
   


@app.route('/appointments')
def appoint():
    username = is_logged_in()
    if username is None:
        return render_template('templogin.html',title="Login-Appointments")
    
    CurruserID = User.query.filter_by(Username=username).first().UserID
    print(CurruserID)
    appts = Appointments.query.filter_by(user_id = CurruserID).all()
    print(appts)
    return render_template('appoint.html',appointments=appts,username=username)


#  * --------- APPOINTMENT BOOKING ----------- #
@app.route('/book_appointment/<int:bankid>', methods=["GET","POST"])
def book(bankid):
    username = is_logged_in()
    if username is None:
        return render_template('templogin.html',title="Login-Donations")
    else:
        Person = User.query.filter_by(Username=username).first()
        email = Person.Email
        bloodgroup = Donor.query.filter_by(DonorID=Person.UserID).first().BloodGroup
        bankTuple = BloodBank.query.filter_by(BloodBankID=bankid).first()
        banklocation = bankTuple.Name + ": " + bankTuple.Location
        return render_template('donationform.html',name=username,email=email,
                               blood_group=bloodgroup, 
                               bank = banklocation, username=username)

#  * --------- PROFILE PAGE ----------- #
@app.route('/profile/<username>')
def profile(username):
    currusername = is_logged_in()
    if currusername is None:
        return render_template('templogin.html',title="Login-Profile")
    else:
        found_user = User.query.filter_by(Username=username).first()
        userInfo = None
        if found_user.UserType == 'donor':
            userInfo = Donor.query.filter_by(DonorID=found_user.UserID).first()
        elif found_user.UserType == 'recipient':
            userInfo = Recipient.query.filter_by(RecipientID=found_user.UserID).first()

        return render_template('profile.html',username=currusername,
                               email=found_user.Email,
                               address=userInfo.Address, userType=found_user.UserType)



# * ------- BLOOD DONATION FORM --------- #
@app.route("/submit_donateForm",methods=["POST","GET"])
def donation_form():
    name = request.form.get('name')
    phone = request.form.get('contact_number')
    # medical = request.form.get('allergies_medication')
    amount = request.form.get('blood_amount')
    donation_date_str = request.form.get('date')
    donation_date = datetime.strptime(donation_date_str, r'%Y-%m-%d').date()
    expiration_date = donation_date + timedelta(days=42)
    bloodgroup = request.form.get('blood_group')
    user = User.query.filter_by(Username = name).first()
    donor = Donor.query.filter_by(DonorID = user.UserID).first()
    bank =request.form.get('location')
    bankname = bank.split(':')[0]
    bankId =  BloodBank.query.filter_by(Name=bankname).first().BloodBankID
    with app.app_context():
        donor.ContactNumber = phone
        donor.LastDonationDate = donation_date
        CurrName = Donations.query.filter_by(donor_id = donor.DonorID).first()
        if CurrName is not None:
            ...
        newDonation = Donations(blood_type=bloodgroup, donor_id = donor.DonorID,
                                quantity=amount,donation_date=donation_date)
        newadd = BloodInventory(Quantity=amount,BloodType=bloodgroup,
                                BloodBankID=bankId, DonationDate=donation_date,
                                ExpirationDate=expiration_date)
        newAppoint = Appointments(appoint_date=donation_date,bank=bankname,user_id=user.UserID)
        db.session.add(newAppoint)
        print("---- NEW APPOINTMENT ADDED ----")
        db.session.add(newDonation)
        db.session.add(newadd)
        db.session.commit()
    return render_template('postform.html')

        
        
# * ----------------- Signup  ------------------ #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    user_type = request.form['userType']
    username = request.form['signup-uname']
    password = request.form['signup-pass']
    confirm_password = request.form['confirmPassword']
    blood_group = request.form['bloodGroup']
    email = request.form['email']
    address = request.form['address']
    print("User type:" , user_type)
    if not all([username, password, email]):
        return "Please fill out all fields"
        # flash("Please fill out all fields", "error")
        # return redirect("/signup")
    elif password != confirm_password:
        return "Passwords do not match!"
        # flash("Passwords do not match!","error")
        # return redirect("/signup")
    else:
        new_user = User(Username=username, Password=password, Email=email, UserType=user_type)
        with app.app_context():
           db.session.add(new_user)
           db.session.commit()
           print("------------ Added User! ------------- ")

        newUser = User.query.filter_by(Username=username,Email=email).first()
        if user_type=='donor':
            new_donor = Donor(UserID=newUser.UserID, Address=address, BloodGroup=blood_group)
            with app.app_context():
                db.session.add(new_donor)
                db.session.commit()
                print("---------- Added Donor!---------- ")
        
        elif user_type=='recipient':
            new_recepient = Recipient(UserID=newUser.UserID, Address=address,
                                      BloodGroup=blood_group, RequestStatus=False)
            with app.app_context():
                db.session.add(new_recepient)
                db.session.commit()
                print("----------- Added Recipient! ---------- ")
        return redirect(url_for('home'))


# * -------------- Login ---------------- #
@app.route('/login', methods=['GET', 'POST'])
def login():
    user_type = request.form['signup-userType']
    username = request.form['login-uname']
    password = request.form['login-pass']
    found_user = User.query.filter_by(Username=username).first()
    if not found_user or password != found_user.Password:
        return 'Incorrect Username or password'
        # flash('Incorrect Username or password')
    else:
        print(" ------- Login successful! ------- ")
        session['logged_in'] = True
        session['username'] = username
        return render_template('home.html',username=username)

# * -------------- Admin Login ---------------- #
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
        # return render_template('admin_dash.html')
        return redirect(url_for('admin_dash'))
    else:
        # Authentication failed, redirect back to login page
        return "Incorrect username of password"

# * ----------- ADMIN DASHBOARD ----------- #
@app.route('/admin/dashboard')
def admin_dash():
    if 'admin_logged_in' in session and session['admin_logged_in']:
        return render_template('admin_dash.html')
    else:
        return "Must be logged in as an Admin!"  # Redirect to login if not logged in


# * ------------- LOGOUT ROUTE ---------------- #
@app.route('/logout')
def logout():
    # Clear session variables
    if 'logged_in' in session:
        print("-------  Logged out user ------- ")
        session.pop('logged_in', None)
        session.pop('username', None)
    elif 'admin_logged_in' in session:
        print("-------  Logged out Admin ------- " )
        session.pop('admin_logged_in', None)
        session.pop('admin_username', None)
    return redirect(url_for('home'))




# with app.app_context():
#     db.session.add(admin1)
#     db.session.add(admin2)
#     db.session.commit()
#     db.create_all()

# * -------------- PRINT TABLE FUNCTIONS ------------- #

def print_bloodBanks():
    with app.app_context():
        print('-------- BLOOD BANKS ---------')
        banks = BloodBank.query.filter().all()
        for bank in banks:
            print(bank)

def print_users():
    with app.app_context():
        print('-------- USER DETAILS ---------')
        users = User.query.filter().all()
        for user in users:
            print(user)

def print_donors():
    with app.app_context():
        print('-------- DONOR DETAILS ---------')
        donors = Donor.query.filter().all()
        for donor in donors:
            print(donor)


def print_admins():
    print('-------- ADMIN DETAILS ---------')
    with app.app_context():
        admins = Admin.query.filter().all()
        for admin in admins:
            print(admin)

def print_recipient():
    print('-------- RECIPIENT DETAILS ---------')
    with app.app_context():
        recipients = Recipient.query.filter().all()
        for recipient in recipients:
            print(recipient)

def print_appointments():
    print('-------- APPOINTMENTS ---------')
    with app.app_context():
        appointments = Appointments.query.filter().all()
        for appointment in appointments:
            print(appointment)
    
# print_appointments()
# print_users()
# print_donors()
# print_admins()
# print_recipient()
# print_bloodBanks()
            
# * ------------------------------------------------------------ #
    
if __name__ == '__main__':
    app.run(debug=True,port=5500)


# ! ------------ DO NOT HAMPER ADMIN CREDENTIALS --------- :
# * @admin1 = Admin(Username="Admin1", Password="nimish123", Email="nimish@gmail.com")
# * admin2 = Admin(Username="Admin2", Password="archish123", Email="archish@gmail.com")