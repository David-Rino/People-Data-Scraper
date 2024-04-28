import tkinter as tk
from pandastable import Table
class View:
    def __init__(self, root):
        self.root = root
        self.controller = None

        root.geometry("1000x500")
        root.title("Fast People Search Scraper")

        self.setMainMenu()

    def setMainMenu(self):
        self.label = tk.Label(self.root, text="Please Enter Import File (include file extension)", font=('Arial', 18))
        self.label.pack()

        self.textbox = tk.Text(self.root, height=2, font=('Arial', 16))
        self.textbox.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Import File & Start", font=('Arial', 16), command=self.buttonPress)
        self.button.pack(padx=10, pady=10)

    def setController(self, controller):
        self.controller = controller

    def buttonPress(self):
        self.controller.setFilename(self.textbox.get('1.0', tk.END))
        self.controller.runScraper()
        self.controller.loadDataFrame()
        self.label.pack_forget()
        self.textbox.pack_forget()
        self.button.pack_forget()
        self.displayPhones()

    def resetTable(self):
        self.sheetTable.pack_forget()
        self.frame.pack_forget()
        self.table.pack_forget()
        self.resetButton.pack_forget()
        self.setMainMenu()

    def displayPhones(self):
        self.sheetTable = tk.Label(self.root, text="List of Phone Numbers", font=('Arial', 18))
        self.sheetTable.pack()

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.table = Table(self.frame, dataframe=self.controller.getDataFrame())
        self.table.show()

        self.resetButton = tk.Button(self.root, text="Reset?", font=('Arial', 16), command=self.resetTable)
        self.resetButton.pack(padx=10, pady=10)


    def openWindow(self):
        self.root.mainloop()



