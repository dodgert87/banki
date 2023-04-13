import os
import time
from art import Help_logo
class Help():
    description : str
    common_problem : list
    
    def __init__(self,description,common_problem,) -> None:
        support_contact : str = "banki.support@gmail.com" 
        self.description = description
        self.common_problem = common_problem
        self.support_contact = support_contact

        return None

    def start(self):
        self.clear_screen()
        print(Help_logo)
        self.display_description()
        self.display_common_problem()
        print("If you're still having a problem don't hesitate to contact support.")
        choice=input("Do you want contact support? [y/n]: ")
        while True:
            if choice.lower() == "y":
                self.contact_support()
                break
            elif choice.lower() == "n":
                break
            else:
                choice=input("invalid Choice try again [y/n]: ")
        input("click Enter to go back...")

    
    def display_description(self) -> None:
        print("App descripition.\n")
        print(self.description)
        return None
    
    def display_common_problem(self) -> None:
        print("\n**Common problem**\n")
        for problem in self.common_problem:
            print(f"*-{problem}\n")
        return None
    def contact_support(self) -> None:
        print(f"\n\nwrite your messege below and click enter, we will contact you via our emmail {self.support_contact}:\n")
        messege=input()
        self.clear_screen()
        print("we will get back to you as soon as possible. :)")

        return None
        


    def clear_screen(self) -> None:

        os.system('cls')
        return None