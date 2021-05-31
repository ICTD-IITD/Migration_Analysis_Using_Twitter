import mongoengine


class Tweet(mongoengine.Document):
    createdAt = mongoengine.StringField(required=True)
    userMentions = mongoengine.ListField(default=[])
    favouriteCount = mongoengine.IntField(required=True)
    tweetID = mongoengine.StringField(primary_key=True)
    language = mongoengine.StringField(default='en')
    country = mongoengine.StringField(default='')
    countryCode = mongoengine.StringField(default='')
    placeURL = mongoengine.URLField()
    placeFullName = mongoengine.StringField(default='')
    placeID = mongoengine.StringField(default='')
    retweetCount = mongoengine.IntField(required=True)
    isRetweeted = mongoengine.BooleanField(required=True)
    text = mongoengine.StringField(default='')
    isQuoteStatus = mongoengine.BooleanField(default=False)
    quotedID = mongoengine.StringField(default='')
    user = mongoengine.StringField(required=True)
    userID = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)
    currentPoint = mongoengine.StringField(default='', required=True)
    currentQueryLocation = mongoengine.StringField(required=True, default='')

    meta = {
        'db_alias': 'core',
        'collection': 'tweets'
    }
