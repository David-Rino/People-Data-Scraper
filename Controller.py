from ScraperModel import DataScraper
from PandasModel import PandasModel
from View import View
from SQLModel import SQLModel
class Controller:
    def __init__(self, userView, pandasModel, SQLModel):
        self.userView = userView
        self.pandasModel = pandasModel
        self.SQLModel = SQLModel
        self.scraperModel = DataScraper()

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







