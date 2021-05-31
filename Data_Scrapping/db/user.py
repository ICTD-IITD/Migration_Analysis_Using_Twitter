import mongoengine


class User(mongoengine.Document):
    userID = mongoengine.StringField(primary_key=True, required=True)
    screenName = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)
    url = mongoengine.URLField()
    followerCount = mongoengine.IntField(default=0)
    friendCount = mongoengine.IntField(default=0)
    statusCount = mongoengine.IntField(default=0)
    createdAt = mongoengine.StringField()
    verified = mongoengine.BooleanField(default=False, required=True)
    profileLocation = mongoengine.StringField(default='')
    profileLocationID = mongoengine.StringField(default='')

    meta = {
        'db_alias': 'core',
        'collection': 'users'
    }
