import os,re,requests

from flask import Flask, session,render_template,request,flash,redirect,url_for,abort,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import timedelta,datetime
from time import strftime

app = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# Configure session to use filesystem
app.secret_key = "MyStrongSecretKey"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#   app.permanent_session_lifetime = timedelta(minutes=5)
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash('Username is required.')
            return redirect(url_for('sign_in'))
        if not password:
            flash('Password is required.')
            return redirect(url_for('sign_in'))
        user = db.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(:username)", {"username": username}).fetchone()
        if not user :
            flash('invalid Username')
            return redirect(url_for('sign_in'))
        if check_password_hash(user.password, password):
            session['id']=user.id
            books=db.execute('SELECT * FROM books WHERE id in (SELECT id FROM reviews ORDER BY rating_scale LIMIT 9 )').fetchall()
            if len(books) < 9:
                books=db.execute('SELECT * FROM books LIMIT 9').fetchall()
            return render_template('page/index.html', title='title', books=books) 
        else:
            flash("Bad Username or Password ")
            return redirect(url_for('sign_in'))
    else:   
        if 'id' in session:
            books=db.execute('SELECT * FROM books WHERE id in (SELECT id FROM reviews ORDER BY rating_scale LIMIT 9 )').fetchall()
            if len(books) < 9:
                books=db.execute('SELECT * FROM books LIMIT 9').fetchall()
            return render_template('page/index.html', title='title', books=books)   
        else:
            flash('Access forbidden Sign in first')
            return redirect(url_for('sign_in'))        




def pagination(page,count):
    pages = count//12        
    prev_url = url_for('all', id=page-1) if page > 1 else None
    next_url = url_for('all', id=page+1) if page < pages else None
    tab_prev =dict()
    tab_next =dict()
    tab_prev['previous']=prev_url
    tab_prev['status']= "disabled" if prev_url is None else ""
    tab_next['next']=next_url
    tab_next['status']= "disabled" if next_url is None else ""
    return (tab_next, tab_prev)

@app.route('/all/<int:id>')
def all(id):
    if 'id' in session:
        page = id
        per_page = 12
        count=db.execute('SELECT * FROM books').rowcount
        pages = count//per_page
        if id > pages :
            abort(404)
        offset = (page-1)*per_page
        limit = 20 if page == pages else per_page
        books = db.execute('SELECT * FROM books ORDER BY title LIMIT :limit OFFSET :offset ',{"limit":limit,"offset":offset})
        paginate = pagination(page,count)
        return render_template('page/all.html', books = books, tab_next=paginate[0], tab_prev = paginate[1])
    else:
        flash('You must be connected to get this page')
        return redirect(url_for('sign_in'))



@app.route('/my_book')
def my_book():
    pass

@app.route('/logout')
def sign_out():
    session.pop('id',None)
    return render_template('/connection/sign_in.html')

@app.route('/search', methods=['POST'])
def search():
    if 'id' in session:
        text = request.form['text']
        isbn_pattern=r'((?P<isb10>^[\d]{10}$)|(?P<isb13>^[\d]{13}$))'
        compiler = re.compile(isbn_pattern)
        result = compiler.match(text)
        books=None
        
        if result is not None :
            if result.group('isb10'):
                books = db.execute('SELECT * FROM books WHERE LOWER(isbn)= LOWER(:text) ' ,{'text':text}).fetchall()

        if not books:
            books = db.execute('SELECT * FROM books WHERE LOWER(title)= LOWER(:text) OR LOWER(author)= LOWER(:text)',{'text':text}).fetchall()
        if not books :
            text = "%"+text+"%"
            books = db.execute('SELECT * FROM books WHERE LOWER(title) LIKE LOWER(:text) OR LOWER(isbn) LIKE LOWER(:text) OR LOWER(author) LIKE LOWER(:text)',{'text':text}).fetchall()
        if not books:
            flash('Book not found')
            return redirect(url_for('not_found_book'))
        else:
            page=1
            count=len(books)
            paginate = pagination(page,count)
            return render_template('page/search.html',books=books,  tab_next=paginate[0], tab_prev = paginate[1])
    else:
        flash('You must be connected to get this page')
        return redirect(url_for('sign_in'))


@app.route('/search/not_found_book')
def not_found_book():
    if 'id' in session:
        return render_template('page/not_found_book.html')
    else:
        flash('You must be connected to get this page')
        return redirect(url_for('sign_in'))


@app.route('/book_view/<string:id>',methods=['POST','GET'])
def book_view(id):
    if "id" in session:
        if request.method == 'POST':
            #text = request.form['text']
            #rating_scale =request.form['rating_scale']
            #db.execute('INSERT INTO reviews(rating_scale, text, id_user,id_book) VALUES (:rating_scale, :text, :id_user, :id_book)',
            #{'rating_scale':rating_scale, 'text':text, 'id_user':session['id'], 'id_book':id})
            #db.commit()
            pass
        book = db.execute('SELECT * FROM books WHERE id=:id',{'id':id}).fetchone()
        posts=db.execute("""SELECT username, text, rating_scale FROM users INNER JOIN reviews ON users.id = reviews.id_user WHERE
        reviews.id_book in (SELECT id from books WHERE id=:id)""",{'id':id}).fetchall();
        #format post for each bo

        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "EGg09TETdsx6k7NS8aheJw", "isbns": book.isbn})
        data = dict()
        if res.status_code != 200:
            data = {'average_rating':"unavailable",'ratings_count':"unavailable"}
        else:
            data = res.json()['books'][0]
        return render_template('/page/book_view.html', data=data, book=book, posts=posts)
    else:
        flash('You must be connected to get this page')
        return redirect(url_for('sign_in'))

# API
@app.route('/api/<isbn>')
def api(isbn):
    book = db.execute('SELECT * FROM books WHERE isbn=:isbn',{'isbn':isbn}).fetchone()
    if not book:
        return jsonify({"error" : "Invalid book_isbn"}),422
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "EGg09TETdsx6k7NS8aheJw", "isbns": book.isbn})
    data = dict()
    if res.status_code != 200:
        data = {'average_rating':"unavailable",'ratings_count':"unavailable"}
    else:
        data = res.json()['books'][0]

    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": data['reviews_count'],
        "average_score": data['average_rating']
    })

@app.errorhandler(404)
def page_not_found(error):
    if 'id' in session:
        return render_template('error/404.html'), 404
    else:
        flash('You must be connected to get this page')
        return redirect(url_for('sign_in'))

@app.route("/review", methods=["POST"])
def posts():
    rate = int(request.form.get("rate") or 2)
    text = request.form.get("text") 
    id_book = request.form.get("id_book")
    if db.execute('SELECT * FROM reviews WHERE id_book=:id_book',{'id_book':id_book}).rowcount > 0:
        data = {'error' : "you can't write two review for one book "}
        return jsonify(data)
    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.execute('INSERT INTO reviews(rating_scale, text, id_user,id_book) VALUES (:rating_scale, :text, :id_user, :id_book)',\
            {'rating_scale':rate, 'text':text, 'id_user':session['id'], 'id_book':id_book})
    db.commit()
    user = db.execute('SELECT user FROM users WHERE id=:id',{'id':session['id']}).fetchone()
    data = {"rate":rate, "text":text, 'user':user,'date':date}
    return jsonify(data)