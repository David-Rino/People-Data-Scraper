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

    def retriveUser(self, user_id):
        return self.SQLModel.retriveUser(user_id)

    def retriveUserList(self, amount):
        return self.SQLModel.retriveUserList(amount)

    def addUser(self, userID, firstName, lastName):
        return self.SQLModel.addUser(userID, firstName, lastName)

    def addClient(self, clientID, currentUserID, firstName, lastName, typeOfInsurance, age):
        return self.SQLModel.addClient(clientID, currentUserID, firstName, lastName, typeOfInsurance, age)

    def retriveClients(self, amount):
        return self.SQLModel.retriveClients(amount)

    def addPhone(self, phoneID, clientID, phoneNumber):
        return self.SQLModel.addPhone(phoneID, clientID, phoneNumber)

    def retrivePhones(self, amount):
        return self.SQLModel.retrivePhones(amount)

    def addAddress(self, propertyID, clientID, address, state, zipcode):
        return self.SQLModel.addAddress(propertyID, clientID, address, state, zipcode)

    def retriveAddresses(self, amount):
        return self.SQLModel.retriveAddresses(amount)







