import datetime
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from SQLModel import SQLModel
from PandasModel import PandasModel
from ScraperModel import DataScraper
from Controller import  Controller

class SQLModelTests(unittest.TestCase):
    def setUp(self):
        self.userConnection = MagicMock()
        self.db = SQLModel('test', 'test', 'test', 'test', 1, self.userConnection)

    def testSetController(self):
        controller = "test"
        self.db.setController(controller)
        self.assertEqual(self.db.controller, controller)

    def testResetDatabaseSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor

        self.db.resetDatabase()

        mock_cursor.execute.assert_called_once()
        self.userConnection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testResetDatabaseFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")

        self.db.resetDatabase()

        mock_cursor.execute.assert_called_once()
        mock_print.assert_called_with("Database error")

    @patch('psycopg.connect')
    def testMakeConnSuccess(self, mock_connect):

        mock_connect.return_value = MagicMock()

        conn = self.db.makeConn()

        mock_connect.assert_called_once_with(host='test', dbname='test', user='test', password='test', port=1)

        self.assertIsNotNone(conn)

    @patch('psycopg.connect')
    @patch('builtins.print')
    def testMakeConnFailure(self, mock_print, mock_connect):

        mock_connect.side_effect = Exception("Connection Failed")

        conn = self.db.makeConn()

        mock_connect.assert_called_once_with(host='test', dbname='test', user='test', password='test', port=1)
        self.assertIsNone(conn)
        mock_print.assert_called_with("Connection Failed")

    def testAddUserSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor

        self.db.addUser(1, 'Shino', 'David')

        expectedSQL = (f"""
                INSERT INTO users (user_id, first_name, last_name)
                VALUES (1, 'Shino', 'David')
            """)
        mock_cursor.execute.assert_called_once_with(expectedSQL)
        mock_cursor.close.assert_called_once()
        self.userConnection.commit.assert_called_once()

    @patch('builtins.print')
    def testAddUserFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Failed to Insert User")

        self.db.addUser(1, 'Shino', 'David')
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_print.assert_called_with("Failed to Insert User")

    def testRetrieveUserSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [(1, 'Shino', 'David')]
        mock_cursor.fetchone.return_value = expected_data

        result = self.db.retrieveUser(1)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testRetrieveUserFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = Exception("Database Error")

        result = self.db.retrieveUser(1)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")

    def testRetrieveUserListSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [(1, 'Shino', 'David'), (2, 'Rion', 'David')]
        mock_cursor.fetchall.return_value = expected_data

        result = self.db.retrieveUserList(2)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testRetrieveUserListFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Database Error")

        result = self.db.retrieveUserList(2)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")

    def testAddClientSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor

        self.db.addClient(1, 1, 'Shion', 'David', 'Health', 21)

        expectedSQL = (f"""
                INSERT INTO clients (clientID, brokerIssuer, first_name, last_name, type_of_insurance, age)
                VALUES (1, 1, 'Shion', 'David', 'Health', '21')
            """)
        mock_cursor.execute.assert_called_once_with(expectedSQL)
        mock_cursor.close.assert_called_once()
        self.userConnection.commit.assert_called_once()

    @patch('builtins.print')
    def testAddClientFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Failed to Insert Client")

        self.db.addClient(1, 1, 'Shion', 'David', 'Health', 21)
        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_print.assert_called_with("Failed to Insert Client")

    def testRetrieveClientsSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [(1, 1, 'Shion', 'David', 'Health', 21), (2, 1, 'Rion', 'David', 'Health', 21)]
        mock_cursor.fetchall.return_value = expected_data

        result = self.db.retrieveClients(2)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testRetrieveClientsFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Database Error")

        result = self.db.retrieveClients(2)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")

    def testRetrieveAllClientIDSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [(1), (2), (3), (4)]
        mock_cursor.fetchall.return_value = expected_data

        result = self.db.retrieveAllClientID(1)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testRetrieveAllClientIDFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Database Error")

        result = self.db.retrieveAllClientID(1)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")

    def testAddPhoneSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor

        self.db.addPhone(1, '1', '777-777-7777')

        expectedSQL = (f"""
                INSERT INTO phonenumbers (phoneID, clientID, phone_number)
                VALUES (1, '1', '777-777-7777')
            """)

        mock_cursor.execute.assert_called_once_with(expectedSQL)
        mock_cursor.close.assert_called_once()
        self.userConnection.commit.assert_called_once()

    @patch('builtins.print')
    def testAddPhoneFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database Error")

        result = self.db.addPhone(1, '1', '777-777-7777')

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")

    def testRetrievePhonesSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [(1, '1', '777-777-7777'), (2, '1', '888-888-8888')]
        mock_cursor.fetchall.return_value = expected_data

        result = self.db.retrievePhones(2)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testRetrievePhoneFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Database Error")

        result = self.db.retrievePhones(2)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")

    def testAddAddressSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor

        self.db.addAddress(1, '1', 'Sigma Ohio 4200', 'OH', '88888')

        expectedSQL = (f"""
                INSERT INTO property (propertyID, clientID, address, state, zipcode)
                VALUES (1, '1', 'Sigma Ohio 4200', 'OH', '88888')
            """)

        mock_cursor.execute.assert_called_once_with(expectedSQL)
        mock_cursor.close.assert_called_once()
        self.userConnection.commit.assert_called_once()

    @patch('builtins.print')
    def testAddAddressFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Failed to Add Address")

        result = self.db.addAddress(1, '1', 'Sigma Ohio 4200', 'OH', '88888')

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Failed to Add Address")

    def testRetrieveAddressesSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [(1, '1', 'Sigma Ohio 4200', 'OH', '88888'), (2, '2', 'Fanum Rd 8008', 'TN', '77777')]
        mock_cursor.fetchall.return_value = expected_data

        result = self.db.retrieveAddresses(2)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testRetrieveAddressesFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Database Error")

        result = self.db.retrieveAddresses(2)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")

    def testRetrieveClientInformationSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [('Shino', 'Rion', 'David', 'Sigma Ohio 4200', 'OH', '88888')]
        mock_cursor.fetchall.return_value = expected_data
        mock_controller = MagicMock()
        mock_controller.currentUserID(1)
        self.db.controller = mock_controller

        result = self.db.retrieveClientInformation(1)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testRetrieveClientInformationFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Database Error")
        mock_controller = MagicMock()
        mock_controller.currentUserID(1)
        self.db.controller = mock_controller

        result = self.db.retrieveClientInformation(1)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")

    def testRetrieveClientPhoneNumbersSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [('111-111-1111'), ('222-222-222'), ('333-333-3333'), ('444-444-4444'), ('555-555-5555')]
        mock_cursor.fetchall.return_value = expected_data

        result = self.db.retrieveClientPhoneNumbers(1)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testretrieveClientPhoneNumbersFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Database Error")

        result = self.db.retrieveClientPhoneNumbers(1)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")

    def testRetrieveLogsSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [(1, '2', '1', 'Scrape', '2024-05-01', 'Success'), (2, '3', '1', 'Scrape', '2024-05-01', 'Success')]
        mock_cursor.fetchall.return_value = expected_data

        result = self.db.retrieveLogs(2)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testRetrieveLogsFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = Exception("Database Error")

        result = self.db.retrieveLogs(2)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database Error")
    def testRetrieveAllUserLogsSuccess(self):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        expected_data = [(1, 'Joe', 'Mama', 'Scrape', '04-20-2024', 'Success')]
        mock_cursor.fetchall.return_value = expected_data

        result = self.db.retrieveAllUserLogs(1)

        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_data)
        mock_cursor.close.assert_called_once()

    @patch('builtins.print')
    def testRetrieveAllUserLogsFailure(self, mock_print):

        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Database error")

        result = self.db.retrieveAllUserLogs(1)

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Database error")

    @patch('SQLModel.datetime')
    def testAddInteractionLogSuccess(self, mock_datetime):

        day = datetime.datetime(2024, 4, 20)
        mock_datetime.datetime.now.return_value = day
        mock_datetime.now.return_value.strftime.return_value = '04-20-2024'

        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor

        self.db.addInteractionLog(1, '1', '1', 'Scrape', 'Success')

        expectedSQL = (f"""
                INSERT INTO interaction_logs (logID, clientID, userID, interactiontype, datechanged, status)
                VALUES (1, 1, 1, 'Scrape', '04-20-2024', 'Success');
            """)
        mock_cursor.execute.assert_called_once_with(expectedSQL)
        mock_cursor.close.assert_called_once()
        self.userConnection.commit.assert_called_once()

    @patch('builtins.print')
    def testAddInteractionLogFailure(self, mock_print):
        mock_cursor = MagicMock()
        self.userConnection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Failed to Add Interaction Log")

        result = self.db.addInteractionLog(1, '1', '1', 'Scrape', 'Success')

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        self.assertIsNone(result)
        mock_print.assert_called_with("Failed to Add Interaction Log")

class PandasModelTests(unittest.TestCase):

    def setUp(self):
        self.pandas = PandasModel()

    def testSetController(self):
        controller = "test"
        self.pandas.setController(controller)
        self.assertEqual(self.pandas.controller, controller)

    @patch('pandas.read_excel')
    def testProcessFileSuccess(self, mock_read_excel):
        mock_df = pd.DataFrame({
            'Test1': [1, 2, 3],
            'Test2': ['A', 'B', 'C']
        })
        mock_read_excel.return_value = mock_df

        self.pandas.processFile('Sigma.xlsx')

        mock_read_excel.assert_called_once_with('Sigma.xlsx')
        pd.testing.assert_frame_equal(self.pandas.df, mock_df)

    @patch('pandas.read_excel')
    @patch('builtins.print')
    def testProcessFileError(self, mock_print, mock_read_excel):
        mock_read_excel.side_effect = Exception("Failed to Read .xlsx")

        self.pandas.processFile('Sigma.xlsx')

        mock_read_excel.assert_called_once_with('Sigma.xlsx')
        mock_print.assert_called_with("Failed to Read .xlsx")

    def testProcessDataSuccess(self):

        clientInfo = [['Rino', 'Shino', 'David', 'Sigma Ohio 420', 'OH', '88888']]

        clientPhones = [
            ['111-111-1111'],
            ['222-222-2222'],
            ['333-333-3333'],
            ['444-444-4444'],
        ]

        mock_controller = MagicMock()
        mock_controller.retrieveClientInformation.return_value = clientInfo
        mock_controller.retrieveClientPhoneNumbers.return_value = clientPhones
        self.pandas.controller = mock_controller

        self.pandas.processData(1)

        expectedData = [['Rino', 'Shino', 'David', 'Sigma Ohio 420', 'OH', '88888', '111-111-1111', '222-222-2222', '333-333-3333', '444-444-4444', 'N/A']]

        # Simulating the processing within process Data
        expectedDfData = pd.DataFrame(expectedData, columns=['Broker_Issuer', 'First_Name', 'Last_Name', 'Address', 'State', 'Zipcode', 'Phone Number 1', 'Phone Number 2', 'Phone Number 3', 'Phone Number 4', 'Phone Number 5'])

        pd.testing.assert_frame_equal(self.pandas.df,expectedDfData)

        self.pandas.controller.retrieveClientInformation.assert_called_once_with(1)
        self.pandas.controller.retrieveClientPhoneNumbers.assert_called_once_with(1)

    def testLoadAllUserLogs(self):

        logData = [['1', 'Rino', 'Shion' 'David', 'Scrape', '04-20-2024', 'Success']]

        mock_controller = MagicMock()
        mock_controller.retrieveAllUserLogs.return_value = logData
        self.pandas.controller = mock_controller

        expectedDFData = pd.DataFrame(logData, columns=['logID', 'Broker_Issuer', 'Client_First_Name', 'interactionType', 'Date', 'Status'])

        self.pandas.loadAllUserLogs(1)

        self.pandas.controller.retrieveAllUserLogs.assert_called_once_with(1)
        pd.testing.assert_frame_equal(self.pandas.df, expectedDFData)

    def testGetDataFrame(self):
        result = self.pandas.getDataFrame()

        self.assertIsNone(result)

class ScraperModelsTest(unittest.TestCase):

    def setUp(self):
        self.scraper = DataScraper()

    def testSetController(self):
        controller = "test"
        self.scraper.setController(controller)
        self.assertEqual(self.scraper.controller, controller)

    def testSetXlsxFile(self):
        filename = "Sigma.xlsx"
        self.scraper.set_xlsx_file(filename)
        self.assertEqual(self.scraper.xlsx_path, filename)

    @patch('ScraperModel.load_workbook')
    def testOpenXlsxFile(self, mock_load_workbook):
        self.scraper.xlsx_path = "Sigma.xlsx"

        mock_workbook = MagicMock()
        mock_worksheet = MagicMock()
        mock_workbook.active.return_value = mock_worksheet
        mock_load_workbook.return_value = mock_workbook

        wb, ws = self.scraper.open_xlsx_file()

        mock_load_workbook.assert_called_once_with("Sigma.xlsx")

    def test_savePhonesToDatabase(self):
        controller = MagicMock()
        controller.retrievePhones(1)[0][0].return_value = 1

        clientID = 123
        phones = ["1234567890", "0987654321", "1112223333", "4445556666", "7778889999", "0001112222"]
        controller.addPhone.return_value = "Success"
        self.scraper.controller = controller
        self.scraper.savePhonesToDatabase(clientID, phones)
        controller.addPhone.assert_called()


class ControllerTest(unittest.TestCase):

    def setUp(self):
        self.userView = MagicMock()
        self.pandasModel = MagicMock()
        self.SQLModel = MagicMock()
        self.scraperModel = MagicMock()

        self.controller = Controller(self.userView, self.pandasModel, self.SQLModel, self.scraperModel)

    def testLoadDataFrame(self):
        self.scraperModel.xlsx_path = "Test"
        self.controller.loadDataFrame()
        self.pandasModel.processFile.assert_called_once()

    def testRunScraper(self):
        self.controller.runScraper()
        self.scraperModel.run.assert_called_once()

    def testRunWindow(self):
        self.controller.runWindow()
        self.userView.openWindow.assert_called_once()

    def testSetFilename(self):
        self.controller.setFilename("goonmaxxing.xlsx")
        self.scraperModel.set_xlsx_file.assert_called_once()

    def testGetDataFrame(self):
        self.pandasModel.getDataFrame.return_value = "Bowomp"
        result = self.controller.getDataFrame()
        self.assertEqual(result, "Bowomp")

    def testRetrieveUser(self):
        self.SQLModel.retrieveUser.return_value = "Ermm... What the Sigma"
        result = self.controller.retrieveUser(1)
        self.assertEqual(result, "Ermm... What the Sigma")

    def testRetrieveUserList(self):
        self.SQLModel.retrieveUserList.return_value = "Fanum Tax"
        result = self.controller.retrieveUserList(2)
        self.assertEqual(result, "Fanum Tax")

    def testAddUser(self):
        self.SQLModel.addUser.return_value = "Drake"
        result = self.controller.addUser(1, "Shino", "Machi")
        self.assertEqual(result, "Drake")

    def testAddClient(self):
        self.SQLModel.addClient.return_value = "SakiSaki"
        result = self.controller.addClient(1, 1, "Shino", "Kiryuu", "Love", 21)
        self.assertEqual(result, "SakiSaki")

    def testRetrieveClients(self):
        self.SQLModel.retrieveClients.return_value = "Hody Jones"
        result = self.controller.retrieveClients(1)
        self.assertEqual(result, "Hody Jones")

    def testAddPhone(self):
        self.SQLModel.addPhone.return_value = "Towa"
        result = self.controller.addPhone(1, 1, '111-111-1111')
        self.assertEqual(result, "Towa")

    def testRetrievePhones(self):
        self.SQLModel.retrievePhones.return_value = "Suisei"
        result = self.controller.retrievePhones(1)
        self.assertEqual(result, "Suisei")

    def testAddAddress(self):
        self.SQLModel.addAddress.return_value = "Arona"
        result = self.controller.addAddress(1, 1, "Sigma Ohio", "NV", "99999")
        self.assertEqual(result, "Arona")

    def testRetrieveAddresses(self):
        self.SQLModel.retrieveAddresses.return_value = "Plana"
        result = self.controller.retrieveAddresses(1)
        self.assertEqual(result, "Plana")

    def testResetDatabase(self):
        self.SQLModel.resetDatabase.return_value = "Yuuka"
        result = self.controller.resetDatabase()
        self.assertEqual(result, "Yuuka")

    def testRetrieveClientInformation(self):
        self.SQLModel.retrieveClientInformation.return_value = "Rio"
        result = self.controller.retrieveClientInformation(100)
        self.assertEqual(result, "Rio")

    def testRetrieveClientPhoneNumbers(self):
        self.SQLModel.retrieveClientPhoneNumbers.return_value = "Haruna"
        result = self.controller.retrieveClientPhoneNumbers(1)
        self.assertEqual(result, "Haruna")

    def testProcessData(self):
        self.pandasModel.processData.return_value = "Hoshino"
        result = self.controller.processData(1)
        self.assertEqual(result, "Hoshino")

    def testResetDataFrame(self):
        self.controller.resetDataFrame()
        self.assertIsNone(self.pandasModel.df)

    def testRetrieveAllClientID(self):
        self.SQLModel.retrieveAllClientID.return_value = "Robin"
        result = self.controller.retrieveAllClientID(1)
        self.assertEqual(result, "Robin")

    def testLoadAllClientData(self):
        self.pandasModel.loadAllClientData.return_value = "Topaz"
        result = self.controller.loadAllClientData(1)
        self.assertEqual(result, "Topaz")

    def testRetrieveLogs(self):
        self.SQLModel.retrieveLogs.return_value = "Jade"
        result = self.controller.retrieveLogs(1)
        self.assertEqual(result, "Jade")

    def testRetrieveAllUserLogs(self):
        self.SQLModel.retrieveAllUserLogs.return_value = "Acheron"
        result = self.controller.retrieveAllUserLogs(1)
        self.assertEqual(result, "Acheron")

    def testAddInteractionLogs(self):
        self.SQLModel.addInteractionLog.return_value = "Sparkle"
        result = self.controller.addInteractionLog(1, 1, 1, 'Gacha', 'Win')
        self.assertEqual(result, "Sparkle")

    def testLoadAllUserLogs(self):
        self.pandasModel.loadAllUserLogs.return_value = "Sliver Wolf"
        result = self.controller.loadAllUserLogs(1)
        self.assertEqual(result, "Sliver Wolf")










if __name__ == '__main__':
    unittest.main()