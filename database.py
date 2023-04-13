import sqlite3
import time

class DB_manger():
   def __init__(self) -> None:
      
      self.conn = sqlite3.connect('banking_management.db')

      self.c = self.conn.cursor()

      self.c.execute('''CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY,
                     username TEXT,
                     password TEXT
                  )''')

      self.c.execute('''CREATE TABLE IF NOT EXISTS bank_accounts (
                     id INTEGER PRIMARY KEY,
                     user_id INTEGER,
                     bank_name TEXT,
                     account_number TEXT,
                     balance REAL,
                     FOREIGN KEY (user_id) REFERENCES users(id)
                  )''')

      self.c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                     bank_account_id INTEGER,
                     transaction_type TEXT,
                     other_bank_account TEXT,
                     amount REAL,
                     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

                     FOREIGN KEY (bank_account_id) REFERENCES bank_accounts(id),
                     FOREIGN KEY (user_id) REFERENCES users(id)
                  )''')


      self.conn.commit()



   def commit_user(self,username,password) -> None:
      try:
         self.c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
         print("User created successfully.")
         self.conn.commit()

      except sqlite3.Error as e:
         print("Error creating user:", e)
      return None

   def get_all_users(self) -> list:
      self.c.execute("SELECT id, username, password FROM users")
      rows = self.c.fetchall()
      return rows
   def commit_acount(self,user_id,bank_name,account_number,initial_balance) -> None:

      try:
         self.c.execute("INSERT INTO bank_accounts (user_id, bank_name, account_number, balance) VALUES (?, ?, ?, ?)",
                  (user_id, bank_name, account_number, initial_balance))
         self.conn.commit()

      except sqlite3.Error as e:
         print("Error creating bank account:", e)
      return None

   def get_banckaccount(self,user_id) -> list:
         self.c.execute("SELECT * FROM bank_accounts WHERE user_id=?", (user_id,))
         accounts = self.c.fetchall()
         return accounts
   
   def commit_transaction(self,user_id, bank_account_id,transaction_type,account_number,amount) -> None:
         

         self.c.execute("INSERT INTO transactions (user_id, bank_account_id, transaction_type,other_bank_account, amount ) VALUES (?, ?, ?, ?, ?)", (user_id, bank_account_id, transaction_type,account_number, amount ))
         self.conn.commit()

         print("Transaction successfully.")
         return None
   def get_transactions(self,user_id) -> list:
      self.c.execute("SELECT id, transaction_type, other_bank_account, amount,created_at FROM transactions WHERE user_id=?", (user_id,))
      transactions = self.c.fetchall()
      return transactions

   def update_balance(self,bank_account_ID, new_value ) -> None:
      self.c.execute('UPDATE bank_accounts SET balance = ? WHERE id = ?', (new_value, bank_account_ID))
      self.conn.commit()
      return None

   def close_DB(self) -> None:
      self.conn.close()
      return None
   