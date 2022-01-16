# Python-Password-Manger-NJRC

Designed and coded a password manager in Python with Arduino integration. The Program uses a master user to login, and stores account data such as usernames and passwords to the master user. While logging into the program with the master user the Arduino was used as a two-factor authentication key. The program detects a connection to the Arduino and checks if certain parameters are met before completing the login procedure.



Introduction


The Password Manager, creates and stores a master user profile, where an Arduino is used as part of a Two-Factor Authentication method, using Arduino inputs and outputs as part of the process. It stores the data for accounts by their names, where it stores the account name, username/e-mail, and password. This can be used whenever you need to store a password you want to remember on your device.



Final Design


The details of design for the different components are described within the notes about their implementation. As a part of the overall design 4 functions were designed:

•	sign_in(user_dir), to ask for username, password, and security question answer. Then checks inputs against stored values to verify they are correct if not, it will continually loop until correct user details are entered. 

•	create_table(), to create a table in a sqlite3 database.

•	store_data(), to store inputted data in a sqlite3 table.

•	lookup_data(), to retrieve stored inputs, from a sqlite3 table using an inputted string that is compared against currently stored strings.
 


Implementation


Imported engi1020.ardunio, random, sleep, pickle and sqlite3 modules.

Created a class User, to store user objects for later use and created an empty user dictionary, user_dir, also created a class Account for later use.

Created variables conn = sqlite3.connect(‘sqldata.db’) and c = conn.cursor(), to connect to an sqlite3 data base.


Worked on sign_in(user_dir)
  
  •	Create a variable that opens and reads pickle file with the stored User object, then created variable stored_user, which loads stored User from the pickle file, then added       stored_user in the user_dir dictionary. 
  
  •	While loop for while true, print “What is your username?”
    
    o	Store input in variable acc_username.
    
    o	Then compared acc_username against stored username in the user_dir.
    
    o	If acc_username = stored username, break out of loop.
    
    o	Else print “username does not exist”.
  
  •	While loop for while true, print “What is your password?”
    
    o	Store input in variable acc_password.
    
    o	Then compared acc_password against stored password in the user_dir.
    
    o	If acc_password = stored password, break out of loop.
    
    o	Else print “You have entered the incorrect password try again”.


Worked on create_table()
  
  •	Used c.execute, to add a new table accounts to the sqlite3 database.


Worked on store_data()
  
  •	Used c.execute, to insert values for account name, username/email and password, to the created accounts table.


Worked on lookup_data(acc_name)
  
  •	Created tuple data = (‘Account Name: ‘, ‘Username/E-Mail: ‘, ‘Password: ‘)
  
  •	Used c.execute to lookup accounts where the account name is equal to the input argument acc_name. 
  
  •	Set variable find = list(c.fetchall()) to store looked up account.
  
  •	If no account is found print “This account does not exist, RETRY”
  
  •	Else, created for loop where account name, username/email, and password, print right after the counterparts of the tuple data.

Once functions were created, worked on creating a user and storing a user and using the create table to start the data storing.


Worked on sign in process
  
  •	While loop for while true, print “Create User? Or Sign In?”
    
    o	Set variable to inputted answer
   
    o	If inputted answer equals create user, print "WARNING! Creating a new account will DELETE the current account! Are you sure you want to proceed?"
    
    o	Set variable to inputted answer
     
      	If inputted answer equals yes, continue with user creation.
      
      	Then asked for name, username, password, and confirmed password, and stored inputs to variables.
  
  •	While loop for while password does not equal confirmed password, continuously runs until both strings are equal.
  
  •	Else continue with user creation and create security question and answer.
    
    o	Save all inputted user info to new_user object, then add to user_dir dictionary. 
    
    o	Create a variable that opens and writes pickle file that stores the new_user object.
    
    o	Used c.execute to check if a table accounts exists, if it does use c.execute to delete table.
    
    o	Then create new table accounts, for new data.
    
    o	Then used sign_in(user_dir) to sign in for first time. After signed in break original while loop.
     
      	Else, anything other than Yes inputted, pass so while loop repeats.
    
    o	Elif inputted answer equals sign in, then use sign_in(user_dir) to sign in. After signed in break original while loop.
    
    o	Else anything other than create user, or sign in inputted print “Error” and original while loop repeats.


Worked on security question and answer check
  
  •	While loop for while true, prints security question stored in user object in dictionary.
  
  •	Set variable for inputted answer.
    
    o	If inputted answer is equal to stored answer break loop.
    
    o	Else print “Security question answer wrong, RETRY”, and while loop repeats.


Worked on Two-Factor Authentication, Step One
  
  •	While loop for while true, print “Two-Factor Authentication, Step One”
    
    o	Used Arduino, printed to lcd screen 5, 4, 3, 2, 1. With sleep(1) between each number and after 1 to count down from 5 to 0.
    
    o	Then used digital_read(2) for the button, and digital_read(7) for the touch sensor.
    
    o	If button and touch sensor reads equal to 1, print “Step One successful!”, and break while loop.
    
    o	Else, print ”Step One failed, RETRY”, and while loop repeats.


Worked on Two-Factor Authentication, Step Two
  
  •	While loop for while true, print “Two-Factor Authentication, Step Two”
    
    o	Used random.randint() to produce a random 4-digit number from 1000-9999 and set it to a variable.
    
    o	Printed variable to lcd screen, and user must input 4-digit number seen on lcd screen to console.
    
    o	If inputted 4-digit number is qual to random 4-digit number, print "Step Two successful!" and print "Two-Factor Authentication complete!". Then break while loop.
    
    o	Else, print ”Step Two failed, RETRY”, and while loop repeats.

Print “Welcome ‘name of user’! You have signed in successfully”.


Worked on, account storing, account lookup and logging out of program
  
  •	While loop for while true, print "Would you like to Store an account?, Lookup an account?, or LogOut?".
  
  •	Set variable for user input
    
    o	If user input is equal to store, ask and store inputs to variables for account name, username/email, and password, of the account you would like to store.
      
      	The store collected data in Account object and set it to a varible acc_data.
      
      	Used store_data() to store collected account data using Account object.
    
    o	Elif user input is equal to lookup, print "What is the name of the account you would like to Lookup?".
      
      	Set a variable acc_name to store user input.
      
      	Used lookup_data(acc_name) to lookup account.
    
    o	Elif user input is equal to logout, print "LogOut successful! Goodbye ‘name of user ‘"), and used exit() to quit program.
    
    o	Else, print “Error”, and while loop repeats.
