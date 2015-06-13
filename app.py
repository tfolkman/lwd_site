from flask import Flask
from flask import send_file
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resources/")
def resources():
    return render_template("resources.html")

@app.route("/nfl/", methods=['GET', 'POST'])
def nfl():
	import psycopg2

	try:
	    conn=psycopg2.connect("dbname=nfl_football user=deploy")
	except:
	    print "I am unable to connect to the database."
	    
	cur = conn.cursor()
	try:
	    cur.execute("""select distinct team from off_regseason_gamestats order by team;""")
	    rows = cur.fetchall()
	    names = []
	    for row in rows:
	        names.append(row[0])
	except:
	    print "I can't drop our test database!"

	if request.method == 'POST':
		name=request.form['team']
	else:
		name="San Francisco 49ers"

	cmd = "select rk, year from off_regseason_gamestats where team like (%s) order by year;"
	cur.execute(cmd, (name, ))
	rows = cur.fetchall()
	rk = []
	year = []
	for row in rows:
		rk.append(row[0])
		year.append(row[1])
	cmd = "select rk from def_regseason_gamestats where team like (%s) order by year;"
	cur.execute(cmd, (name, ))
	rows = cur.fetchall()
	d_rk = []
	for row in rows:
		d_rk.append(row[0])

	return render_template("historical_nfl_rankings.html", team_names=names, name=name, o_data_years=year, o_data_rk=rk, d_data_rk=d_rk)

@app.route("/nfl_team/", methods=['GET', 'POST'])
def nfl_team():
	curr_team = request.form['team']
	return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
