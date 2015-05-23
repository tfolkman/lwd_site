from flask import Flask
from flask import send_file
import datetime
from flask import render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

data = pd.read_json("https://data.seattle.gov/resource/3xqu-vnum.json?$limit=50000")

app = Flask(__name__)
app._static_folder = "/Users/tylerfolkman/projects/dashboard/static" 

@app.route("/")
def index(data=data):
    crime_values = data.crime_type.unique()
    v_list = json.dumps(crime_values.tolist())
    v_list = json.loads(v_list)
    return render_template("index.html", v_list=v_list)


@app.route("/test")
def test(data=data):
    data['year'] = data.report_date.str[:4].convert_objects(convert_numeric=True)
    data['month'] = data.report_date.str[5:7].convert_objects(convert_numeric=True)
    data['date'] = data.apply(lambda row: datetime.date(row['year'], row['month'], 1), axis=1)

    total_crimes = pd.pivot_table(data, index='date', columns='crime_type', values='stat_value', aggfunc=np.sum)
    total_crimes.index = pd.to_datetime(total_crimes.index)
    total_crimes.plot()
    plt.savefig('test')

    return send_file('test.png', mimetype='image/gif')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
