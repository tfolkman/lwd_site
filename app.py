from flask import Flask
from flask import send_file
from flask import render_template
app = Flask(__name__)
app._static_folder = "/Users/tylerfolkman/projects/dashboard/static" 

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/resources/")
def resources():
    return render_template("resources.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
