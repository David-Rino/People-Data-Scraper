# Author: Rino David
# Purpose: WebScraper with GUI for FastPeopleSearch.com

from Controller import Controller
from PandasModel import PandasModel
import tkinter as tk
from View import View

if __name__ == "__main__":
    userData = PandasModel()
    root = tk.Tk()
    userView = View(root)
    userController = Controller(userView, userData)
    # Used so the View has a way to contact the controller during runtime
    userView.setController(userController)
    userController.runWindow()



