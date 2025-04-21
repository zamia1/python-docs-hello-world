from werkzeug.security import generate_password_hash, check_password_hash

from pymongo import MongoClient
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

from flask import jsonify, render_template, request, url_for
#, send_file
from flask import Flask, flash, redirect, send_file
import pdb
import mimetypes
import os
import io

import gridfs
import chardet
import magic

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if not logged in


# Configure a secret key for Flask-Login
app.secret_key =os.urandom(50)
#url= "http://python-web-test-softpost-newh.azurewebsites.net/"
#url="http://127.0.0.1:5000/"
FILE_SYSTEM_ROOT =os.getcwd()


client = MongoClient("mongodb+srv://mongodb:mongodb@cluster0.ps5mh8y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Get and Post Route
bflag=True
db = client.dataghotkali
gender=""
age=""
#allghotkali = db.dataghotkalicol
ghotkali_collection = db['ghotali']
users_collection = db['users']


ages="25 years or younger,25-30 years,30-35 years,40-45 years"
agetra=ages.split(',')
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({'username': user_id})
    if user:
        return User(user_id)
    return None

def connectToDb(namesp):
    fs = gridfs.GridFS(db,namesp)
    return db, ghotkali_collection, fs
@app.route('/register', methods=['GET', 'POST'])
def register():
    pdb.set_trace()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if users_collection.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({'username': username, 'password': hashed_password,'email': email})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = users_collection.find_one({'email': email})
        
        if user:
            return render_template('reset_password.html', username=user['username'])
        else:
            flash('Email not found', 'danger')

    return render_template('forgot_password.html')
@app.route('/reset_password', methods=['POST'])
def reset_password():
    username = request.form['username']
    new_password = request.form['password']
    
    hashed_password = generate_password_hash(new_password)
    
    result = users_collection.update_one(
        {'username': username},
        {'$set': {'password': hashed_password}}
    )
    
    if result.modified_count > 0:
        flash('Password updated successfully.', 'success')
    else:
        flash('Error updating password.', 'danger')

    return redirect(url_for('login'))

@app.route('/forgot_username', methods=['GET', 'POST'])
def forgot_username():
    if request.method == 'POST':
        email = request.form['email']
        user = users_collection.find_one({'email': email})
        if user:
            flash(f"Your username is: {user['username']}", 'info')
        else:
            flash("Email not found", 'danger')
    return render_template('forgot_username.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            login_user(User(username))
            flash('Login successful.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/get_file/<namef>/<gender>', methods=['GET','POST'])
@login_required
def get_file(namef=None,gender=None):
    pdb.set_trace()
    global agetra
    if request.method=="POST":
        gender=request.form['gender']
        age=request.form['age']
        db, collectn, fs = connectToDb(gender+age)
        return render_template('get_file.html',url=request.url, names=fs.list(),gender=gender,age=age)
    else:
        if namef is not None:
            db, collectn, fs = connectToDb(gender)    
            file = fs.find_one({'filename': namef})
            if file:
                grid_out = fs.find_one({'filename': namef})
                if grid_out:
                    file_data = io.BytesIO(grid_out.read())
                    #return send_file(file_data, mimetype='application/pdf', download_name=namef)
               
                    mimetype, _ = mimetypes.guess_type(namef)
                    print(mimetype)
                    if not mimetype:
                        if namef.endswith(('.jpg', '.jpeg')):
                            mimetype = 'image/jpeg'
                        elif namef.endswith('.png'):
                            mimetype = 'image/png'
                        elif namef.endswith('.gif'):
                            mimetype = 'image/gif'
                        elif namef.endswith('.pdf'):
                            mimetype = 'application/pdf'
                        else:
                            mimetype = 'application/octet-stream'
                    return send_file(file_data, mimetype=mimetype, download_name=namef)
                
            
            else:
                return "File not found", 404


    return render_template('filter.html')
@app.route('/delete_file', methods=['POST','GET'])
@login_required
def delete_file():
    global agetra
    global db

    if request.method=="POST":
        files=request.form.getlist('files[]')
        for file in files:
            rs=file.split(',')
            gender=rs[0][0:4]
            age=rs[0][4:len(rs[0])]
            db, collectn, fs = connectToDb(gender+age)
            for x in fs.find({'filename':rs[1] }).distinct('_id'):
                fs.delete(x)
                print('file' +rs[1] +'is deleted')

        return jsonify({'message': 'file is deleted'}), 201
    else:
        agel=["boys","girl"]


        rs=[]
        files_a={}
        for i in agel:
            for j in agetra:
                rs.append(i+j)
        for i in rs:

            # pdb.set_trace()
            fs = gridfs.GridFS(db,i)

            if len(fs.list())>0:
                gender=i[0:4]
                age=i[4:len(i)]
                files_a[i]=fs.list()
        # pdb.set_trace()        
        return render_template('delete_file.html', names=files_a)


    return render_template('filter.html')
@app.route('/list_file',methods=['GET'])
@login_required
def list_file():
    global db
    # pdb.set_trace()
    global agetra
    agel=["boys","girl"]
    rs=[]
    files_a={}
    for i in agel:
        for j in agetra:

            rs.append(i+j)
    for i in rs:

    #    pdb.set_trace()
        fs = gridfs.GridFS(db,i)

        if len(fs.list())>0:
           # pdb.set_trace()
            gender=i[0:4]
            age=i[4:len(i)]
            files_a[i]=fs.list()
         
    return render_template('get_file_all.html', names=files_a)

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET','POST'])
@login_required
def upload():

    if request.method == "POST":
        names=request.form['names']
        age=request.form['age']

        files = request.files.getlist("file[]")
        for file in files:
            if file.filename == '':
                msg = "No selected file"
                return render_template('upload.html', msgs=msg)
            file_bytes = file.read(2048)  # Read a chunk of the file
            mime_type = magic.from_buffer(file_bytes, mime=True)
            file.seek(0)  # Reset file pointer so fs.put() reads the full file




            if mime_type == 'application/pdf':
                db, collectn, fs = connectToDb(names + age)
                file_id = fs.put(file, filename=file.filename)
            elif mime_type and mime_type.startswith('image/'):
                db, collectn, fs = connectToDb(names + age)
                file_id = fs.put(file, filename=(file.filename ), content_type=mime_type)

              
            else:
                return render_template('upload.html', msgs='Only PDF or image files are allowed')


        return render_template('upload.html',msgs='file is uploaded')

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()