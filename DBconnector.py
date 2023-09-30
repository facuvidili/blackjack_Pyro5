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
            password="",
            database="blackjack"
            
        )   
        return self._instance
    
    def get_all(self, attr, table):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT " + attr + " FROM " + table)
        return mycursor.fetchall()
    
    def get_card_id(self, rank, suit):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT id FROM mazo WHERE valorCarta = '" + str(rank) + "' AND tipoCarta = '" + str(suit) + "'")
        cardId = mycursor.fetchone()
        return cardId
    
    def update_all(self, deck, players, dealer, dealerAmmount):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("UPDATE mazo SET estado = 0")
            for card in deck.cards:
                mycursor.execute("UPDATE mazo SET estado = 1 WHERE tipoCarta = '" + str(card.get_suit()) + "' AND valorCarta = '" + str(card.get_rank()) + "'")

            mycursor.execute("DELETE FROM manoactual")
            mycursor.execute("ALTER TABLE manoactual AUTO_INCREMENT=0;")
        # mycursor.execute("DELETE FROM jugadores")
        # mycursor.execute("ALTER TABLE jugadores AUTO_INCREMENT=0;")
            mycursor.execute("UPDATE jugadores SET saldo = '"+ str(dealerAmmount) +"' WHERE id = '99999999'")
        except mysql.connector.Error as e:
            print(f"Error al guardar el mazo: {e}")
            self.mydb.rollback()
        finally:
            mycursor.close()

        dealerCards = dealer.get_cards()
        # print(*dealerCards)
        for card in dealerCards:
            mycursor = self.mydb.cursor()
            try:
                mycursor.execute("INSERT INTO manoactual (idCarta, idJugador) VALUES ('"
                                        + str(self.get_card_id(card.rank, card.suit)[0]) 
                                        + "', '99999999')")
            except mysql.connector.Error as e:
                print(f"Error al guardar la mano del dealer: {e}")
                self.mydb.rollback()
            finally:
                mycursor.close()
            
        for player in players:
            # mycursor.execute("INSERT INTO jugadores (id, nombre, saldo) VALUES ('" + str(index+1) + "', '"  + player.name + "', '" + str(player.ammount) + "')")
            try:
                mycursor = self.mydb.cursor()
                # Verificamos si ya existe un registro con el mismo nombre
                mycursor.execute("SELECT nombre FROM jugadores WHERE nombre = '" + player.name + "'")
                existing_record = mycursor.fetchone()
                
                if existing_record:
                    # Si existe un registro con el mismo nombre, actualizamos el saldo
                    mycursor.execute("UPDATE jugadores SET saldo = '"+ str(player.ammount) +"' WHERE nombre = '" + player.name + "'")
                else:
                    # Si no existe, insertamos un nuevo registro
                    mycursor.execute("INSERT INTO jugadores (nombre, saldo) VALUES (%s, %s)", (player.name, player.ammount))
        
                self.mydb.commit()
            except mysql.connector.Error as e:
                print(f"Error al guardar el jugador: {e}")
                self.mydb.rollback()
            finally:
                mycursor.close()
            
                cards = player.get_hand().get_cards()

                for card in cards:   
                    try:
                        mycursor = self.mydb.cursor()

                        mycursor.execute("SELECT id FROM jugadores WHERE nombre = '" + player.name + "'")
                        id= mycursor.fetchone()

                        mycursor.execute("INSERT INTO manoactual (idCarta, idJugador) VALUES ('"
                                    + str(self.get_card_id(card.rank, card.suit)[0]) 
                                    + "', '" + str(id[0]) + "')")
                        self.mydb.commit()
                    except mysql.connector.Error as e:
                        print(f"Error al guardar la mano: {e}")
                        self.mydb.rollback()
                    finally:
                        mycursor.close()


    def remove_one(self, id, table):
        mycursor = self.mydb.cursor()
        mycursor.execute("DELETE FROM manoactual WHERE idJugador = '" + str(id+1) + "'")
        mycursor.execute("DELETE FROM '" + table + "' WHERE id = '" + str(id+1) + "'")
        self.mydb.commit()
    
    def reset_deck(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("UPDATE mazo SET estado = 1")

    def get_one_ammount(self, name):
        try:
            mycursor = self.mydb.cursor()
            # Verificamos si ya existe un registro con el mismo nombre
            mycursor.execute("SELECT saldo FROM jugadores WHERE nombre = '" + name + "'")
            ammount = mycursor.fetchone()
            if ammount:
                return ammount[0]
            else:
                return -1
        except mysql.connector.Error as e:
                print(f"Error al extraer monto: {e}")
                self.mydb.rollback()
        finally:
                mycursor.close()

    def get_dealer_ammount(self):
        try:
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT saldo FROM jugadores WHERE id = '99999999'")
            ammount = mycursor.fetchone()
            return ammount[0]
        except mysql.connector.Error as e:
                print(f"Error al extraer monto: {e}")
                self.mydb.rollback()
        finally:
                mycursor.close()