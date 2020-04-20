import os

from flask import Flask, session,render_template,request,flash,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash,check_password_hash


app = Flask(__name__)



# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def sign_in():

    return render_template("connection/sign_in.html",title_in="Sign in")

@app.route("/sign_up")
def sign_up():
    return render_template("connection/sign_up.html" ,title_up="Sign up")

@app.route('/success',methods=['POST','GET'])
def success():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(username)
        print(email)
        print(password)
        
        if username == None or email == None or password == None:
            
            render_template('connection/sign_up.html',title="Sign up",message="Veillez renseigner tous les champ")        
        
        # Make sure username exists.
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0:
            return render_template('connection/sign_up.html',title="Sign up",message="Le login est deja utiliser")
        
        #Insert a new user
        db.execute("INSERT INTO users (username, email,password) VALUES (:username, :email, :password)",
                {"username" : username, "email" : email, "password" : generate_password_hash(password) })
       
        db.commit()
        flash('You were successfully registred')
        return redirect(url_for("success"))
    
    return render_template('connection/success.html')



@app.route('/home')
def home():
   return "BIENVENUE DANS LA PAGE DE CONNECTION"