import os
import time
from utils.dicegame import DiceGame

class UserManager:
    def __init__(self):
        self.user_folder = "user_data"
        self.user_file = os.path.join(self.user_folder, "users.txt")
        
        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)

    def load_users(self):
        users = {}
        if os.path.exists(self.user_file):
            with open(self.user_file, "r") as file:
                for line in file:
                    username, password = line.strip().split(",")
                    users[username] = password
        return users

    def save_users(self, users):
        with open(self.user_file, "w") as file:
            for username, password in users.items():
                file.write(f"{username},{password}\n")

    def validate_username(self, username):
        users = self.load_users()
        if username in users:
            return False, "Username already exists."
        elif len(username) < 4:
            return False, "Username must be at least 4 characters long."
        else:
            return True, ""

    def validate_password(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        else:
            return True, ""

    def register(self):
        while True:
            os.system('cls')
            print("REGISTRATION: ")

            # Username input and validation
            username = input("Enter username (at least 4 characters), or leave blank to cancel: ")

            if username:
                valid_username, user_message = self.validate_username(username)
                if valid_username:
                    password = input("Enter password (at least 8 characters), or leave blank to cancel: ")
                    if password:
                        valid_password, pw_message = self.validate_password(password)
                        if valid_password:
                            users = self.load_users()
                            users[username] = password
                            self.save_users(users)  # Save the updated users dictionary
                            print("Registration Successful.")
                            time.sleep(1)
                            return
                        else:
                            print(pw_message)
                    else:
                        print("Transaction Cancelled!")
                else:
                    print(user_message)
                time.sleep(1)
                return
            else:
                print("Transaction Cancelled!")
                time.sleep(1)
                return

    def login(self):
        users = self.load_users()
        while True:
            os.system('cls')
            print("LOGIN:")
            username = input("Enter Username, or leave blank to cancel: ")
            if username:
                if username in users:
                    password = input("Enter Password, or leave blank to cancel: ")
                    if password == users[username]:
                        print("Logged in successfully!")
                        time.sleep(1)
                        usermenu = DiceGame(username)
                        if usermenu.menu():
                            break
                    else:
                        print('Wrong Password')  
                else:
                    print("Username does not exist.")
                time.sleep(1)
            else:
                print("Transaction Cancelled!")
                time.sleep(1)
                return