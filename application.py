import os,re

from flask import Flask, session,render_template,request,flash,redirect,url_for,abort
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
        
        if username == "" or email == "" or password == "":
            flash("Veillez renseigner tous les champ")
            return redirect(url_for('sign_up'))       
        
        # Make sure username exists
        
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0:
            flash("Username already use ")
            return redirect(url_for('sign_up'))
        
        #Insert a new user
        db.execute("INSERT INTO users (username, email,password) VALUES (:username, :email, :password)",
                {"username" : username, "email" : email, "password" : generate_password_hash(password) })
       
        db.commit()
        flash('You were successfully registred')
        return redirect(url_for("success"))
    
    return render_template('connection/success.html')



@app.route('/home', methods=['POST','GET'])
def home():
    
    username = request.form['username']
    password = request.form['password']
      
    if not username:
        flash('Username is required.')
        return redirect(url_for('sign_in'))
    elif not password:
        flash('Password is required.')
        return redirect(url_for('sign_in'))
    
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    if check_password_hash(user.password,password):
        books=db.execute('SELECT * FROM books LIMIT 10').fetchall()
        return render_template('page/index.html', title='title', books=books)    
    else:        
        flash("Bad Username or Password ")
        return redirect(url_for('sign_in'))


@app.route('/all/<int:id>')
def all(id):
    page = id
    per_page = 12
    count=db.execute('SELECT * FROM books').rowcount
    pages = count//per_page
    if id > pages :
        abort(404)
    offset = (page-1)*per_page 
    limit = 20 if page == pages else per_page 
    books = db.execute('SELECT * FROM books ORDER BY title LIMIT :limit OFFSET :offset ',{"limit":limit,"offset":offset})
    prev_url = url_for('all', id=page-1) if page > 1 else None
    next_url = url_for('all', id=page+1) if page < pages else None
    tab_prev =dict()
    tab_next =dict()
    tab_prev['previous']=prev_url
    tab_prev['status']= "disabled" if prev_url is None else ""
    tab_next['next']=next_url
    tab_next['status']= "disabled" if next_url is None else ""
    return render_template('page/all.html', books = books, tab_next=tab_next, tab_prev = tab_prev)



@app.route('/my_book')
def my_book():
    pass

@app.route('/logout')
def sign_out():
    return render_template('/connection/sign_in.html')

@app.route('/search', methods=['POST'])
def search():
    text = request.form['text']
    
    isbn_pattern=r'((?P<isb10>^[\d]{10}$)|(?P<isb13>^[\d]{13}$))'
    compiler = re.compile(isbn_pattern)
    result = compiler.match(text)
    if result is not None :
        if result.group('isb10'):
            print(f"==> {text }")
            books = db.execute('SELECT * FROM books WHERE isbn= :text ' ,{'text':text}).fetchone()
            #A changer 
            if books:
                return render_template('page/search.html',books=books)
            else:
                flash('Book not found ')
                redirect(url_for('not_found_book'))
        else:
            pass#will take data from goodreader
    else:
        
        books = db.execute('SELECT * FROM books WHERE title= :text OR author= :text',{'text':text}).fetchall()
        if books:
            return render_template('page/search.html',books=books)
        else:
            text = "%"+text+"%"
            books = db.execute('SELECT * FROM books WHERE title LIKE :text OR isbn LIKE :text OR author LIKE :text',{'text':text}).fetchall()
            if books :
                return render_template('page/search.html',books=books)
            else:
                print(text)
                flash('Book not found')
                return redirect(url_for('not_found_book'))
                
        

@app.route('/search/not_found_book')
def not_found_book():
    
    return render_template('page/not_found_book.html')        






    
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404