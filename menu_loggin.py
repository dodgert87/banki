
from menu import Menu
from database import DB_manger
from menu_main import  MenuMain
from art import *
import time
from help import Help
class Menu_loggin(Menu):
    
    help_menu: Help
    def __init__(self) -> None:
        super().__init__(options=[
            { "description": "Sing Up", "action": self.SingIn },
            { "description": "Sing In", "action": self.Login },
            {"description": "Help?", "action": self.openHelpMenu }
        ])
        description = "This is a banking management system,\nthat gives you the ability to manage all your bank accounts in one place,\nyou simply have to create an account and log in, add your accounts,\nand perform transactions."
        common_problem=["problem creating an account: your username needs to be unique to you and\nthe password needs at least 8 characters long and has at least one upper case and one lower case.",
                    "problem log-in: if it doesn't ask you for your password check the username it may not be the one you\n created your account with also check that you do not have any space when you type.",
                    ]
        self.help_menu = Help(description,common_problem)
        self.db_manger=DB_manger()
                
        return None
    def openHelpMenu(self) -> None:
        self.help_menu.start()
        return None
    
    def SingIn(self) -> None:
        self.clear_screen()
        print(singup)
        username=input("Enter username: ")
        self.accounts=self.db_manger.get_all_users()
        while True:
            exist=False
            for account in self.accounts:
                if username in account:
                    exist=True
                    break
            if exist:
                username=input("this username alerday taken choose another one: ")
            else:
                break
        password=input("inter a password at least 8 long with one uppercase and one lowercase: ")

        while True:
            if len(password) >= 7 :
                if any(c.isupper() for c in password) and any(c.islower() for c in password):
                        break    
                else:
                    password = input("password dosent have uppercase or lowercase try again: ")
            else:
                password = input("password to short try again: ")
        
        self.db_manger.commit_user(username,password)
        self.clear_screen()
        print(singup_ok)
        time.sleep(1.5)
        return None
    def Login(self) -> None:
        self.clear_screen()
        print(login)
        self.accounts = self.db_manger.get_all_users()
        self.user_name = input("Enter your UserName: ")
        while True:
            self.exist=False
            for account in self.accounts:
                if self.user_name in account:
                    self.exist=True
                    break
                if self.exist:
                    self.user_name=input("UserName dosent exist try again or enter 0 to exit: ")
                if self.user_name=="0":
                    break
            if  self.exist:
                self.password=input("Enter  Password: ")
                while True:
                    self.coorect_password=False
                    if self.password in account:
                        self.account=account
                        self.coorect_password=True
                        break
                    if not self.coorect_password:
                        self.password=input("wrong password try again or inter 0 to exit: ")
                    if self.password=="0":
                        break
                break
            else:
                break
                   
                
        if  self.exist and self.coorect_password:
            self.clear_screen()
            print(login_ok)
            time.sleep(1.5)
            self.main_menu=MenuMain(account,submenu=True)
            self.main_menu.start()
            self.db_manger.close_DB()

        return None
   