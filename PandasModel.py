import pandas as pd

class PandasModel:
    def __init__(self):
        self.df = None
        self.controller = None

    def setController(self, controller):
        self.controller = controller

    def processFile(self, file_path):
        try:
            self.df = pd.read_excel(file_path)
            #print(self.df)
        except Exception as e:
            print(str(e))

    def processData(self, clientID):
        #print("Ermm What the Sigma. Process Client Data for " + str(clientID))
        clientData = self.controller.retrieveClientInformation(clientID)
        clientPhones = self.controller.retrieveClientPhoneNumbers(clientID)

        dfData = pd.DataFrame(clientData, columns=['Broker_Issuer', 'First_Name', 'Last_Name', 'Address', 'State', 'Zipcode'])
        dfPhones = pd.DataFrame(clientPhones, columns=['Phone_number'])

        dfPhonesTransposed = dfPhones.T

        dfPhonesTransposed.reset_index(drop=True, inplace=True)
        new_columns = ['Phone Number 1', 'Phone Number 2', 'Phone Number 3', 'Phone Number 4', 'Phone Number 5']
        dfPhonesTransposed.columns = new_columns[:len(dfPhones)]

        for column in new_columns[len(dfPhones):]:
            dfPhonesTransposed[column] = 'N/A'

        dfCombined = pd.concat([dfData, dfPhonesTransposed], axis=1)

        self.df = pd.concat([self.df, dfCombined], ignore_index=True)
        print(self.df)

    def loadAllClientData(self, userID):
        clientData = self.controller.retrieveAllClientID(userID)

        print(clientData)

        for clientID in clientData:
            clientID = clientID[0]
            self.processData(clientID)

    def loadAllUserLogs(self, userID):
        logData = self.controller.retrieveAllUserLogs(userID)
        dfData = pd.DataFrame(logData, columns=['logID', 'Broker_Issuer', 'Client_First_Name', 'interactionType', 'Date', 'Status'])
        self.df = pd.concat([self.df, dfData], ignore_index=True)

    def getDataFrame(self):
        return self.df