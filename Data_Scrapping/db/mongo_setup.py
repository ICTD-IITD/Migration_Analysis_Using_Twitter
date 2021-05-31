from mongoengine import connect, disconnect


def init(username, password):
    connect(
        alias='core',
        host='mongodb+srv://' + username+':'+password +
        '@iitdellhi-kakxg.mongodb.net/metro_tf?retryWrites=true&w=majority'
    )
    print('Connected to DB')


def disconnect_conn():
    print('Disconnected from DB')
    disconnect(alias='core')
