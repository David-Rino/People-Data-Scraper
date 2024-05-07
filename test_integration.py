import datetime
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from SQLModel import SQLModel
from PandasModel import PandasModel
from ScraperModel import DataScraper
from Controller import  Controller
from View import View

# Mocking will be used for database and GUI was github actions workflow will not work as Erin stated
# Intergration functionality will be tested still
# Webscraping will also be mocked when tested however the other functions of a scraper model will not.
class intergrationTest(unittest.TestCase):

    def setUp(self):
        root = MagicMock()
        self.userView = View(root)
        self.pandasModel = PandasModel()
        database = MagicMock()
        self.SQLModel = SQLModel("test", "test", "test", "test", "test", connection=database)
        self.scraperModel = DataScraper()

        self.controller = Controller(self.userView, self.pandasModel, self.SQLModel, self.scraperModel)
        self.userView.setController(self.controller)

    @patch('tkinter.Label')
    def testUserLoginExists(self, mock_label):
        # Intergration Tests That Checks that when a user Logs and provides a username that it will call controller
        # In which controller will call the SQL Database (Which the expected return  value is mocked)
        # After It will check if userView Properly Calls self.mainMenu()
        self.userView.label = MagicMock()
        self.userView.textbox = MagicMock()
        self.userView.button = MagicMock()
        self.userView.mainMenu = MagicMock()

        self.userView.textbox.get.return_value = "1"
        self.SQLModel.retrieveUser = MagicMock()
        self.SQLModel.retrieveUser.return_value = [1, 'Rino', 'David']

        self.userView.loginButton()

        mock_label.assert_called_with(self.userView.root, text="Current User: Rino David")
        self.userView.mainMenu.assert_called_once()

    def testUserLoginDoesNotExists(self):
        # Intergration Tests That Checks that when a user Logs and provides a username that is NOT VALID that it will call controller
        # In which controller will call the SQL Database which return a mocked value of none
        #When None uservalue should return
        self.userView.label = MagicMock()
        self.userView.textbox = MagicMock()
        self.userView.button = MagicMock()
        self.userView.addUser = MagicMock()

        self.userView.textbox.get.return_value = "1"
        self.SQLModel.retrieveUser = MagicMock()
        self.SQLModel.retrieveUser.return_value = None

        self.userView.loginButton()

        self.userView.addUser.assert_called_once()
