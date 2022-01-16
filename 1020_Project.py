# Password Manager
# Python 3
# By Noah Colbourne

from engi1020.arduino import *
from time import sleep
import random
import pickle
import sqlite3

# Created a class to store an object User, so I could store the user object using the imported pickle module.
class User:
    def __init__(self, username, name, password, sq, sq_ans):
        self.username = username
        self.name = name
        self.password = password
        self.sq = sq
        self.sq_ans = sq_ans

# Create a class to store an object Account, so I could  store the account object using the imported sqlite3 module.
class Account:
    def __init__(self, acc_name, acc_un, acc_pw):
        self.acc_name = acc_name
        self.acc_un = acc_un
        self.acc_pw = acc_pw

# Created a sqlite3 database
conn = sqlite3.connect('sqldata.db')
c = conn.cursor()

user_dir = {}

acc_username = ''

# Defined functions for easier use later, Defined sign_in, create_table, store_data, lookup_data.
def sign_in(user_dir):
    infile = open('userdata.pkl', 'rb')
    stored_user = pickle.load(infile)
    user_dir[stored_user.username] = stored_user
    acu = 0
    while acu == 0:
        print("What is your username?")
        global acc_username             # Made global to be used as key for retrieve User object data from user_dir
        acc_username = input()
        if acc_username in user_dir:
            break
        else:
            print("username does not exist")
    acp = 0
    while acp == 0:
        print("What is your password?")
        acc_password = input()
        user = user_dir[acc_username]
        if acc_password == user.password:
            acp = 1 
        else:
            print("You have entered the incorrect password try again")
            break

def create_table():
    c.execute("""CREATE TABLE accounts (
        acc_name text,
        username text,
        password text
        )""")
    conn.commit()

def store_data():
    c.execute("INSERT INTO accounts VALUES (:name, :username, :password)", {'name': acc_data.acc_name, 'username': acc_data.acc_un, 'password': acc_data.acc_pw})
    conn.commit()
    print("Account stored successfully!")


def lookup_data(acc_name):
    data = ('Account Name: ', 'Username/E-Mail: ', 'Password: ')
    c.execute("SELECT * FROM accounts WHERE acc_name=:name", {'name': acc_name})
    find = list(c.fetchall())
    print('')
    if not find:
        print("This account does not exist, RETRY")
    else:
        for row in find:
            for i in range(0, len(row)):
                print(data[i] + row[i])
    print('')

print('Welcome to PassMan!')
account = ' '                           # Set empty string to account so It can be used for condition in while loop.
while account != 'signed_in':           # Used while loop for the create user/sign in process.
    print('Create User? or Sign In?')
    ansintro = input()                  # ansintro, answer to introduction question.
    if (ansintro == 'Create User') or (ansintro == 'create user') or (ansintro == 'Create user') or (ansintro == 'CREATE USER'):
        print("WARNING! Creating a new user will DELETE the current user! Are you sure you want to proceed?")
        proceed = input()                  
        if (proceed == 'Yes') or (proceed == 'yes') or (proceed == 'YES'):
            print("Creating User")
            print('What is your name?')
            name = input()
            print('Create Username')
            cr_username = input()       # cr_username, Created Username.
            print('Create Password')
            cr_password = input()       # cr_password, Created Password.
            print('Confirm Password')
            con_pass = input()          # con_pass, Confirmed Password.
            while con_pass != cr_password:
                print('Password did not match, RETRY')
                print('Create Password')
                cr_password = input()   # cr_password, Created Password.
                print('Confirm Password')
                con_pass = input()      # con_pass, Confirmed Password.
            else:
                print(f"Congratulations {name}! User created successfully!")
                print('Securing your account with Two-Factor Authentication')
                print('Create a security question!')
                cr_sq = input()         # cr_sq, Created Security Question.
                print('What is the answer?')
                cr_sq_ans = input()     # cr_sq_ans, Created Security Question Answer.
                print('Secured with Two-Factor Authentication, when signing in your security question will be asked, and you will have to Authenticate using an Arduino')

                new_user = User(cr_username, name, con_pass, cr_sq, cr_sq_ans) 
                # User object set to new_user
                # new_user used to make key:value in user_dir, key = to created username and value = User object stored in newuser.
                user_dir[new_user.username] = new_user

                outfile = open('userdata.pkl', 'wb')    # created and open userdata.pkl, writing data in bytes.
                pickle.dump(new_user, outfile)          # writes data of new user to file userdata.pkl.
                outfile.close()                         # data is stored file is closed.
                c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")   # Checks if a table named accounts exists in sqlite database
                c.execute("DROP TABLE IF EXISTS accounts")                                           # If table accounts exists, it is deleted
                conn.commit()
                create_table()

                print("Now Sign In for the first time!")
                sign_in(user_dir)
                account = 'signed_in'
        else:
            pass
    elif (ansintro == "Sign In") or (ansintro == "sign in") or (ansintro == "Sign in") or (ansintro == "SIGN IN"):
        sign_in(user_dir)  
        account = 'signed_in'  
    else:
        print("Error") 
sq_login = 0                         # sq_login, security question login is set to 0 as condition for while loop.
while sq_login == 0:
    print("Answer your security question")
    sq_user = user_dir[acc_username] # sq_user, security question of user is set to the value User object associated with key acc_username
    print(f"{sq_user.sq}")           # sq_user.sq retrives the security qustrion saved to the User object for acc_username
    in_sq_ans = input()              # in_sq_ans, user inputted security question answer
    if in_sq_ans == sq_user.sq_ans:
        sq_login = 1
        print("Answered successfully!")
    else:
        print("Security question answer wrong, RETRY")
tfa1 = 0                             # tfa1, Two-Factor Authentication Step One is set to 0 as condition for while loop.
while tfa1 == 0:
    print("Two-Factor Authentication, Step One")
    lcd_print("5")
    sleep(1)
    lcd_clear()
    lcd_print("4")
    sleep(1)
    lcd_clear()
    lcd_print("3")
    sleep(1)
    lcd_clear()
    lcd_print("2")
    sleep(1)
    lcd_clear()
    lcd_print("1")
    sleep(1)
    lcd_clear()
    button = digital_read(2)
    touch = digital_read(7)
    if (button == 1) and (touch == 1):
        tfa1 = 1
        print("Step One successful!")
    else:
        print("Step One failed, RETRY")
tfa2 = 0                             # tfa2, Two-Factor Authentication Step Two is set to 0 as condition for while loop.
while tfa2 == 0:
    print("Two-Factor Authentication, Step Two")
    print("Enter the 4-digit code that is shown on the LCD screen!")
    rg4_code = int(random.randint(1000, 9999))     # rg4_code, randomly generated 4-digit code.
    lcd_print(rg4_code)
    in_code = int(input())                         # in_code, user inputted 4-digit code.
    if rg4_code == in_code:
        tfa2 = 1
        lcd_clear()
        print("Step Two successful!")
        print("Two-Factor Authentication complete!")
    else:
        print("Step Two failed, RETRY")
name_user = user_dir[acc_username]     # name_user, name of user is set to the value User object associated with key acc_username
print(f"Welcome {name_user.name}! You have signed in successfully!") # name_user.name retrives the name saved to the User object for acc_username
menu = 0                               # menu is set to 0 as condition for while loop.
while menu == 0:
    print("Would you like to Store an account?, Lookup an account?, or LogOut?")
    choice = input()                       
    if (choice == 'store') or (choice == 'Store') or (choice == 'STORE'):
        print("What is the name of the account you would like to store?")
        acc_name = input()                  # acc_name, name of the account you would like to store or lookup.
        print("What is the Username/E-Mail for the account you would like to store?")
        st_username = input()               # st_username, username associated with the account you would like to store.   
        print("What is the Password for the account you would like to store?")
        st_pass = input()                   # st_pass, password associated with the account you would like to store. 
        acc_data = Account(acc_name, st_username, st_pass)   # Stored data in Account object, and set it to acc_data, to be used in store_data() function.
        store_data()
    elif (choice == 'lookup') or (choice == 'Lookup') or (choice == 'LOOKUP'):
        print("What is the name of the account you would like to Lookup?")
        acc_name = input()
        lookup_data(acc_name)               # acc_name, name of the account you would like to store.
    elif (choice == 'LogOut') or (choice == 'Logout') or (choice == 'LOGOUT') or (choice == 'logout'):
        print(f"LogOut successful! Goodbye {name_user.name}")
        conn.close()
        exit()
    else:
        print("Error")
exit()




    


