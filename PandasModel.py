import pandas as pd

class PandasModel:
    def __init__(self):
        self.df = None

    def processFile(self, file_path):
        try:
            self.df = pd.read_excel(file_path)
            print(self.df)
        except Exception as e:
            print(f"Error reading the Excel file: {e}")

    def getDataFrame(self):
        return self.df