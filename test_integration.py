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
        # Controller is the main facilator of the integration tests as it combines all models together.
        root = MagicMock()
        self.userView = View(root)
        self.pandasModel = PandasModel()
        database = MagicMock()
        self.SQLModel = SQLModel("test", "test", "test", "test", "test", connection=database)
        self.scraperModel = DataScraper()
        self.controller = Controller(self.userView, self.pandasModel, self.SQLModel, self.scraperModel)
        self.userView.setController(self.controller)
        self.pandasModel.setController(self.controller)


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
        self.userView.label.pack_forget.assert_called_once()
        self.userView.textbox.pack_forget.assert_called_once()
        self.userView.button.pack_forget.assert_called_once()


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
        self.SQLModel.retrieveUser.assert_called_once()

    @patch('View.Table')
    @patch('View.tk.Frame')
    @patch('View.tk.Label')
    @patch('View.tk.Button')
    def testIntegrationOpenInteractionLog(self, mock_button, mock_label, mock_frame, mock_table):
        self.userView.resetMenu = MagicMock()
        self.SQLModel.retrieveAllUserLogs = MagicMock()
        # Mocking the Database Return that Pandas Model will use in loadAllUserLogs
        self.SQLModel.retrieveAllUserLogs.return_value = [[1, 'Rino', 'Shino', 'David', '04-20-2024', 'Success']]

        self.userView.currentUser = [1, 'Rino', 'David']

        self.userView.openInteractionLog()

        mock_button.assert_called_once()
        mock_label.assert_called_once()
        mock_frame.assert_called_once()
        mock_table.assert_called_once()

        self.SQLModel.retrieveAllUserLogs.assert_called_once()

        #Retrive User Logs should have set data in the dataframe meaning it should have data if processed it correctly
        self.assertIsNotNone(self.pandasModel.df)

    @patch('View.Table')
    @patch('View.tk.Frame')
    @patch('View.tk.Label')
    @patch('View.tk.Button')
    def testIntegrationRunAndDisplayScrape(self, mock_button, mock_label, mock_frame, mock_table):
        # Mocking the scrape option that a user selects in which they provide a .xlsx file and starts the process
        # The scraping of the actual website is mocked as it is not possible to run it through GitHubActionsWorkflow

        self.userView.label = MagicMock()
        self.userView.textbox = MagicMock()
        self.userView.button = MagicMock()
        self.userView.mainMenu = MagicMock()

        self.userView.textbox.get.return_value = "sigma.xlsx"

        # The Mocking Section Where Scrape Would have taken place, mocking the purposes of run to see if interaction is proper
        self.scraperModel.run = MagicMock()

        self.SQLModel.addAddress = MagicMock()
        self.SQLModel.addClient = MagicMock()
        self.SQLModel.addInteractionLog = MagicMock()
        #Checks if the controller is properly callling SQLModel through the controller connection
        self.controller.addClient(2, 1, 'Shino', 'David', "Life", 21)
        self.controller.addAddress(2, 2, 'Test Rd 4200', 'NV', '88888')
        self.controller.addInteractionLog(2, 2, 1, 'Scrape', 'Sucesss')

        # Run Scrape
        self.userView.buttonPress()

        self.userView.label.pack_forget.assert_called_once()
        self.userView.textbox.pack_forget.assert_called_once()
        self.userView.button.pack_forget.assert_called_once()
        mock_button.assert_called_once()
        mock_label.assert_called_once()
        mock_frame.assert_called_once()
        mock_table.assert_called_once()

        self.scraperModel.run.assert_called_once()
        self.SQLModel.addAddress.assert_called_once()
        self.SQLModel.addClient.assert_called_once()
        self.SQLModel.addInteractionLog.assert_called_once()

    @patch('View.Table')
    @patch('View.tk.Frame')
    @patch('View.tk.Label')
    @patch('View.tk.Button')
    def testIntegrationOpenAllClients(self, mock_button, mock_label, mock_frame, mock_table):
        # Tests the Interaction of a user selecting open all clients and confirming all models are intergrating properly
        # THhe retrieval of information from the database is mocked, however the processing of the data is not
        self.userView.resetMenu = MagicMock()
        self.userView.currentUser = [1, 'Rino', 'David']

        self.SQLModel.retrieveAllClientID = MagicMock()
        self.SQLModel.retrieveAllClientID.return_value = [[1], [2], [3], [4], [5]]
        self.SQLModel.retrieveClientInformation = MagicMock()
        self.SQLModel.retrieveClientInformation.return_value = [['Rino', 'Shino', 'David', 'Test Address 4200', 'NV', '88888']]
        self.SQLModel.retrieveClientPhoneNumbers = MagicMock()
        self.SQLModel.retrieveClientPhoneNumbers.return_value =  [['111-111-1111'], ['222-222-2222'], ['333-333-3333'], ['444-444-4444'],]

        self.userView.openAllClients()

        mock_button.assert_called_once()
        mock_label.assert_called_once()
        mock_frame.assert_called_once()
        mock_table.assert_called_once()

        self.SQLModel.retrieveAllClientID.assert_called_once()
        self.SQLModel.retrieveClientInformation.assert_called_once()
        self.SQLModel.retrieveClientPhoneNumbers.assert_called_once()