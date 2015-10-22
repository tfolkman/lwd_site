from lwd import db


class Post(db.Model):

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    most_recent = db.Column(db.Boolean, default=False)
    href = db.Column(db.String(256))
    title = db.Column(db.String(128))
    sub_title = db.Column(db.String(256))
    image_source = db.Column(db.String(128))
    post_date = db.Column(db.Date)


class Resource(db.Model):

    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    resource_type = db.Column(db.String(64))
    href = db.Column(db.String(256))
    title = db.Column(db.String(128))
    sub_title = db.Column(db.String(512))
    image_source = db.Column(db.String(128))
