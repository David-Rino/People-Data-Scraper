import psycopg
from datetime import datetime

class SQLModel:
    def __init__(self, hostname, database, username, password, port_id):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.port_id = port_id
        self.controller = None

    def setController(self, controller):
        self.controller = controller

    def makeConn(self):
        conn = None

        try:
            conn = psycopg.connect(host=self.hostname, dbname=self.database, user=self.username, password=self.password, port = self.port_id)
        except Exception as error:
            print(error)

        return conn

    def closeConn(self, conn):
        conn.close()

    def addUser(self, user_id, firstName, lastName):

        try:
            conn =self.makeConn()
            cur = conn.cursor()
            cur.execute(f"""
                INSERT INTO users (user_id, first_name, last_name)
                VALUES ({user_id}, '{firstName}', '{lastName}')
            """)
            conn.commit()
            cur.close()
            conn.close()
            print(f"User: {firstName}, {lastName} has been added with the user ID: {user_id} ")
        except Exception as error:
            print(error)

    def retriveUser(self, user_id):
        try:
            conn = self.makeConn()
            cur = conn.cursor()
            cur.execute(f"""
                SELECT *
                FROM users u
                WHERE u.user_id = {user_id}
            """)
            row = cur.fetchone()
            cur.close()
            conn.close()
            return row
        except Exception as error:
            print(error)

        return None

    def retriveUserList(self, amount):
        try:
            conn = self.makeConn()
            cur = conn.cursor()
            cur.execute(f"""
                SELECT *
                FROM users 
                ORDER BY user_id DESC
                limit {amount}
            """)
            row = cur.fetchall()
            cur.close()
            conn.close()
            return row
        except Exception as error:
            print(error)

        return None

    def addClient(self, clientID, currentUserID, firstName, lastName, typeOfInsurance, age):
        try:
            conn =self.makeConn()
            cur = conn.cursor()
            cur.execute(f"""
                INSERT INTO clients (clientID, brokerIssuer, first_name, last_name, type_of_insurance, age)
                VALUES ({clientID}, {currentUserID}, '{firstName}', '{lastName}', '{typeOfInsurance}', '{age}')
            """)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as error:
            print(error)

    def retriveClients(self, amount):
        try:
            conn = self.makeConn()
            cur = conn.cursor()
            cur.execute(f"""
                SELECT *
                FROM clients 
                ORDER BY clientID DESC
                limit {amount}
            """)
            row = cur.fetchall()
            cur.close()
            conn.close()
            return row
        except Exception as error:
            print(error)

        return None

    def addPhone(self, phoneID, clientID, phoneNumber):
        try:
            conn =self.makeConn()
            cur = conn.cursor()
            cur.execute(f"""
                INSERT INTO phonenumbers (phoneID, clientID, phone_number)
                VALUES ({phoneID}, '{clientID}', '{phoneNumber}')
            """)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as error:
            print(error)

    def retrivePhones(self, amount):
        try:
            conn = self.makeConn()
            cur = conn.cursor()
            cur.execute(f"""
                SELECT *
                FROM phonenumbers 
                ORDER BY phoneID DESC
                limit {amount}
            """)
            row = cur.fetchall()
            cur.close()
            conn.close()
            return row
        except Exception as error:
            print(error)

        return None

    def addAddress(self, propertyID, clientID, address, state, zipcode):
        try:
            conn =self.makeConn()
            cur = conn.cursor()
            cur.execute(f"""
                INSERT INTO property (propertyID, clientID, address, state, zipcode)
                VALUES ({propertyID}, '{clientID}', '{address}', '{state}', '{zipcode}')
            """)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as error:
            print(error)

    def retriveAddresses(self, amount):
        try:
            conn = self.makeConn()
            cur = conn.cursor()
            cur.execute(f"""
                SELECT *
                FROM property 
                ORDER BY propertyID DESC
                limit {amount}
            """)
            row = cur.fetchall()
            cur.close()
            conn.close()
            return row
        except Exception as error:
            print(error)

        return None