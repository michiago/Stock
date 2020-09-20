import sqlite3
import pandas


class InteractionDB:
    def __init__(self, nameDB):
        self.nameDB = nameDB

    def insertInDB(self, dataframe, tableName):
        """ Create a table in the database from a dataframe object """

        try:
            connection = sqlite3.connect(self.nameDB)
            dataframe.to_sql(tableName, connection, if_exists="replace", index=False)
            connection.close()
        except Error as e:
            print("Sorry, an ERROR while connecting to the database occurred")
            raise SystemExit(e)

    def getQueryFromDB(self, query):
        """ Get the result of a given query on the database """

        try:
            connection = sqlite3.connect(self.nameDB)
            data = pandas.read_sql_query(query, connection)
            connection.close()
            return data
        except Error as e:
            print("Sorry, an ERROR while connecting to the database occurred")
            raise SystemExit(e)