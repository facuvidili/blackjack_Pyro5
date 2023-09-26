import mysql.connector
class DBconnectSingleton:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super().__new__(self)
            # Iniciar DB
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="blackjack"
            
        )   
        return self._instance
    
    def get_all(self, attr, table):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT " + attr + " FROM " + table)
        return mycursor.fetchall()
