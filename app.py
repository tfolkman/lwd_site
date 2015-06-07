from flask import Flask
from flask import send_file
from flask import render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resources/")
def resources():
    return render_template("resources.html")

@app.route("/nfl/")
def nfl():
    return render_template("historical_nfl_rankings.html")

if __name__ == "__main__":
    app.run(debug=True)
