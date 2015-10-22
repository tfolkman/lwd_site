from flask import render_template
from flask import request
from flask import send_from_directory
from . import app, db
from lwd.models import Post, Resource


@app.route("/")
def index():
    sections = [
        {
            'href': '#mostRecent',
            'name': 'Most Recent Post'
        },
        {
            'href': '#prevPosts',
            'name': 'Previous Posts'
        },
        {
            'href': '#about',
            'name': 'About/Contact'
        },
        {
            'href': '/resources/',
            'name': 'Data Science Resources'
        }
    ]

    most_recent_post = db.session.query(Post).filter_by(most_recent=True).one()
    most_recent_post = most_recent_post.__dict__
    old_posts = db.session.query(Post).filter_by(most_recent=False).order_by(Post.id.desc()).all()
    old_posts = [post.__dict__ for post in old_posts]

    return render_template("index.html", title='Learning With Data', sections=sections,
                           most_recent_post=most_recent_post, previous_posts=old_posts)


@app.route("/resources/")
def resources():
    sections = [
        {
            'href': '#gettingStarted',
            'name': 'Getting Started'
        },
        {
            'href': '#online',
            'name': 'Online Courses'
        },
        {
            'href': '#sites',
            'name': 'Websites'
        },
        {
            'href': '#podcasts',
            'name': 'Podcasts'
        },
        {
            'href': '#books',
            'name': 'Books'
        },
        {
            'href': '#libs',
            'name': 'Libraries'
        },
        {
            'href': '/',
            'name': 'Blog'
        }
    ]

    resource_posts = db.session.query(Resource).order_by(Resource.id).all()

    getting_started = []
    online_resources = []
    site_resources = []
    podcast_resources = []
    book_resources = []
    library_resources = []

    for resource in resource_posts:
        resource_dict = resource.__dict__
        if resource_dict['resource_type'] == 'gettingStarted':
            getting_started.append(resource_dict)
        if resource_dict['resource_type'] == 'online':
            online_resources.append(resource_dict)
        if resource_dict['resource_type'] == 'sites':
            site_resources.append(resource_dict)
        if resource_dict['resource_type'] == 'podcasts':
            podcast_resources.append(resource_dict)
        if resource_dict['resource_type'] == 'books':
            book_resources.append(resource_dict)
        if resource_dict['resource_type'] == 'libs':
            library_resources.append(resource_dict)

    return render_template("resources.html", title="Learning With Data / Resources", sections=sections,
                           getting_started=getting_started,
                           online_resources=online_resources,
                           site_resources=site_resources,
                           podcast_resources=podcast_resources,
                           book_resources=book_resources,
                           library_resources=library_resources)


@app.route("/rss_feed.xml")
def feed():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/nfl_historical_rankings/", methods=['GET', 'POST'])
def nfl_historical_rankings():
    import psycopg2

    conn = psycopg2.connect("dbname=nfl_football user=deploy")
    cur = conn.cursor()
    cur.execute("""select distinct team from off_regseason_gamestats order by team;""")
    teamNames = cur.fetchall()
    teamNamesList = []
    for name in teamNames:
        teamNamesList.append(name[0])

    if request.method == 'POST':
        name = request.form['team']
    else:
        name = "San Francisco 49ers"

    offRankCmd = "select rk, year from off_regseason_gamestats where team like (%s) order by year;"
    cur.execute(offRankCmd, (name,))
    offRankRows = cur.fetchall()
    offRankList = []
    yearList = []
    for row in offRankRows:
        offRankList.append(row[0])
        yearList.append(row[1])
    defRankCmd = "select rk from def_rev_regseason_gamestats where team like (%s) order by year;"
    cur.execute(defRankCmd, (name,))
    defRankRows = cur.fetchall()
    defRankList = []
    for row in defRankRows:
        defRankList.append(row[0])

    return render_template("historical_nfl_rankings.html", team_names=teamNamesList, name=name, o_data_years=yearList,
                           o_data_rk=offRankList, d_data_rk=defRankList)


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
