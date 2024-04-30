import tkinter as tk
from pandastable import Table
class View:
    def __init__(self, root):
        self.root = root
        self.controller = None
        self.currentUser = None

        root.geometry("1000x500")
        root.title("Fast People Search Scraper")

        self.menuBar()
        self.userLogin()
        # self.setMainMenu()

    def menuBar(self):
        menubar = tk.Menu(self.root)
        self.file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Admin', menu=self.file)
        self.file.add_command(label='Reset Table', command=self.resetDatabase)
        self.file.add_command(label='Log Out', command=self.userLogout)
        self.file.add_separator()
        self.file.add_command(label='Exit', command=self.root.destroy)
        self.root.config(menu = menubar)

    def resetDatabase(self):
        # A needed restriction due to set-up constraints
        self.controller.resetDatabase()

    def userLogin(self):
        self.label = tk.Label(self.root, text="Enter userID", font=('Arial', 18))
        self.label.pack()

        self.textbox = tk.Text(self.root, height=2, font=('Arial', 16))
        self.textbox.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Login", font=('Arial', 16), command=self.loginButton)
        self.button.pack(padx=10, pady=10)

    def loginButton(self):
        self.currentUser = self.controller.retriveUser(self.textbox.get('1.0', tk.END).strip())

        self.label.pack_forget()
        self.textbox.pack_forget()
        self.button.pack_forget()

        if self.currentUser != None:
            self.controller.currentUserID = self.currentUser[0]
            self.user_label = tk.Label(self.root, text="Current User: " + self.currentUser[1] + " " + self.currentUser[2])
            self.user_label.pack(anchor="ne")
            self.setMainMenu()
        else:
            self.addUser()

    def userLogout(self):
        self.currentUser = None

        for widget in self.root.winfo_children():
            widget.destroy()

        self.userLogin()

    def addUser(self):
        self.label = tk.Label(self.root, text="Error: User Does Not Exist\nCreate a New Account Enter First and Last Name:", font=('Arial', 18))
        self.label.pack()

        self.textbox = tk.Text(self.root, height=2, font=('Arial', 16))
        self.textbox.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Create Account", font=('Arial', 16), command=self.addUserButton)
        self.button.pack(padx=10, pady=10)

    def addUserButton(self):
        previousUserNo = self.controller.retriveUserList(1)
        name = self.textbox.get('1.0', tk.END).strip().split()
        self.controller.addUser(previousUserNo[0][0] + 1, name[0].strip(), name[1].strip())

        self.currentUser = self.controller.retriveUser(previousUserNo[0][0] + 1)
        self.controller.currentUserID = self.currentUser[0]
        self.user_label = tk.Label(self.root, text="Current User: " + self.currentUser[1] + " " + self.currentUser[2])
        self.user_label.pack(anchor="ne")

        self.label.pack_forget()
        self.textbox.pack_forget()
        self.button.pack_forget()

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



