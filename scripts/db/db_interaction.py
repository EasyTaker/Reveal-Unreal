import mysql.connector

class search_db:

 def __init__(self, user='root', password='testtest123HALLO', host='127.0.0.1', database='databasefake'):
        self.user=user
        self.password=password
        self.host= host
        self.database = database
 def con(self):
        conn = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
        cursor = conn.cursor()
        #Executing an MYSQL function using the execute() method
        cursor.execute("SELECT DATABASE()")
        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Class created, Connection established to: ",data)

