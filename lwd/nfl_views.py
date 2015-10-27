from flask import render_template, request, make_response
from . import app, db
import json
from sqlalchemy import text

@app.route("/nfl_teams/")
def nfl_rankings_data():
    team_names = db.engine.execute("""select distinct team from off_regseason_gamestats order by team;""")
    values = [team[0] for team in team_names]
    return json.dumps(values)


@app.route("/nfl_historical_rankings/", methods=['GET', 'POST'])
def nfl_historical_rankings():

    if request.method == 'POST':
        name = request.form['team']
    else:
        name = "San Francisco 49ers"

    team_names = db.engine.execute("""select distinct team from off_regseason_gamestats order by team;""")
    team_names_list = []
    for team_name in team_names:
        team_names_list.append(team_name[0])

    team_data = db.engine.execute(text("""select o.year, o.rk as off_rk, d.rk as def_rk
                            from off_regseason_gamestats o
                            left join def_rev_regseason_gamestats d
                              on o.year = d.year and o.team = d.team
                            where o.team like :name
                            order by year;"""), {'name': "San Francisco 49ers"})
    off_rank_list = []
    year_list = []
    def_rank_list = []
    for row in team_data:
        off_rank_list.append(row[1])
        year_list.append(row[0])
        def_rank_list.append(row[2])

    return render_template("/nfl/historical_nfl_rankings.html", team_names=team_names_list, name=name,
                           o_data_years=year_list,
                           o_data_rk=off_rank_list,
                           d_data_rk=def_rank_list)
