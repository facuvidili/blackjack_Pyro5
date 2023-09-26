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

    def save_bet(self, name, bet):
        try:
            mycursor = self.mydb.cursor()
            # Verificamos si ya existe un registro con el mismo nombre
            mycursor.execute("SELECT nombre FROM jugadores WHERE nombre = %s", (name,))
            existing_record = mycursor.fetchone()
    
            if existing_record:
                # Si existe un registro con el mismo nombre, actualizamos el saldo
                mycursor.execute("UPDATE jugadores SET saldo = %s WHERE nombre = %s", (bet, name))
            else:
                # Si no existe, insertamos un nuevo registro
                mycursor.execute("INSERT INTO jugadores (nombre, saldo) VALUES (%s, %s)", (name, bet))
    
            self.mydb.commit()
        except mysql.connector.Error as e:
            print(f"Error al guardar la apuesta: {e}")
            self.mydb.rollback()
        finally:
            mycursor.close()

