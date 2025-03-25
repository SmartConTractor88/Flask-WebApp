from flask import Flask, render_template, request

app = Flask(__name__)

# main page
@app.route("/", methods = ["GET","POST"])
def index():
    
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        e_mail = request.form["e_mail"]
        date = request.form["start_date"]
        occupation = request.form["occupation"]
        print(first_name)
        print(last_name)
        print(date)
        print(e_mail)
        print(occupation)
        
        
    return render_template("index.html")


app.run(debug=True, port=5001)