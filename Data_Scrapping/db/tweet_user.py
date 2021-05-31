import mongoengine
from .user import User
from .tweets import Tweet


class tweetUser(mongoengine.Document):
    homeLocationID = mongoengine.StringField(default='')
    homeLocation = mongoengine.StringField(default='')
    userID = mongoengine.StringField(default='', required=True)
    tweetedFrom = mongoengine.StringField(required=True)
    tweetedFromLat = mongoengine.StringField(required=True)
    tweetedFromLong = mongoengine.StringField(required=True)
    tweetID = mongoengine.StringField(required=True, primary_key=True)
    searchTerm = mongoengine.StringField(required=True)
    tweetedFromState = mongoengine.StringField(required=True)
    meta = {
        'db_alias': 'core',
        'collection': 'tweetUsers'
    }
