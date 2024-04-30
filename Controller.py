from ScraperModel import DataScraper
from PandasModel import PandasModel
from View import View
from SQLModel import SQLModel
class Controller:
    def __init__(self, userView, pandasModel, SQLModel, DataScraperModel):
        self.userView = userView
        self.pandasModel = pandasModel
        self.SQLModel = SQLModel
        self.scraperModel = DataScraperModel
        self.currentUserID = None

    def loadDataFrame(self):
        self.pandasModel.processFile(self.scraperModel.xlsx_path)

    def runScraper(self):
        self.scraperModel.run()

    def runWindow(self):
        self.userView.openWindow()

    def setFilename(self, filename):
        self.scraperModel.set_xlsx_file(filename)

    def getDataFrame(self):
        return self.pandasModel.getDataFrame()

    def retrieveUser(self, user_id):
        return self.SQLModel.retrieveUser(user_id)

    def retrieveUserList(self, amount):
        return self.SQLModel.retrieveUserList(amount)

    def addUser(self, userID, firstName, lastName):
        return self.SQLModel.addUser(userID, firstName, lastName)

    def addClient(self, clientID, currentUserID, firstName, lastName, typeOfInsurance, age):
        return self.SQLModel.addClient(clientID, currentUserID, firstName, lastName, typeOfInsurance, age)

    def retrieveClients(self, amount):
        return self.SQLModel.retrieveClients(amount)

    def addPhone(self, phoneID, clientID, phoneNumber):
        return self.SQLModel.addPhone(phoneID, clientID, phoneNumber)

    def retrievePhones(self, amount):
        return self.SQLModel.retrievePhones(amount)

    def addAddress(self, propertyID, clientID, address, state, zipcode):
        return self.SQLModel.addAddress(propertyID, clientID, address, state, zipcode)

    def retrieveAddresses(self, amount):
        return self.SQLModel.retrieveAddresses(amount)

    def resetDatabase(self):
        return self.SQLModel.resetDatabase()

    def retrieveClientInformation(self, clientID):
        return self.SQLModel.retrieveClientInformation(clientID)

    def retrieveClientPhoneNumbers(self, clientID):
        return self.SQLModel.retrieveClientPhoneNumbers(clientID)

    def processData(self, clientID):
        return self.pandasModel.processData(clientID)

    def resetDataFrame(self):
        self.pandasModel.df = None







