from flask import render_template, request
from . import app, db, redis_db
import json
from sqlalchemy import text


@app.route("/nfl_teams/")
def nfl_teams():
    team_names = db.engine.execute("""select distinct team from off_regseason_gamestats order by team;""")
    values = [team[0] for team in team_names]
    return json.dumps(values)


@app.route("/nfl_team_data/", methods=['POST'])
def nfl_team_data():
    team = request.json['team']

    if redis_db.exists(team):
        return redis_db.get(team).decode('utf-8')
    else:
        team_data = db.engine.execute(text("""select o.year, o.rk as off_rk, d.rk as def_rk
                                from off_regseason_gamestats o
                                left join def_rev_regseason_gamestats d
                                  on o.year = d.year and o.team = d.team
                                where o.team like :name
                                order by year;"""), {'name': team})
        off_rank_list = []
        year_list = []
        def_rank_list = []
        for row in team_data:
            year_list.append(row[0])
            off_rank_list.append(row[1])
            def_rank_list.append(row[2])
        json_data = {'years': year_list, 'offense': off_rank_list, 'defense': def_rank_list}
        redis_db.set(team, json.dumps(json_data))
        return json.dumps(json_data)


@app.route("/nfl_historical_rankings/")
def nfl_historical_rankings():
    sections = [
        {
            'href': '/',
            'name': 'Blog'
        },
        {
            'href': '/resources/',
            'name': 'Data Science Resources'
        }
    ]
    return render_template("/nfl/historical_nfl_rankings.html", sections=sections)
