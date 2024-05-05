import psycopg
from datetime import datetime

class SQLModel:
    def __init__(self, hostname, database, username, password, port_id, connection=None):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.port_id = port_id
        self.controller = None

        if connection:
            self.connection = connection
        else:
            self.connection = self.makeConn()

    def setController(self, controller):
        self.controller = controller

    def resetDatabase(self):
        # This function is simply to reset an SQLData base for testing
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                TRUNCATE TABLE clients, phonenumbers, property;

                INSERT INTO clients (clientID, brokerIssuer, first_name, last_name, type_of_insurance, age)
                VALUES (1, 1, 'Rino', 'David', 'health', 21);

                INSERT INTO phonenumbers (phoneID, clientID, phone_number)
                VALUES (1, 1, '777-777-777');

                INSERT INTO property (propertyID, clientID, address, state, zipcode)
                VALUES (1, 1, '7777 Home Rd', 'NV', '89142');
            """)
            self.connection.commit()
            cur.close()
        except Exception as error:
            cur.close()
            print(str(error))


    def makeConn(self):
        conn = None

        try:
            conn = psycopg.connect(host=self.hostname, dbname=self.database, user=self.username, password=self.password, port = self.port_id)
        except Exception as error:
            print(str(error))

        return conn

    def closeConn(self, conn):
        conn.close()

    def addUser(self, user_id, firstName, lastName):

        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                INSERT INTO users (user_id, first_name, last_name)
                VALUES ({user_id}, '{firstName}', '{lastName}')
            """)
            self.connection.commit()
            cur.close()
            #print(f"User: {firstName}, {lastName} has been added with the user ID: {user_id} ")
        except Exception as error:
            cur.close()
            print(str(error))

    # Retrieves a single user from the SQLDatabase by using their userID
    def retrieveUser(self, user_id):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT *
                FROM users u
                WHERE u.user_id = {user_id}
            """)
            row = cur.fetchone()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    # Retrieves all users, specified by an amount, ordered in Desc format
    def retrieveUserList(self, amount):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT *
                FROM users 
                ORDER BY user_id DESC
                limit {amount}
            """)
            row = cur.fetchall()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    def addClient(self, clientID, currentUserID, firstName, lastName, typeOfInsurance, age):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                INSERT INTO clients (clientID, brokerIssuer, first_name, last_name, type_of_insurance, age)
                VALUES ({clientID}, {currentUserID}, '{firstName}', '{lastName}', '{typeOfInsurance}', '{age}')
            """)
            self.connection.commit()
            cur.close()
        except Exception as error:
            cur.close()
            print(str(error))

    def retrieveClients(self, amount):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT *
                FROM clients 
                ORDER BY clientID DESC
                limit {amount}
            """)
            row = cur.fetchall()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    def retrieveAllClientID(self, userID):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT cl.clientID
                FROM users u 
                JOIN clients cl ON cl.brokerissuer = u.user_id
                WHERE u.user_id = {userID}
            """)
            row = cur.fetchall()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    def addPhone(self, phoneID, clientID, phoneNumber):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                INSERT INTO phonenumbers (phoneID, clientID, phone_number)
                VALUES ({phoneID}, '{clientID}', '{phoneNumber}')
            """)
            self.connection.commit()
            cur.close()
        except Exception as error:
            cur.close()
            print(str(error))

    def retrievePhones(self, amount):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT *
                FROM phonenumbers 
                ORDER BY phoneID DESC
                limit {amount}
            """)
            row = cur.fetchall()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    def addAddress(self, propertyID, clientID, address, state, zipcode):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                INSERT INTO property (propertyID, clientID, address, state, zipcode)
                VALUES ({propertyID}, '{clientID}', '{address}', '{state}', '{zipcode}')
            """)
            self.connection.commit()
            cur.close()
        except Exception as error:
            cur.close()
            print(str(error))

    # Retrieves Address as a list given a specified amount, will return in a descending format
    def retrieveAddresses(self, amount):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT *
                FROM property 
                ORDER BY propertyID DESC
                limit {amount}
            """)
            row = cur.fetchall()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    # Returns the joined table of a singular clientID.
    def retrieveClientInformation(self, clientID):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT u.first_name AS Broker_Issuer, cl.first_name, cl.last_name, pr.address, pr.state, pr.zipcode
                FROM users u 
                JOIN clients cl ON cl.brokerissuer = u.user_id
                JOIN property pr ON pr.clientid = cl.clientid
                WHERE u.user_id = {self.controller.currentUserID} and cl.clientId = {clientID}
            """)
            row = cur.fetchall()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    # Returns all the associated phone numbers of a client, will return an empty list if no phone numbers associated with a client
    def retrieveClientPhoneNumbers(self, clientID):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT phone_number
                FROM phonenumbers 
                JOIN clients ON clients.clientid = phonenumbers.clientid
                WHERE clients.clientid = {clientID}
            """)
            row = cur.fetchall()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    def retrieveLogs(self, amount):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT *
                FROM interaction_logs 
                ORDER BY logID DESC
                limit {amount}
            """)
            row = cur.fetchall()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    def retrieveAllUserLogs(self, userID):
        try:
            cur = self.connection.cursor()
            cur.execute(f"""
                SELECT inter.logID, cl.first_name AS Broker_Issuer, cl.first_name AS Client_First_Name, inter.interactiontype, inter.datechanged, inter.status 
                FROM users u
                JOIN clients cl ON cl.brokerissuer = u.user_id
                JOIN interaction_logs inter ON inter.clientid = cl.clientid
                WHERE u.user_id = {userID}
            """)
            row = cur.fetchall()
            cur.close()
            return row
        except Exception as error:
            cur.close()
            print(str(error))

        return None

    def addInteractionLog(self, logID, clientID, userID, interactionType, status):
        try:
            cur = self.connection.cursor()
            currentTime = datetime.now().strftime("%m-%d-%Y")

            cur.execute(f"""
                INSERT INTO interaction_logs (logID, clientID, userID, interactiontype, datechanged, status)
                VALUES ({logID}, {clientID}, {userID}, '{interactionType}', '{currentTime}', '{status}');
            """)
            self.connection.commit()
            cur.close()
        except Exception as error:
            cur.close()
            print(str(error))