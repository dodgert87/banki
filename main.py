from menu_loggin import Menu_loggin
import time 
import os
from art import welcom, goodbye
class Main:
    def __init__(self) -> None:
        
        loggin_menu = Menu_loggin()
        os.system('cls')
        print(welcom)
        time.sleep(1.5)
        loggin_menu.start()

        os.system('cls')
        print(goodbye)
        time.sleep(1.5)
        return None

if __name__ == "__main__":
    app = Main()