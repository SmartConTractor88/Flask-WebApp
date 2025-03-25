from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "banana104859820931" # guard application from hackers
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app) # create a database instance

# create a database module

class DataBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    e_mail = db.Column(db.String(80))
    start_date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

# main page
@app.route("/", methods = ["GET","POST"])
def index():
    
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
        flash("Your form was submited successfully.", "success")

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # create a database
    app.run(debug=True, port=5001)
