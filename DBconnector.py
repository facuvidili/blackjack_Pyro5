import mysql.connector
import sys
class DBconnectSingleton:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super().__new__(self)
            
            # try:
            #         self.mydb = mysql.connector.connect(
            #         host="192.168.100.7",
            #         user="chimi",
            #         password="chimi",
            #         database="blackjack"
                    
            #         )
            # except mysql.connector.Error as e:
            #         try:
            #             self.mydb = mysql.connector.connect(
            #             host="localhost",
            #             user="root",
            #             password="",
            #             database="blackjack"
                        
            #             )
            #         except mysql.connector.Error as e:
            #             print(f"Error al conectarse a la base de datos: {e}")
            #             sys.exit()
               
        return self._instance
    
    def connect(self):
        try:
                    mydb = mysql.connector.connect(
                    host="172.16.205.157",
                    user="root",
                    password="",
                    database="blackjack"
                    
                    )
        except mysql.connector.Error as e:
                    try:
                        mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="blackjack"

                        
                        )
                        None
                    except mysql.connector.Error as e:
                        print(f"Error al conectarse a la base de datos: {e}")
                        sys.exit()
        return mydb
    
    def get_all(self, attr, table):
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT " + attr + " FROM " + table)
        all= mycursor.fetchall()
        mycursor.close()
        return all
    
    def get_card_id(self, rank, suit):
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id FROM mazo WHERE valorCarta = '" + str(rank) + "' AND tipoCarta = '" + str(suit) + "'")
        cardId = mycursor.fetchone()
        mycursor.close()
        return cardId
    
    def update_all(self, deck, players, dealer, dealerAmmount):
        
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE mazo SET estado = 0")
            for card in deck.cards:
                mycursor.execute("UPDATE mazo SET estado = 1 WHERE tipoCarta = '" + str(card.get_suit()) + "' AND valorCarta = '" + str(card.get_rank()) + "'")

            mycursor.execute("DELETE FROM manoactual")
            mycursor.execute("ALTER TABLE manoactual AUTO_INCREMENT=0;")
            # mycursor.execute("DELETE FROM jugadores")
            mycursor.execute("ALTER TABLE jugadores AUTO_INCREMENT=0;")
            mycursor.execute("UPDATE jugadores SET saldo = '"+ str(dealerAmmount) +"' WHERE id = '-1'")
            mydb.commit()
        except mysql.connector.Error as e:
            print(f"Error al guardar el mazo: {e}")
            mydb.rollback()
        finally:
            mycursor.close()

        self.update_dealer_hand(dealer)
            
        for player in players:
            # mycursor.execute("INSERT INTO jugadores (id, nombre, saldo) VALUES ('" + str(index+1) + "', '"  + player.name + "', '" + str(player.ammount) + "')")
            try:
                mydb = self.connect()
                mycursor = mydb.cursor()
                # Verificamos si ya existe un registro con el mismo nombre
                mycursor.execute("SELECT nombre FROM jugadores WHERE nombre = '" + player.name + "'")
                existing_record = mycursor.fetchone()
                
                if existing_record:
                    # Si existe un registro con el mismo nombre, actualizamos el saldo
                    mycursor.execute("UPDATE jugadores SET saldo = '"+ str(player.ammount) +"', apuesta = '"+ str(player.bet) +"' WHERE nombre = '" + player.name + "'")
                else:
                    # Si no existe, insertamos un nuevo registro
                    mycursor.execute("INSERT INTO jugadores (nombre, saldo, apuesta) VALUES (%s, %s, %s)", (player.name, player.ammount, 0))
        
                mydb.commit()
                self.update_player_hand(player)
            except mysql.connector.Error as e:
                print(f"Error al guardar el jugador: {e}")
                mydb.rollback()
            finally:
                mycursor.close()
    
    def update_player_hand(self, player):
        cards = player.get_hand().get_cards()
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT id FROM jugadores WHERE nombre = '" + player.name + "'")
            playerId= mycursor.fetchone()
            mycursor.execute("DELETE FROM manoactual WHERE idJugador = " + str(playerId[0]))
            for card in cards:   
                mycursor.execute("UPDATE mazo SET estado = 0 WHERE tipoCarta = '" + str(card.get_suit()) + "' AND valorCarta = '" + str(card.get_rank()) + "'")
                mycursor.execute("INSERT INTO manoactual (idCarta, idJugador) VALUES ('"
                            + str(self.get_card_id(card.rank, card.suit)[0]) 
                            + "', '" + str(playerId[0]) + "')")
            mydb.commit()
        except mysql.connector.Error as e:
            print(f"Error al guardar la mano: {e}")
            mydb.rollback()
        finally:
            mycursor.close()
    
    def update_dealer_hand(self, dealer):
        cards = dealer.get_cards()
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()
            mycursor.execute("DELETE FROM manoactual WHERE idJugador = -1")
            for card in cards:   
                mycursor.execute("UPDATE mazo SET estado = 0 WHERE tipoCarta = '" + str(card.get_suit()) + "' AND valorCarta = '" + str(card.get_rank()) + "'")
                mycursor.execute("INSERT INTO manoactual (idCarta, idJugador) VALUES ('"
                            + str(self.get_card_id(card.rank, card.suit)[0]) 
                            + "', -1)")
            mydb.commit()
        except mysql.connector.Error as e:
            print(f"Error al guardar la mano del dealer: {e}")
            mydb.rollback()
        finally:
            mycursor.close()
    
    def update_player_ammount(self, player):
        try:
                mydb = self.connect()
                mycursor = mydb.cursor()
                # Verificamos si ya existe un registro con el mismo nombre
                mycursor.execute("SELECT nombre FROM jugadores WHERE nombre = '" + player.name + "'")
                existing_record = mycursor.fetchone()
                
                if existing_record:
                    # Si existe un registro con el mismo nombre, actualizamos el saldo
                    mycursor.execute("UPDATE jugadores SET saldo = '"+ str(player.ammount) +"', apuesta = '"+ str(player.bet) +"' WHERE nombre = '" + player.name + "'")
               
                mydb.commit()
        except mysql.connector.Error as e:
                print(f"Error al guardar el monto: {e}")
                mydb.rollback()
        finally:
                mycursor.close()        
            
    def remove_one(self, id, table):
       
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()
            mycursor.execute("DELETE FROM manoactual WHERE idJugador = '" + str(id+1) + "'")
            mycursor.execute("DELETE FROM '" + table + "' WHERE id = '" + str(id+1) + "'")
            mydb.commit()
        except mysql.connector.Error as e:
                    print(f"Error al guardar remover el jugador: {e}")
                    mydb.rollback()
        finally:
                     mycursor.close()
    
    def reset_deck(self):
       
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()

            mycursor.execute("UPDATE mazo SET estado = 1")
        except mysql.connector.Error as e:
                    print(f"Error al guardar el mazo: {e}")
                    mydb.rollback()
        finally:
                    mycursor.close()

    def get_one_ammount(self, name):
       
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()
            # Verificamos si ya existe un registro con el mismo nombre
            mycursor.execute("SELECT saldo FROM jugadores WHERE nombre = '" + name + "'")
            ammount = mycursor.fetchone()
            if ammount:
                return ammount[0]
            else:
                return -1
        except mysql.connector.Error as e:
                print(f"Error al extraer monto: {e}")
                mydb.rollback()
        finally:
                mycursor.close()

    def get_one_bet(self, name):
        
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()
            # Verificamos si ya existe un registro con el mismo nombre
            mycursor.execute("SELECT apuesta FROM jugadores WHERE nombre = '" + name + "'")
            bet = mycursor.fetchone()
            if bet:
                return bet[0]
            else:
                return 0
        except mysql.connector.Error as e:
                print(f"Error al extraer apuesta: {e}")
                mydb.rollback()
        finally:
                mycursor.close()
    
    def get_one_hand(self, name):
        
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()
            # Verificamos si ya existe un registro con el mismo nombre
            mycursor.execute("SELECT id FROM jugadores WHERE nombre = '" + name + "'")
            playerId=mycursor.fetchone()
            if playerId:
                mycursor.execute("SELECT mazo.tipoCarta, mazo.valorCarta, mazo.estado FROM mazo LEFT JOIN manoactual ON manoactual.idCarta = mazo.id WHERE manoactual.idJugador = " + str(playerId[0]))
                cards = mycursor.fetchall()
                return cards
            else:
                return False
        except mysql.connector.Error as e:
                print(f"Error al extraer mano: {e}")
                mydb.rollback()
        finally:
                mycursor.close()

    def get_dealers_cards(self):
       
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT mazo.tipoCarta, mazo.valorCarta, mazo.estado FROM mazo LEFT JOIN manoactual ON manoactual.idCarta = mazo.id WHERE manoactual.idJugador = -1")
            cards = mycursor.fetchall()
            if cards:
                return cards
            else:
                return None
        except mysql.connector.Error as e:
                print(f"Error al extraer mano: {e}")
                mydb.rollback()
        finally:
                mycursor.close()

    def get_dealer_ammount(self):
        try:
            mydb = self.connect()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT saldo FROM jugadores WHERE id = '-1'")
            ammount = mycursor.fetchone()
            return ammount[0]
        except mysql.connector.Error as e:
                print(f"Error al extraer monto: {e}")
                mydb.rollback()
        finally:
                mycursor.close()