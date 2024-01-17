from mongoengine import connect


class DatabaseManager:
    def __init__(self, db_name, uri, port=27017):
        self.db_name = db_name
        self.uri = uri
        self.port = port

    def connect_db(self):
        connect(alias=self.db_name, db=self.db_name, host=self.uri)
