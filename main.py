from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "banana104859820931" # guard application from hackers
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "zigmarszigmars19@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("JBN@gmail_APP_PASS_01")

db = SQLAlchemy(app) # create a database instance

mail = Mail(app)

# create a database module

class DataBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    e_mail = db.Column(db.String(80))
    start_date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


# home page
@app.route("/", methods = ["GET","POST"])
def home():
    return render_template("home.html")


# projects page
@app.route("/projects", methods = ["GET","POST"])
def projects():
    return render_template("projects.html")


#art page
@app.route("/art", methods = ["GET","POST"])
def art():
    return render_template("art.html")


# application page
@app.route("/contact", methods = ["GET","POST"])
def contact():
    
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        e_mail = request.form["e_mail"]
        date = request.form["start_date"]
        date_object = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]
        print(first_name)
        print(last_name)
        print(date_object)
        print(e_mail)
        print(occupation)
        
        form = DataBase(first_name=first_name, last_name=last_name, 
                        e_mail=e_mail, start_date=date_object, occupation=occupation)
        
        db.session.add(form)
        db.session.commit()

        message_body = f"""{first_name}, your submission was successful.
        We will reach out to you asap.
        Regards
        """

        message = Message(subject="Submission Successfull", 
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[e_mail],
                           body=message_body)
        
        mail.send(message)

        flash("Your form was submited successfully.", "success")

    return render_template("contact.html")


# blog page

@app.route("/blog", methods = ["GET","POST"])
def blog():
    return render_template("blog.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create a database
    app.run(debug=True, port=5001)
