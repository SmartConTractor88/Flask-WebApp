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

# send email function

def send_email(mail_content):

    msg = Message(
        subject="Portfolio Web App Mail",
        sender=app.config["MAIL_USERNAME"],
        recipients=[app.config["MAIL_USERNAME"]],                      
    )
    msg.body=mail_content 
    mail.send(msg)


# create a database model

class DataBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    message = db.Column(db.String(1000))
    date = db.Column(db.Date)
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


# contact page
@app.route("/contact", methods = ["GET","POST"])
def contact():
    
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        message = request.form["message"]
        date = request.form["date"]
        date_object = datetime.strptime(date, "%Y-%m-%d") # to add to database
        occupation = request.form["occupation"]

        # send an email
        mail_content = message + '\n' + '\n' + \
            first_name + ' ' + last_name + ', ' + occupation + '\n' + \
                'Chosen date:' + date + '\n' + \
                'E-mail:' + ' ' + email
        
        print(mail_content)
        send_email(mail_content=mail_content)
        
        # add data to database
        form = DataBase(first_name=first_name, last_name=last_name, 
                        email=email, message=message, date=date_object, occupation=occupation)
        
        db.session.add(form)
        db.session.commit()

        # respond automatically
        response_text = f"""{first_name}, thank you for your message.
        I will reach out to you asap.
        Regards
        """

        response = Message(subject="Submission Successfull", 
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                           body=response_text)
        
        mail.send(response)

        # flash message of success
        flash("Your e-mail was sent.", "success")

    return render_template("contact.html")


# blog page

@app.route("/blog", methods = ["GET","POST"])
def blog():
    return render_template("blog.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create a database
    app.run(debug=True, port=5001)
