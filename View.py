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

    def mainMenu(self):
        self.label = tk.Label(self.root, text="Welcome " + self.currentUser[1] + " , Please Choose an Option", font=('Arial', 18))
        self.label.pack()

        self.buttonFrame = tk.Frame(self.root)
        self.buttonFrame.pack(pady=20)

        self.interactionLogs = tk.Button(self.buttonFrame, text = "Interaction Logs", font=('Arial', 16), command= self.openInteractionLog)
        self.interactionLogs.pack(side=tk.LEFT, padx = 10)

        self.allClients = tk.Button(self.buttonFrame, text = "View All Clients", font=('Arial', 16), command= self.openAllClients)
        self.allClients.pack(side=tk.LEFT, padx = 10)

        self.scrape = tk.Button(self.buttonFrame, text = "Start Scrape", font=('Arial', 16), command= self.setImportMenu)
        self.scrape.pack(side=tk.LEFT, padx=10)

    def openAllClients(self):
        self.resetMenu()
        self.controller.loadAllClientData(self.currentUser[0])
        self.displayPhones()

    def openInteractionLog(self):
        self.resetMenu()
        self.controller.resetDataFrame()
        self.controller.loadAllUserLogs(self.currentUser[0])
        self.displayLogs()

    def displayLogs(self):
        self.sheetTable = tk.Label(self.root, text="List of User Logs for: " + self.currentUser[1], font=('Arial', 18))
        self.sheetTable.pack()

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.table = Table(self.frame, dataframe=self.controller.getDataFrame())
        self.table.show()

        self.resetButton = tk.Button(self.root, text="Main Menu", font=('Arial', 16), command=self.resetTable)
        self.resetButton.pack(padx=10, pady=10)

    def resetMenu(self):
        self.label.pack_forget()
        self.buttonFrame.pack_forget()
        self.interactionLogs.pack_forget()
        self.allClients.pack_forget()
        self.scrape.pack_forget()

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
        self.currentUser = self.controller.retrieveUser(self.textbox.get('1.0', tk.END).strip())

        self.label.pack_forget()
        self.textbox.pack_forget()
        self.button.pack_forget()

        if self.currentUser != None:
            self.controller.currentUserID = self.currentUser[0]
            self.user_label = tk.Label(self.root, text="Current User: " + self.currentUser[1] + " " + self.currentUser[2])
            self.user_label.pack(anchor="ne")
            self.mainMenu()
            #self.setImportMenu()
        else:
            self.addUser()

    def userLogout(self):
        self.currentUser = None

        for widget in self.root.winfo_children():
            widget.destroy()

        self.menuBar()
        self.userLogin()

    def addUser(self):
        self.label = tk.Label(self.root, text="Error: User Does Not Exist\nCreate a New Account Enter First and Last Name:", font=('Arial', 18))
        self.label.pack()

        self.textbox = tk.Text(self.root, height=2, font=('Arial', 16))
        self.textbox.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Create Account", font=('Arial', 16), command=self.addUserButton)
        self.button.pack(padx=10, pady=10)

    def addUserButton(self):
        previousUserNo = self.controller.retrieveUserList(1)

        if previousUserNo == []:
            self.controller.addUser(1, "Test", "User")
            previousUserNo = self.controller.retrieveUserList(1)

        name = self.textbox.get('1.0', tk.END).strip().split()
        self.controller.addUser(previousUserNo[0][0] + 1, name[0].strip(), name[1].strip())

        self.currentUser = self.controller.retrieveUser(previousUserNo[0][0] + 1)
        self.controller.currentUserID = self.currentUser[0]
        self.user_label = tk.Label(self.root, text="Current User: " + self.currentUser[1] + " " + self.currentUser[2])
        self.user_label.pack(anchor="ne")

        self.label.pack_forget()
        self.textbox.pack_forget()
        self.button.pack_forget()

        self.mainMenu()


    def setImportMenu(self):
        self.resetMenu()

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
        #self.controller.loadDataFrame()
        self.label.pack_forget()
        self.textbox.pack_forget()
        self.button.pack_forget()
        self.displayPhones()

    def resetTable(self):
        self.sheetTable.pack_forget()
        self.frame.pack_forget()
        self.table.pack_forget()
        self.resetButton.pack_forget()
        self.controller.resetDataFrame()
        self.mainMenu()

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




