from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import datetime
# Passwords module.
from passwordhelper import PasswordHelper
# Import for login management
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import LoginManager
from flask.ext.login import current_user
from flask.ext.login import login_required
# Import forms.
from forms import LoginForm
from forms import RegistrationForm
from forms import CreateMeasurementForm
# Import our classes.
from user import User
# Hack for local development without database.
import config
if config.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper


DB = DBHelper()
PH = PasswordHelper()

app = Flask(__name__)
login_manager = LoginManager(app)
# We are using this secret key for CSRF
app.secret_key = "KEjD0UYZ/1YeciecjTW/m7qwczhQRVu7Zz9Iu0EaRAPn9uuWEuKz+VzsjXGplWQ2Dz7ICQRiFFTlqnnIuWCNrDDA3TJ5R9XaZg+T"


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for("account"))
    return render_template("home.html", loginForm=LoginForm(), registrationForm=RegistrationForm())


@app.route('/login', methods=["POST"])
def login():
    login_form = LoginForm(request.form)
    if login_form.validate():
        stored_user = DB.get_user(login_form.loginemail.data)
        if stored_user and PH.validate_password(login_form.loginpassword.data,
                                                stored_user['salt'],
                                                stored_user['hashed']):
            user = User(login_form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('account'))
        login_form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginForm=login_form, registrationForm=RegistrationForm())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# The decorator indicates to Flask-Login that this is the function we want to use
# to handle users who already have a cookie assigned,
# and it'll pass the user_id variable from the cookie to this function whenever a user visits our site,
# which already has one.


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route('/account')
@login_required
def account():
    measurements = DB.get_measurements()
    return render_template("account.html", createMeasurementForm=CreateMeasurementForm(), measurements=measurements)


@app.route('/register', methods=["POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("We already have a user with this email")
            return render_template("home.html", loginForm=LoginForm(), registrationForm=form)
        salt = PH.get_salt()
        hashed = PH.get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        # Debug: We'll print user list:
        # print("User list:")
        # DB.print_users()
        # return redirect(url_for('home'))
        return render_template("home.html",
                               loginForm=LoginForm(),
                               registrationForm=form,
                               onloadMessage="Registration successful. Please log in.")
    return render_template("home.html", loginForm=LoginForm(), registrationForm=form)


@app.route('/account/add_measurement', methods=["POST"])
def account_add_measurement():
    form = CreateMeasurementForm(request.form)
    if form.validate():
        DB.add_measurement(datetime.datetime.now(), form.sys_mmhg.data, form.dia_mmhg.data, form.pul.data)
        return redirect(url_for("account"))
    return render_template("account.html", createMeasurementForm=CreateMeasurementForm())


@app.route('/account/delete_measurement')
@login_required
def account_delete_measurement():
    measurement_id = request.args.get("measurement_id")
    DB.delete_measurement(measurement_id)
    return redirect(url_for('account'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
