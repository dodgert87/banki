from menu import Menu
from art import *
from help import Help
from database import DB_manger
from tabulate import tabulate
import time


class MenuMain(Menu): 
   
    help_menu: Help
    def __init__(self,account,submenu,) -> None:
        super().__init__(options=[
            { "description": "Add Account", "action": self.add_account },
            { "description": "View Accounts", "action": self.view_account },
            { "description": "Transfer money", "action": self.transfer },
            { "description": "View transaction", "action": self.view_transaction },
            {"description": "Help?", "action": self.openHelpMenu }
        ])
        description="in this menu, you have the ability to add accounts and view all your accounts\n, perform a transaction, and view a record of your transaction. "
        common_problem=["problem creating account: make sure you enter a valid account number in the correct format as shown.",
                        "problem making transaction: make sure you suffusion funds and the correspondent bank account is valid.",
                        "problem viewing transaction: make sure that the transaction was performed successfully and that you choose the correct one."]
        self.help_menu = Help(description,common_problem)
        self.submenu = submenu
        self.account = account
        self.db_manger = DB_manger()
        
        return None
    def openHelpMenu(self) -> None:
        self.help_menu.start()
        return None
    def add_account(self) -> None:
        self.clear_screen()
        print(add_Account)
        Continue = True
        bank_name = input("Enter a bank name or -1 to cancel: ")
        if bank_name == "-1":
            Continue = False
        while Continue:
            account_number = input("Enter your account number (XX-10-digit number) or -1 to cancel: ")

            if account_number == -1:
                Continue = False
                break
            elif account_number[2:].isdigit() and len(account_number) == 12 and account_number[0:2].isalpha():
                break
            else:
                print("Invalid account number format. Please enter a XX-10-digit number.")

        while Continue:
            try:
                initial_balance = float(input("Enter an initial balance or -1 to cancel: "))
                break 

            except ValueError:
                print("Invalid balance. Please enter a numeric value.")

        if Continue:
            if initial_balance > -1:
                self.clear_screen()
                self.db_manger.commit_acount(self.account[0],bank_name,account_number,initial_balance)
                print(account_added)
                time.sleep(1.5)
        return None
    
    def view_account(self) -> None:

        self.clear_screen()
        print(view_account)
        self.bank_accounts = self.db_manger.get_banckaccount(self.account[0])
        
        accounts=[]
        self.total_balnce=0

        for account in self.bank_accounts:
           accounts.append([account[2],account[3],account[4]])
           self.total_balnce+=int(account[4])
        header = ["Index","Bank name:","bank account:","balance:"]
        print(tabulate(accounts,headers=header,showindex=True,tablefmt="rounded_grid",numalign="center",stralign="center"))
        print(f"your total balance: {self.total_balnce}")
        input("Click Enter to go back... ")
        return None
    def transfer(self) -> None:

        Continue=True
        self.clear_screen()
        print(transfer)
        self.bank_accounts=self.db_manger.get_banckaccount(self.account[0])

        print("chose a bank to opreat with:")
        count=1
        for account in self.bank_accounts:
           print(f"Bank {count}: {account[2]}")
           count+=1
        choice=int(input("Enter bank number or -1 if you want to cancel : "))
        while choice < 1 or choice > count-1:
            if choice == -1:
                Continue=False
                break
            else:
                choice=int(input("invalid choice try again: "))
        bank_id = self.bank_accounts[choice-1] [0]
              
        while Continue:
            transaction_type = int(input("Enter transaction type (1: deposit or 2: withdraw -1: cancel): "))
            if transaction_type == 1:
                transaction_message=["deposit","from"]
                break
            elif transaction_type == 2:
               transaction_message=["send","to"]
               break
            elif transaction_type == -1:
                Continue = False
                break
            else:
               print("Invalid transaction type. Please enter either 1 for 'deposit' or 2 for 'withdraw' or -1 for 'canceling' .")
        
        while Continue:
            try:
               amount = float(input(f"Enter the amount you to {transaction_message[0]} or -1 to cancel: "))
               break
            except ValueError:
               print("Invalid amount. Please enter a valid numerical value.")
        if Continue:
            if transaction_type == 2:
                while True:
                    if amount <= self.bank_accounts[choice-1][4]:
                        break
                    elif amount == -1 :
                        Continue = False
                        break
                    else:
                        amount = float(input(f"unsufficient funds, balance = {self.bank_accounts[choice-1][4]}, enter new value or type -1 to go back: "))

              
        while Continue:
            recipient_bank_account = input(f"Enter the account number you want to {transaction_message[0]} {transaction_message[1]} (XX-10-digit number) or -1 to cancel: ")
            if recipient_bank_account == "-1":
               Continue = False
               break
            elif recipient_bank_account[2:].isdigit() and len(recipient_bank_account) == 12 and recipient_bank_account[0:2].isalpha():
                break
            else:
                print("Invalid account number format. Please enter a XX-10-digit number.")
        if Continue:
            if transaction_type == 1 :
                new_balance = self.bank_accounts[choice-1][4]+ amount
                transaction_type = "deposit"
            elif transaction_type == 2 :
                new_balance = self.bank_accounts[choice-1][4]-amount
                transaction_type = "withdraw"
            
            self.db_manger.update_balance(bank_id,new_balance)
            self.db_manger.commit_transaction(self.account[0],bank_id,transaction_type,recipient_bank_account,amount)
            self.clear_screen()
            print(transfer_ok)
            time.sleep(1.5)
        
        return None
    def view_transaction(self) -> None:
        self.clear_screen()
        print(view_transaction)
        data = []
        Continue = True
        trans_Type=""
        self.bank_accounts = self.db_manger.get_banckaccount(self.account[0])


        print("Choose what you want to view: \n 1) For all the banks.\n 2) For a certain bank.\n 0) to go back. ")
        Bank_choice = int(input("Choose: "))
        if Bank_choice == 0:
            Continue = False
        while Continue :
            if Bank_choice > 0 and Bank_choice < 3:
                break
            else:
                Bank_choice = int(input("invalid choice try again: "))
        if Bank_choice == 2:
            count = 1
            for account in self.bank_accounts:
                print(f"Bank {count}: {account[2]}")
                count += 1
            choice = int(input("Enter bank number or -1 if you want to cancel : "))
            while choice < 1 or choice > count-1:
                if choice == -1:
                    Continue = False
                    break
                else:
                    choice = int(input("invalid choice try again: "))
            bank_id = self.bank_accounts[choice-1] [0]
        else:
            bank_id = -1
        while Continue: 
        
            trans_Type = int(input("Enter '1' to view only the deposits, '2' to view only the withdraws, '3' for both or '0' to go back: "))
            if trans_Type == 0:
                Continue = False
                break
            elif trans_Type == 1: 
                trans_Type = "deposit"
                break

            elif trans_Type == 2:
                trans_Type = "withdraw"
                
                break
            elif trans_Type == 3:
                trans_Type = "All"
                break
            else:
                trans_Type = int(input("invalid choice try again: "))                   
        transactions = self.db_manger.get_transactions(self.account[0])
        
        if Continue:
            for trans in transactions:
                Continue = True
                
                if bank_id == -1:
                    if trans_Type == trans [1] or trans_Type == "All":
                        data.append([trans[1],trans[2],trans[3],trans[4]])
                elif bank_id == trans[0]:
                    if trans_Type == trans [1] or trans_Type == "All":
                        data.append([trans[1],trans[2],trans[3],trans[4]])
                        
               
               

            Headers=["Index","Transaction type","correspondent bank account","Amount","time stamp"]
            print(tabulate(data,headers=Headers,showindex=True,tablefmt="rounded_grid",numalign="center",stralign="center",))
            input("Click Enter to go back...")
    