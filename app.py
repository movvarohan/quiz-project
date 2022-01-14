# *************************************Quiz Web Project*************************************
#****************************************By Rohan Movva*************************************
#*******************************************************************************************


# Imports


# Flask imports
from flask import Flask, render_template, request, session, redirect, url_for, flash
import json
import urllib.request as ur
# Random API to get a random number within a Range.
import random, datetime
# Data object
import Model
from Model import Item
from html import unescape
from flask_login import LoginManager
from forms import loginform, signupform
from bson.objectid import ObjectId
from flask_login import login_user, current_user, logout_user, login_required,UserMixin
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import pymongo
import string
from flask_mail import Mail, Message
# Used to read the questions file.
import configparser

#Define the Flask App
app = Flask(__name__)
#Mongo DB connection info
app.config['MONGO_URI'] = 'mongodb+srv://admin:Rmovva1234$@cluster0.fhaii.mongodb.net/flask?retryWrites=true&w=majority'
app.config['MONGO_DBNAME'] = 'flask'

#Mail server connection details
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rohanquizappinfo@gmail.com'
app.config['MAIL_PASSWORD'] = 'Rmovva1234$'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.secret_key = "SnoopyIsMyDog"
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
mongo = PyMongo(app)
posta = Mail(app)

# This is the main file for the project. It has 9 routes.
# 1. home. This will redirect the user to the start page.
# 2. start. Start displays the first page. In this page, the user can select the category and level.
# 3. nextQn. This page displays the question and 4 options.
# 4. check. This page checks if the user answered the question correct or not. It also displays the score.

#5 login -- This will allow the user to login with a valid username password
#6 logout -- Logs the user out, clears the cookie and session and redirects the user to the home page.
#7 Signup -- Signup using email and password.
#8 Forgot password -- If the user forgot the password, this will allow them to reset the password.
#9 Dashboard -- Shows the previous scores for the user.



cat_mapping = {
    "math": "Math",
    "presidents": "Presidents",
    "govt": "Government",
    "tax": "Taxes",
    "21": "Sports",
    "9": "General Knowledge",
    "22": "Geography",
    "23": "History",
    "24": "Politics",
    "18": "Computers",
    "29": "Comics",
    "12": "Music",
    "27": "Animals",
    "11": "Film",
    "14": "Television",
    "17": "Nature",
    "26": "Celebrities"

}

# Starting page to select the category and level.
# The 2 session values are initialized to 0 to reset the counter.
# Count is to track the number of questions that are asked to the user.
# Score is to track the number of questions the user answered correctly.
@app.route("/start", methods=['POST', 'GET'])
def start():
    # Track the number of questions.
    session["count"] = 0
    # Track the number of correct answers.
    session["score"] = 0
    return render_template('selectCategory.html')


# This page does 2 things. It calls the rest api to get the question and answers for the selected category and
# displays the Question to the user.
@app.route("/nextQn", methods=['POST', 'GET'])
def nextQn():
    # Get the Cateogry and level from the request.
    category = request.form.get('category')
    level = request.form.get('level')
    # If the Math category is selected, generate the questions using the Random numbers.
    # For all other categories, go to the url
    if category == "math":
        operatorNum = random.randint(0, 1)
        correctAnswer = 0
        # Did the user select easy level?
        if level == "easy":
            # Get 2 random numbers.
            num1 = random.randint(1, 1000)
            # Make the second number bigger than the first one.
            num2 = random.randint(num1, 2000)
            # Calculate some incorrect values to display them to the user.
            a = int(num2 - num1 - 1)
            b = int(num2 + num1 + num1)
            c = int(num2 / (num1 + 1))
            d = int(num2 + (num1 - 1))
            # Pick the operator randomly + or - for easy.
            if operatorNum == 0:
                operator = "+"
                correctAnswer = num1 + num2
            elif operatorNum == 1:
                operator = "-"
                correctAnswer = num2 - num1
        # is the level Hard?
        else:
            # get 2 random numbers
            num1 = random.randint(1, 500)
            num2 = random.randint(num1, 1000)

            # Calculate some incorrect values to display them to the user.
            a = int(num2 + num1 + 2)
            b = int(num2 * (num1 + 1))
            c = int(num2 / (num1 + 2))
            d = int(num2 + num1 + 23)
            # Pick the operator randomly * or / for hard.
            if operatorNum == 0:
                operator = "*"
                correctAnswer = num1 * num2
            elif operatorNum == 1:
                operator = "/"
                correctAnswer = num2 / num1

        # Set one of the answers to the correct answer. Pick the option Randomly.
        answerNum = random.randint(0, 3)
        if answerNum == 0:
            a = correctAnswer
            correctInputAnswer = "a"
        elif answerNum == 1:
            b = correctAnswer
            correctInputAnswer = "b"
        elif answerNum == 2:
            c = correctAnswer
            correctInputAnswer = "c"
        elif answerNum == 3:
            d = correctAnswer
            correctInputAnswer = "d"

        # format the question and options.
        question = "What is the value of {} {} {} ?".format(num2, operator, num1)

        # Load all the question information into a class.
        item = Item(question, a, b, c, d, correctAnswer, correctInputAnswer, category, level)
        # Pass the item object to the question.html file to render it on the browser.
        return render_template('question.html', item=item)
    elif category == "presidents" or category == "tax" or  category == "govt" :
        # This method is used to ask presidents or tax or gov category questions.
        # Read the presidents or tax or gov .txt file for all the questions.
        questions = configparser.ConfigParser();
        questions._interpolation = configparser.ExtendedInterpolation();
        maxqns = 10
        if category == "presidents":
            questions.read('./presidents.txt');
            maxqns = 16
        elif category == "tax":
            if level == "easy":
                questions.read('./tax-easy.txt');
            else:
                questions.read('./tax-hard.txt');
            maxqns = 15
        elif category == "govt":
            if level == "easy":
                questions.read('./govt-easy.txt');
            else:
                questions.read('./govt-hard.txt');
            maxqns = 21
        num1 = random.randint(1, maxqns)
        question = unescape(questions.get('questions', 'question_{}'.format(num1)))
        a = unescape(questions.get('questions', 'question_{}_a'.format(num1)))
        b = unescape(questions.get('questions', 'question_{}_b'.format(num1)))
        c = unescape(questions.get('questions', 'question_{}_c'.format(num1)))
        d = unescape(questions.get('questions', 'question_{}_d'.format(num1)))
        correctAnswer = unescape(questions.get('questions', 'question_{}_answer'.format(num1)))
        if correctAnswer == 'a':
            correctInputAns = a
        elif correctAnswer == 'b':
            correctInputAns = b
        elif correctAnswer == 'c':
            correctInputAns = c
        elif correctAnswer == 'd':
            correctInputAns = d

        # Load all the question information into a class.
        item = Item(question, a, b, c, d, correctInputAns, correctAnswer, category, level)
        # Pass the item object to the question.html file to render it on the browser.
        return render_template('question.html', item=item)
    else:
        # build the url with the category and level.
        url = "https://opentdb.com/api.php?amount=1&type=multiple&difficulty={}&category={}".format(str(level), str(category))
        print(url)
        # Read the response and parse the json response.
        html = ur.urlopen(url).read()
        # Load the response into a data array.
        data = json.loads(html.decode('utf-8'))

        # Get the question details from the array.
        question = unescape(data["results"][0]["question"])
        correct = unescape(data["results"][0]["correct_answer"])
        # Pick a random number to select the correct answer randomly between 0 and 3.
        # 0 = Option A, 1 = Option B, 2 = Option C, 3 = Option D
        answerNum = random.randint(0, 3)
        # If random number is 0, make Option A as a correct answer.
        if answerNum == 0:
            incorrect1 = unescape(data["results"][0]["correct_answer"])
            incorrect2 = unescape(data["results"][0]["incorrect_answers"][0])
            incorrect3 = unescape(data["results"][0]["incorrect_answers"][1])
            incorrect4 = unescape(data["results"][0]["incorrect_answers"][2])
            correctOption = "a"
        # If random number is 1, make Option B as a correct answer.
        elif answerNum == 1:
            incorrect1 = unescape(data["results"][0]["incorrect_answers"][0])
            incorrect2 = unescape(data["results"][0]["correct_answer"])
            incorrect3 = unescape(data["results"][0]["incorrect_answers"][1])
            incorrect4 = unescape(data["results"][0]["incorrect_answers"][2])
            correctOption = "b"
        # If random number is 2, make Option C as a correct answer.
        elif answerNum == 2:
            incorrect1 = unescape(data["results"][0]["incorrect_answers"][0])
            incorrect2 = unescape(data["results"][0]["incorrect_answers"][1])
            incorrect3 = unescape(data["results"][0]["correct_answer"])
            incorrect4 = unescape(data["results"][0]["incorrect_answers"][2])
            correctOption = "c"
        # If random number is 3, make Option D as a correct answer.
        elif answerNum == 3:
            incorrect1 = unescape(data["results"][0]["incorrect_answers"][0])
            incorrect2 = unescape(data["results"][0]["incorrect_answers"][1])
            incorrect3 = unescape(data["results"][0]["incorrect_answers"][2])
            incorrect4 = unescape(data["results"][0]["correct_answer"])
            correctOption = "d"
        # Load all the question information into a class.
        item = Item(question, incorrect1, incorrect2, incorrect3, incorrect4, correct, correctOption, category, level)
        # Pass the item object to the question.html file to render it on the browser.
        return render_template('question.html', item=item)


# This method checks if the user selected the correct answer by comparing the user's selection to the correct option.
# It formats the display message based on the correct or wrong answer.
# It also calculates the score with a maximum of 5 questions.
# If the total questions reaches 5, it will hide the next button.
@app.route("/check", methods=['POST', 'GET'])
def check():
    # Get the Correct Answer options from the request.
    correctAnswer = request.form.get('correctAnswer')
    correctOption = request.form.get('correctOption')
    withinTimer = request.form.get('withinTimer')
    # Get the user selected option.
    userOption = request.form.get('q_answer')
    # Get the category and level.
    category = request.form.get('category')
    level = request.form.get('level')
    # Get the scores from the session.
    score = session["score"]
    count = session["count"]
    # Increment the total questions count.
    count = int(count)+1
    # Default the Next button to show.
    hideNextButton = "inline-block"

    # Check if the user answered the question correctly.
    if correctOption == userOption:
        displayMessage = "Correct !! "
        # If the answer is correct, increment the score.
        if withinTimer == 'true':
            score = int(score) + 2
        else:
            score = int(score) + 1
    # If the user answer is incorrect, format the display message to show the correct answer.
    else:
        displayMessage = "Oops Not Correct!! The correct Answer is {}".format(correctAnswer)

    # If the total questions count is 5, display the final score and hide the next button.
    if int(count) == 5:
        scoreMessage = "Final Score is {}".format(score)
        # This is a javascript attribute to hide the button.
        hideNextButton="none"

        # check whether user is logged in or not
        users = mongo.db.users
        db_user = users.find_one({'_id': ObjectId(current_user.get_id())})
        print("here")
        print(db_user)
        if db_user:
            print(db_user['_id'])
            scores = mongo.db.score
            scores.insert_one({
                            'user_id': db_user['_id'],
                            'cat': cat_mapping[category],
                            'level': level,
                            'score': score, 
                            'updated_at': datetime.datetime.utcnow()
                            })
    # If the total questions is less than 5, just display the current score.
    else:
        scoreMessage = "Score is {}".format(score)

    # Put the new score and count values in the session.
    session["count"] = count
    session["score"] = score
    # Pass all the information to the checkAnswer.html page to be rendered.
    return render_template('checkAnswer.html', displayMessage=displayMessage, scoreMessage=scoreMessage, category=category, level=level, hideNextButton=hideNextButton)

# This route shows all the previous scores for that logged in  user.
@app.route("/dashboard" ,methods=['GET', 'POST'])
@login_required
def dashboard():
    #Get the data from the DB.
    users = mongo.db.users
    db_user = users.find_one({'_id': ObjectId(current_user.get_id())})
    if not db_user:
        return redirect(url_for('start'))
    
    scores = mongo.db.score
    result = scores.find({'user_id': ObjectId(current_user.get_id())}).sort('updated_at',pymongo.ASCENDING)[:10]
    return render_template('dashboard.html', result = result)

#If the user is trying to login, check and load the user from the DB.
@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    user_json = users.find_one({'_id': ObjectId(user_id)})
    return User(user_json)


class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    # Overriding get_id is required if you don't have the id property
    # Check the source code for UserMixin for details
    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)

#When the user tries to login.
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    forms = loginform()
    if forms.validate_on_submit():
        users = mongo.db.users
        db_user = users.find_one({'email': request.form['email']})
        print(db_user)
        if db_user and bcrypt.check_password_hash(db_user['password'], request.form['password']):
            loginuser = User(db_user)
            login_user(loginuser, remember=forms.remember.data)
            return redirect(url_for('start'))
    return render_template('login.html', forms=forms)

#When the user forgot the password and tries to reset the password.
# An email will be sent to the user with the link to reset the password.
@app.route("/forgetPassword", methods=['GET', 'POST'])
def forgetPassword():
    forms = loginform()
    if request.method == "POST":
        mail = request.form['mail']
        users = mongo.db.users
        db_user = users.find_one({'email': mail})
        print(db_user)

        if db_user:
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))

            myquery = {'email': mail}
            newvalues = {"$set": {"hashCode": hashCode}}
            users.update_one(myquery, newvalues)

            msg = Message('Confirm Password Change', sender='berat@github.com', recipients=[mail])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n https://rohan-flask.herokuapp.com/changePassword/" + hashCode
            posta.send(msg)
            flash("check Your mail")
        else:
            flash("User not found")
    else:
        pass
    return render_template('forgetPassword.html', forms=forms)

#THis is called when the user clicks on the link in the email to change the password.
@app.route("/changePassword/<string:hashCode>", methods=["GET", "POST"])
def hashcode(hashCode):
    forms = loginform()
    users = mongo.db.users
    db_user = users.find_one({'hashCode': hashCode})
    if db_user:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                hash_pass = bcrypt.generate_password_hash(passw).decode('utf-8')
                myquery = {'hashCode': hashCode}
                newvalues = {"$set": {"hashCode": None, 'password': hash_pass}}
                users.update_one(myquery, newvalues)
                return redirect(url_for('login'))
            else:
                flash('Password Mismatch')
                return render_template('changePassword.html', forms=forms)
        else:
            return render_template('changePassword.html', forms=forms)

    else:
        return render_template('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # users = mongo.db.users
    # db_user = users.find_one({'_id': ObjectId(current_user.get_id())})
    # if 'admin' not in db_user:
    #     return redirect(url_for('home'))
    forms = signupform()
    error = None
    if forms.validate_on_submit():
        users = mongo.db.users
        db_user = users.find_one({'email': request.form['email']})
        if db_user is None:
            hash_pass = bcrypt.generate_password_hash(forms.password.data).decode('utf-8')

            users.insert_one({
                'password': hash_pass,
                'email': request.form['email'],
                'name': request.form['name']
            })
            return redirect(url_for('login'))
        else:
            flash('Email already taken')
            error = "Email already taken"
    return render_template('signUp.html', forms=forms, error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Redirect the user to the start page.
@app.route("/", methods=['POST', 'GET'])
def home():
    return redirect(url_for('start'))

# This is the main method.
if __name__ == '__main__':
    # This secret key is used by Flask to manage unique sessions.
    # app.secret_key = "SnoopyIsMyDog"
    # app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app)
    # Run the app in debug mode on the local machine.
    app.run(debug=True, port=5000)
