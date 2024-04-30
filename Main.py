# Author: Rino David
# Purpose: WebScraper with GUI for FastPeopleSearch.com

from Controller import Controller
from PandasModel import PandasModel
from SQLModel import SQLModel
from ScraperModel import DataScraper
import tkinter as tk
from View import View

if __name__ == "__main__":
    userData = PandasModel()
    root = tk.Tk()
    userView = View(root)
    userDataScraper = DataScraper()
    userDatabase = SQLModel('localhost', 'DataScraper', 'postgres', 'Rd1258545', 5432)
    userController = Controller(userView, userData, userDatabase, userDataScraper)
    # Used so the View has a way to contact the controller during runtime
    userView.setController(userController)
    userData.setController(userController)
    userDatabase.setController(userController)
    userDataScraper.setController(userController)
    userController.runWindow()



