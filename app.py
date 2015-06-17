from flask import Flask
from flask import send_file
from flask import render_template
from flask import request
from flask import send_from_directory
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resources/")
def resources():
    return render_template("resources.html")

@app.route("/nfl_historical_rankings/", methods=['GET', 'POST'])
def nfl_historical_rankings():
	import psycopg2

	conn=psycopg2.connect("dbname=nfl_football user=deploy")    
	cur = conn.cursor()
	cur.execute("""select distinct team from off_regseason_gamestats order by team;""")
	teamNames = cur.fetchall()
	teamNamesList = []
	for name in teamNames:
		teamNamesList.append(name[0])

	if request.method == 'POST':
		name=request.form['team']
	else:
		name="San Francisco 49ers"

	offRankCmd = "select rk, year from off_regseason_gamestats where team like (%s) order by year;"
	cur.execute(offRankCmd, (name, ))
	offRankRows = cur.fetchall()
	offRankList = []
	yearList = []
	for row in offRankRows:
		offRankList.append(row[0])
		yearList.append(row[1])
	defRankCmd = "select rk from def_rev_regseason_gamestats where team like (%s) order by year;"
	cur.execute(defRankCmd, (name, ))
	defRankRows = cur.fetchall()
	defRankList = []
	for row in defRankRows:
		defRankList.append(row[0])

	return render_template("historical_nfl_rankings.html", team_names=teamNamesList, name=name, o_data_years=yearList, o_data_rk=offRankList, d_data_rk=defRankList)

@app.errorhandler(404)
def error_handler(error):
    app.logger.warning(error)

@app.errorhandler(500)
def error_handler(error):
    app.logger.warning(error)

@app.route('/robots.txt')
def static_from_root():
	    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == "__main__":
	handler = RotatingFileHandler('./logs/flask/lwd.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter( "%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
	handler.setFormatter(formatter)
	app.logger.addHandler(handler)
	app.logger.setLevel(logging.DEBUG)
	app.run()
