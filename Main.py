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
    # Will have to change to the system's database connection
    #userDatabase = SQLModel('localhost', 'DataScraper', 'postgres', 'Rd1258545', 5432)
    userDatabase = SQLModel('host.docker.internal', 'DataScraper', 'postgres', 'Rd1258545', 5432)
    userController = Controller(userView, userData, userDatabase, userDataScraper)
    # Used so the View has a way to contact the controller during runtime
    userView.setController(userController)
    userData.setController(userController)
    userDatabase.setController(userController)
    userDataScraper.setController(userController)

    # This Section of Commented Code is Used for testing for CS 333
    print("This Dockerfile has been created but for the purposes of the program view it will not work")
    print("Below is are table showing interaction logs, all clients")
    userData.loadAllUserLogs(1)
    print(userData.df.to_string())
    userController.resetDataFrame()
    userData.loadAllUserLogs(1)
    print(userData.df.to_string())

    userController.runWindow()



