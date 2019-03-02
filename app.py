import pyrebase
import random
from firebase import firebase
from flask import *
app = Flask(__name__)
config = {
    "apiKey": "AIzaSyBxRaf5lE-4yER2W2iAPgehRwlxRGCOWgs",
    "authDomain": "flasklogin-11701.firebaseapp.com",
    "databaseURL": "https://flasklogin-11701.firebaseio.com",
    "projectId": "flasklogin-11701",
    "storageBucket": "flasklogin-11701.appspot.com",
    "messagingSenderId": "715568210092"
}

firebase12 = pyrebase.initialize_app(config)

auth = firebase12.auth()

firebase1 = firebase.FirebaseApplication('https://flasklogin-11701.firebaseio.com/', None)

app.secret_key="lawyeriscreat"

db = firebase12.database()


@app.route('/', methods=['GET', 'POST'])
def basic():
    unsuccessful='Please check your credentials'
    successful = 'Login successful'
    c="client"
    l="lawyer"
    if request.method == 'GET':
        return render_template('new.html')
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        typeper=request.form['typeperson']
        if(typeper==c):
            ch=1
        else:
            ch=2
        session['type']=typeper
        #print(type(typeper))
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user']=request.form['name']
            if ch==1:
                todo = db.child("users").get()
                to = todo.val()
                return render_template('client.html',s=successful,t=typeper,username=request.form['name'],results=to.values())
            else:
                todo = db.child("users").get()
                to = todo.val()
                return render_template('lawyer.html',s=successful,t=typeper,username=request.form['name'],results=to.values())
        except:
            return render_template('new.html', us=unsuccessful)
        # if ch==1:
        #     return render_template('client.html', s=successful,t=typeper)
        # else:
        #     return render_template('lawyer.html',s=successful,t=typeper)

@app.route("/signup",methods=['GET','POST'])
def signup1():
    return render_template('signup.html')

@app.route("/firesignup1",methods=['GET','POST'])
def firesignup():
    unsuccessful='email is already exits try login!!'
    successful='Account created!!'
    if request.method == 'POST':
        name= request.form['name']
        email = request.form['email']
        password = request.form['psw']
        try:
            auth.create_user_with_email_and_password(email, password)
            return render_template('new.html', s=successful)
        except:
            return render_template('signup.html', us=unsuccessful)
    return render_template('firebase.html')


@app.route("/firepush",methods=['GET','POST'])
def querypost():
    data=(request.form['data'])
    username=session['user']
    hash = random.getrandbits(8)
    if session['user']=='client':
        try:
            firebase1.post('/users', {'name':username,'article':data,'type':session['type'],'article_id':hash})
        except:
            return render_template('client.html',st="unsuccessful")
    return render_template("client.html",st="success")


if __name__ == '__main__':
	app.run(debug=True)