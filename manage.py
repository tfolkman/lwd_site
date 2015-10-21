import json
import datetime
from lwd import app, db
from lwd.models import Post
from flask_script import Manager

manager = Manager(app)


@manager.command
def syncdb():
    db.create_all()


@manager.command
def create_posts(post_file):
    with open(post_file) as f:
        data = json.load(f)

    for post in data:
        new_post = Post()
        new_post.id = post['id']
        new_post.most_recent = post['most_recent'] == 'True'
        new_post.href = post['href']
        new_post.title = post['title']
        new_post.sub_title = post['sub_title']
        new_post.image_source = post['image_source']
        new_post.post_date = datetime.datetime.strptime(post['date'], "%Y%m%d").date()
        db.session.add(new_post)
    db.session.commit()


@manager.command
def clear_posts():
    Post.query.delete()
    db.session.commit()

if __name__ == '__main__':
    manager.run()
