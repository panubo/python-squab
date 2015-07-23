class CouchConnection(object):

    def __init__(self, host, db, user, password, ignore_missing=False):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.ignore_missing = ignore_missing
