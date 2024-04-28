import DataScraperModel as model
from PandasModel import PandasModel
from View import View
class Controller:
    def __init__(self, userView, pandasModel):
        self.userView = userView
        self.pandasModel = pandasModel

    def loadDataFrame(self):
        self.pandasModel.processFile(model.getOutputName())

    def runScraper(self):
        model.main()

    def runWindow(self):
        self.userView.openWindow()

    def setFilename(self, filename):
        model.set_xlsx_file(filename)

    def getDataFrame(self):
        return self.pandasModel.getDataFrame()




