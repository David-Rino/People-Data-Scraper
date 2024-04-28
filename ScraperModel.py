import os
import time

from openpyxl import load_workbook

import undetected_chromedriver as uc

import bs4

class ScraperModel:

    def __init__(self):
        self.chromedriver_path = "chromedriver.exe"
        self.xlsx_path = "data.xlsx"
        self.CURR_SCRIPT_PATH = os.path.realpath(os.path.dirname(__file__))
        self.profile_path = self.CURR_SCRIPT_PATH + "\\profile"

        self.FIRST_NAME_COL = 'A'
        self.LAST_NAME_COL = 'B'
        self.ADDRESS_COL = 'K'
        self.PHONEs_COLs = ['L', 'M', 'N', 'O', 'P']

    def open_chrome_with_profile(self):
        options = uc.ChromeOptions()
        options.add_argument("--user-data-dir=" + self.profile_path)

        driver = uc.Chrome(driver_executable_path=self.chromedriver_path)
        return driver

    def set_xlsx_file(self, filename):
        self.xlsx_path = filename

    def open_xlsx_file(self):
        wb = load_workbook(filename = self.xlsx_path)
        ws = wb.active
        return wb, ws

    def write_phones_to_xlsx_file(self, wb, ws, phones, row):

        #Limit the amount of phone numbers to 5
        phoneLength = len(phones)
        if phoneLength >= 5:
            phoneLength = 5

        for i in range(phoneLength):
            ws[self.PHONEs_COLs[i] + str(row)].value = phones[i]

        wb.save(self.xlsx_path)

    def extract_phones_from_page(self, page_source):
        phones = []

        try:
            # Attempt to find phones
            soup = bs4.BeautifulSoup(page_source, "html.parser")
            a_tags = soup.find_all("a", title=lambda x: x and "Search people with phone number" in x)
            for a_tag in a_tags:
                phone = a_tag.text.strip()
                phones.append(phone)

                return phones

        except Exception as e:
            print(str(e))
            return phones

    def getOutputName(self):
        return self.xlsx_path

    def run(self):
        driver = self.open_chrome_with_profile()
        driver.get("https://www.fastpeoplesearch.com/")

        if "Access Denied" in driver.page_source:
            print("Access Denied")
            time.sleep(60)
            driver.get("https://www.fastpeoplesearch.com/")
            if "Access Denied" in driver.page_source:
                return 1

            wb, ws = self.open_xlsx_file()

            for row in range(2, ws.max_row + 1):

                try:
                    first_name = ws[self.FIRST_NAME_COL + str(row)].value
                    last_name = ws[self.LAST_NAME_COL + str(row)].value
                    address = ws[self.ADDRESS_COL + str(row)].value

                    if (first_name is None and last_name is None) or address is None:
                        continue

                    first_name = first_name.replace(" ", "-")
                    last_name = last_name.replace(" ", "-")
                    address = address.replace(" ", "-")
                    driver.get("https://www.fastpeoplesearch.com/name/" + first_name + "-" + last_name + "-" + address)

                except Exception as e:
                    print(str(e))
                    continue



