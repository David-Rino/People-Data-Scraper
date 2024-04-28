from ScraperModel import DataScraper
from PandasModel import PandasModel
from View import View
class Controller:
    def __init__(self, userView, pandasModel):
        self.userView = userView
        self.pandasModel = pandasModel
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




