import pyodbc

# Connect to the SQLite database
conn = pyodbc.connect('DRIVER={SQLite3 ODBC Driver};DATABASE=bloodlink.db;')

# Create a cursor object
cursor = conn.cursor()

# List of SQL queries for table creation
table_creation_queries = [
    # Admin Table
    """
    CREATE TABLE IF NOT EXISTS admin (
        AdminID INTEGER PRIMARY KEY,
        Username VARCHAR(50) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        Email VARCHAR(100) UNIQUE NOT NULL
    )
    """,
    # Users Table
    """
    CREATE TABLE IF NOT EXISTS users (
        UserID INTEGER PRIMARY KEY,
        Username VARCHAR(50) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        Email VARCHAR(100) UNIQUE NOT NULL,
        UserType VARCHAR(20) NOT NULL,
        RegistrationDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
    # Donors Table
    """
    CREATE TABLE IF NOT EXISTS donors (
        DonorID INTEGER PRIMARY KEY,
        UserID INTEGER NOT NULL,
        BloodGroup VARCHAR(5) NOT NULL,
        LastDonationDate DATE,
        ContactNumber VARCHAR(15),
        Address VARCHAR(255),
        FOREIGN KEY (UserID) REFERENCES users(UserID)
    )
    """,
    # Donations Table
    """
    CREATE TABLE IF NOT EXISTS donations (
        donation_id INTEGER PRIMARY KEY,
        donor_id INTEGER NOT NULL,
        blood_type VARCHAR(5) NOT NULL,
        quantity INTEGER NOT NULL,
        donation_date DATE NOT NULL,
        FOREIGN KEY (donor_id) REFERENCES donors(DonorID)
    )
    """,
    # Appointments Table
    """
    CREATE TABLE IF NOT EXISTS appointments (
        appoint_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        appoint_date DATE NOT NULL,
        bank VARCHAR NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(UserID)
    )
    """,
    # Recipients Table
    """
    CREATE TABLE IF NOT EXISTS recipients (
        RecipientID INTEGER PRIMARY KEY,
        UserID INTEGER NOT NULL,
        BloodGroup VARCHAR(5) NOT NULL,
        MedicalHistory TEXT,
        ContactNumber VARCHAR(15),
        Address VARCHAR(255),
        RequestStatus BOOLEAN NOT NULL,
        FOREIGN KEY (UserID) REFERENCES users(UserID)
    )
    """,
    # Blood Banks Table
    """
    CREATE TABLE IF NOT EXISTS blood_banks (
        BloodBankID INTEGER PRIMARY KEY,
        Name VARCHAR(100) NOT NULL,
        Location VARCHAR(100) NOT NULL,
        ContactNumber VARCHAR(20) NOT NULL,
        InventoryID INTEGER,
        FOREIGN KEY (InventoryID) REFERENCES blood_inventory(InventoryID)
    )
    """,
    # Blood Inventory Table
    """
    CREATE TABLE IF NOT EXISTS blood_inventory (
        InventoryID INTEGER PRIMARY KEY,
        BloodBankID INTEGER,
        BloodType VARCHAR(5) NOT NULL,
        Quantity INTEGER NOT NULL,
        DonationDate DATE NOT NULL,
        ExpirationDate DATE NOT NULL,
        FOREIGN KEY (BloodBankID) REFERENCES blood_banks(BloodBankID)
    )
    """
]

# Execute table creation queries
for query in table_creation_queries:
    cursor.execute(query)

# List of SQL queries for data retrieval
data_retrieval_queries = [
    # Query 9
    "SELECT BloodType, SUM(Quantity) AS TotalQuantity FROM blood_inventory GROUP BY BloodType;",
    # Query 10
    "SELECT d.UserID, d.BloodGroup, d.LastDonationDate, u.Username FROM donors d JOIN users u ON d.UserID = u.UserID;",
    # Query 11
    "SELECT r.UserID, r.BloodGroup, r.RequestStatus, u.Username FROM recipients r JOIN users u ON r.UserID = u.UserID;",
    # Query 12
    "SELECT d.donation_id, d.quantity, d.donation_date, d.blood_type, u.Username AS Donor_Username FROM donations d JOIN donors dn ON d.donor_id = dn.DonorID JOIN users u ON dn.UserID = u.UserID;",
    # Query 13
    "SELECT user_id, COUNT(appoint_id) AS TotalAppointments FROM appointments GROUP BY user_id;",
    # Query 14
    "SELECT UserID, Username, BloodGroup, LastDonationDate FROM donors WHERE LastDonationDate <= DATE('now', '-6 months');",
    # Query 15
    "SELECT BloodBankID, Name, Location, MAX(Quantity) AS HighestQuantity FROM blood_banks JOIN blood_inventory ON blood_banks.InventoryID = blood_inventory.InventoryID;",
    # Query 16
    "SELECT DISTINCT user_id, u.Username FROM appointments a JOIN users u ON a.user_id = u.UserID;",
    # Query 17
    "SELECT BloodType, SUM(Quantity) AS TotalQuantity FROM blood_inventory WHERE BloodBankID = [BloodBankID] GROUP BY BloodType;",
    # Query 18
    "SELECT Name, Location FROM blood_banks ORDER BY Location;",
    # Query 19
    "SELECT u.Username, r.Address FROM recipients r JOIN users u ON r.UserID = u.UserID;",
    # Query 20
    "SELECT u.Username, d.BloodGroup FROM donors d JOIN users u ON d.UserID = u.UserID;",
    # Query 21
    "SELECT d.UserID, d.BloodGroup, COUNT(*) AS DonationCount FROM donations d GROUP BY d.UserID HAVING COUNT(*) > 5;",
    # Query 22
    "SELECT r.UserID, r.BloodGroup, u.Username FROM recipients r JOIN users u ON r.UserID = u.UserID WHERE RequestStatus = False;"
    # Query 23
]

# Execute data retrieval queries
for query in data_retrieval_queries:
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)



complex_queries=[
    #query 1 - 	Retrieve Admins and Their Corresponding Blood Bank Inventory:
    """
    SELECT * 
    FROM Admin 
    JOIN BloodBank ON BloodInventory.BloodBankID = BloodBank.BloodBankID 
    JOIN BloodInventory ON BloodBank.BloodBankID = BloodInventory.BloodBankID;
    """

#query 2 - 	Get Blood Inventory Details with Donor Information and Recipient Requests:
    """
    SELECT Donor.Name, BloodBank.Name
    FROM BloodInventory 
    LEFT JOIN Donor ON BloodInventory.BloodBankID = Donor.UserID 
    JOIN Recipient ON BloodInventory.BloodBankID = Recipient.UserID;
    """

#query 3 - Fetch Recipient Information, Their Appointments, and Blood Bank Locations:

    """
    SELECT Recipient.RecipientID, Recipient.BloodTypeRequested, 
    Recipient.BloodQuantity, Recipient.request_date
    FROM Recipient
    LEFT JOIN Appointments ON Recipient.UserID = Appointments.user_id
    LEFT JOIN BloodBank ON Appointments.bank = BloodBank.Name;
    """

#query 4 - 	Retrieve Donor Information and Their Donation History along with Blood Bank Details:
    """
    SELECT Donor.donor_id , Donations.blood_type
    Donations.quantity, Donations.donation_date, BloodBank.BloodBankName
    FROM Donor
    LEFT JOIN Donations ON Donor.DonorID = Donations.donor_id
    RIGHT JOIN BloodBank ON Donations.blood_bank_id = BloodBank.BloodBankID;
    """
]
#execute complex queries
for query in complex_queries:
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print()
# Close the cursor and connection
cursor.close()
conn.close()





