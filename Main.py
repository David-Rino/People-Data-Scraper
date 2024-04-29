# Author: Rino David
# Purpose: WebScraper with GUI for FastPeopleSearch.com

from Controller import Controller
from PandasModel import PandasModel
from SQLModel import  SQLModel
import tkinter as tk
from View import View

if __name__ == "__main__":
    userData = PandasModel()
    root = tk.Tk()
    userView = View(root)
    userDatabase = SQLModel('localhost', 'DataScraper', 'postgres', 'Rd1258545', 5432)
    userController = Controller(userView, userData, userDatabase)
    # Used so the View has a way to contact the controller during runtime
    userView.setController(userController)
    userDatabase.setController(userController)
    userController.runWindow()



