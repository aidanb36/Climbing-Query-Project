import sqlite3
import pandas as pd
import os


class DBOperation:
    def __init__(self):
        #Create the connection to the database
        self.conn = sqlite3.connect('climbData.db')
        #Create the cursor object
        self.cursor = self.conn.cursor()
        
    def loadData(self):
        #Create tables and add data
        self.createTables()
        self.readCsvToTable('mountains.csv', 'mountains')
        self.readCsvToTable('routes.csv', 'routes')

        #Commit changes to the database
        self.conn.commit()

    def createTables(self):
        self.cursor.execute('''
              CREATE TABLE IF NOT EXISTS mountains
              (
                mountainId INTEGER PRIMARY KEY,
                name VARCHAR(255),
                location VARCHAR(255),
                elevation INTEGER,
                rockType VARCHAR(255)
              );
              ''')
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS routes
                (
                    climbId INTEGER PRIMARY KEY,
                    name VARCHAR(255),
                    mountainName VARCHAR(255),
                    type VARCHAR(255),
                    grade VARCHAR(255),
                    CONSTRAINT fk_mountainName
                        FOREIGN KEY (mountainName)
                        REFERENCES mountains(name)
                );
                ''')


    def readCsvToTable(self, filename, tablename):
        #Read the csv file as a pandas dataframe
        path = os.path.join('backend', 'data', filename)
        dataFrame = pd.read_csv(path)
        #This call takes the dataframe created above and loads it into the correct table
        dataFrame.to_sql(tablename, self.conn, if_exists='replace', index=False)
    
    def buildWhere(self, data):
        whereString = ''
        if (data['key'] != '' and data['value'] != ''):
            whereString = f"WHERE {data['key']} = '{data['value']}'"
        return whereString
    
    def buildSelect(self, data):
        if (data['count']):
            return "SELECT COUNT(*)"
        else:
            return "SELECT *"

    #eg. data = {"table": "mountains", "key": "name", "value": "Mingus Mountain", "count": True}
    def queryData(self, data):
        if (data["table"] == "both"):
            return self.joinQuery(data)
        else:
            return self.simpleQuery(data)
       
    def simpleQuery(self, data):
        # print(f"{self.buildSelect(data)} FROM {data['table']} {self.buildWhere(data)}")
        self.cursor.execute(f"{self.buildSelect(data)} FROM {data['table']} {self.buildWhere(data)}")
        return self.cursor.fetchall()

    
    def joinQuery(self, data):
        # print(f"{self.buildSelect(data)} FROM routes JOIN mountains ON routes.mountainName = mountains.name {self.buildWhere(data)}")
        self.cursor.execute(f"{self.buildSelect(data)} FROM routes JOIN mountains ON routes.mountainName = mountains.name {self.buildWhere(data)}")
        return self.cursor.fetchall()
