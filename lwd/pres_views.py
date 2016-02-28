from flask import render_template, request
from . import app, db, redis_db
import json
from sqlalchemy import text

@app.route("/talk_like_pres_candidate/")
def talk_like_pres_candidate():
    sections = [
        {
            'href': '/',
            'name': 'Blog'
        },
        {
            'href': '/resources/',
            'name': 'Data Science Resources'
        },
        {
            'href': '/#about',
            'name': 'About/Contact'
        }
    ]
    return render_template("/talk_pres/talk_like_pres_cand.html", sections=sections)
