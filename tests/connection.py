from squab.connection import CouchConnection


def connection(db='definition'):
    return CouchConnection(
        host='http://localhost:5984',
        db=db,
        user='admin',
        password='admin',
        ignore_missing=False)
