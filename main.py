from flask import Flask, render_template
#import requests

app = Flask(__name__)

# main page
@app.route("/")
def index():
    return render_template("index.html")


app.run(debug=True, port=5001)