#Import the Modules:
from flask import Flask,render_template,request,redirect,session
import pymongo
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import date
from decouple import config
# Initializing Flask and Pymongo:
key = config('SENDGRID_API_KEY',default='')
mongo_passkey = config('MONGO_PASSWORD',default='')
sender = config('SENDER_EMAIL',default='')
receiver = config('RECEIVER_EMAIL',default='')
client = pymongo.MongoClient(mongo_passkey)
db = client.VolunteerBuddy
document = {}
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'HELLOTHISISASECRETMESSAGE'
# Creating home route
@app.route("/")
def home_view():
    return render_template('home.html')
# Creating registration page
@app.route("/register",methods =['GET',"POST"])
def registration():
    if request.method=='POST':
        #Setting parameters for the document before entering the dataset
        global document 
        document['First Name'] = request.form['fname']
        document['Last Name'] = request.form['lname']
        document['Email'] = request.form['email']
        document['Password'] = request.form['password']
        session['Full Name'] = request.form['fname']+' '+request.form['lname']
        #Checking the user type and changing the interface accordingly
        if request.form['volunteer']=='1':
            document['Type of User'] = 'Volunteer'
            return redirect('/specialities')
        else:
            document['Type of User'] = 'Elder'
            db.Users.insert_one(document)
            document = {}
    return render_template('register.html')
# Creating login page
@app.route("/login",methods =['GET',"POST"])
def login():
    if request.method=='POST':
        # Filtering the email and password details from the database
        filtered_db = db.Users.find({'Email':request.form['email'],'Password':request.form['password']})
        # Iterating through the cursor
        for iterator in filtered_db:
            # Adding a session
            session['Full Name'] = iterator['First Name']+' '+iterator['Last Name']
    return render_template('login.html')
# Creating Talents page
@app.route("/specialities",methods =['GET',"POST"])
def talents():
    # Modifying the document one last time before adding to the database
    global document
    if request.method=='POST':
        db.Users.insert_one(document)
        return redirect("/help")
    return render_template('talents.html')
# Creating the "add profession" route
@app.route("/add/<talent>",methods =['GET',"POST"])
def add_profession(talent):
    # Adding the talent if the key exists, otherwise creating the list of talents
    global document
    if 'Talents' not in document:
        document['Talents'] = [talent]
    else:
        document['Talents'].append(talent)
    return redirect("/specialities")
# Creating the helping page
@app.route("/help",methods =['GET',"POST"])
def help():
    # Creating a collection list that includes all the documents
    collection=[]
    if request.method=='POST':
        # Filtering the results from the cursor
        cursor = db.Users.find({'Type of User':'Volunteer'})
        # Iterating over the cursor and adding items to the collection
        for item in cursor:
            if request.form['dropdown'] in item['Talents']:
                collection.append(item)
    return render_template('help.html',documents=collection)
# Creating the sending route
@app.route('/send', methods =['GET',"POST"])
def send():
    # Setting mail credentials and main text
    message = Mail(
    from_email=sender,
    to_emails=receiver,
    subject='An elder has requested a booking with you',
    html_content='{} has requested a booking. Please check your portal for more information'.format(session['Full Name']))
    try:
        # Entering the API key and sending the email
        sg = SendGridAPIClient(key)
        response = sg.send(message)
        # If the email doesn't send successfully, then I will print the message
    except Exception as e:
        print(e.message)
    return redirect('/bookings')
# Create the bookings route
@app.route("/bookings",methods =['GET',"POST"])
def bookings():
    # Creating the bookings list
    bookings = []
    # Finding all the elders in the database
    cursor = db.Users.find({'Type of User':'Elder'})
    # Iterating over the cursor
    for items in cursor:
        # We are appending 3 things to the bookings list: 
        # The date of today(when we created a booking), the elder who created the booking, and the time of the booking
        today = date.today()
        bookings.append([today,items['First Name']+' '+items['Last Name'], "5PM-7PM"])
    return render_template('bookings.html',bookings=bookings)
# Running the main code
if __name__=='__main__':
  app.run(debug=True)
