# capualator - calculator with hidden vault
# created by : Chris Taylor [C0SM0]

# imports
from cryptography.fernet import Fernet # pip req
from PIL import Image, ImageTk # pip req
from tkinter import messagebox
from tkinter import *
import os

'''
TODO
github
installer -
'''

# root initialization
root = Tk()
root.title('Capulator')
root.config(bg='#000000')
root.iconbitmap(r'C:\\ProgramData\\Capulator\\images\\logo.ico')

# math type variables
addition_var = 'addition'
subtraction_var = 'subtraction'
multiplication_var = 'multiplication'
division_var = 'division'

# databases [db]
code_file = 'code.txt'  # code_db
key_file = 'encrypted.key'  # key_db
hidden_dir = 'HiddenVault' # hidden_db

# unlocks files
def unlock_files(key_db, code_db):
    os.system(f'attrib -h -s -r {key_db}')
    os.system(f'attrib -h -s -r {code_db}')

# locks key file
def lock_files(key_db, code_db):
    os.system(f'attrib +h +s +r {key_db}')
    os.system(f'attrib +h +s +r {code_db}')

# create encryption key
def create_key(key_db):
    created_key = Fernet.generate_key()

    with open(key_db, 'wb') as db:
        db.write(created_key)

    return created_key

# load encryption key
def load_key(key_db):
    return open(key_db, 'rb').read()

# validates encryption key
def key_checker(key_db):
    with open(key_db, 'r') as db:
        fkey = db.read()

    if fkey.endswith('='):
        checked_key = fkey.encode()

    else:
        checked_key = create_key(key_db)

    return checked_key

# encryption method
def encryption_process(code_db, key):
    f = Fernet(key)

    with open(code_db, 'rb') as db:
        original_data = db.read()

    encrypted_data = f.encrypt(original_data)

    with open(code_db, 'wb') as db:
        db.write(encrypted_data)

    return encrypted_data

# decryption method
def decryption_process(code_db, key):
    f = Fernet(key)

    with open(code_db, 'rb') as db:
        encrypted_data = db.read()

    decrypted_data = f.decrypt(encrypted_data)

    with open(code_db, 'wb') as db:
        db.write(decrypted_data)

    return str(decrypted_data)

# checks and decrypts credentials file
def code_checker(code_db, key):
    with open(code_db, 'r') as db:
        read_db = db.read()

# checks if file is encrypted
    if read_db.startswith('gAA'):
        decrypted_db = decryption_process(code_db, key)
        encryption_process(code_db, key)
        return decrypted_db

# checks if file is decrypted
    elif '||' in read_db:
        encryption_process(code_db, key)
        return read_db

    else:
        pass

unlock_files(key_file, code_file)

# error detection
try:
    key = key_checker(key_file)
    decryption_process(code_file, key)

except:
    key = key_checker(key_file)
    encryption_process(code_file, key)
    decryption_process(code_file, key)

code = code_checker(code_file, key)
code = code.replace('||', '')

lock_files(key_file, code_file)

# main entry box
calculator_entry = Entry(root, width = 45, borderwidth=8, bg='#32c878')
calculator_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# opens hidden directory
def open_directory():
    os.system(f'attrib -h -s -r {hidden_dir}')
    os.system(f'mkdir {hidden_dir}')
    os.system(f'start {hidden_dir}')

# gets new password
def get_password(password, window):
    messagebox.showwarning('WARNING, App Restart Needed', 'Restart The App in Order For The Password Change to Take Affect\nMake Sure to "Exit & Save"')

    with open(code_file, 'w') as f:
        f.write('||'+str(password))

    encryption_process(code_file, key)
    exit_window(window)

# change password code
def change_password():
    account_info = Toplevel()
    account_info.title('Change Password')
    account_info.config(bg='#003333')
    Label(account_info, text='Enter New Password Code :', fg='#ffffff', bg='#003333').grid(row=0)
    new_code = Entry(account_info, width=35, borderwidth=5, bg='#32c878')
    new_code.grid(row=1)
    Button(account_info, text='SUBMIT', fg='#32c878', bg='#000000', command=lambda: get_password(new_code.get(), account_info)).grid(row=2)

# exits vault
def exit_window(window):
    os.system(f'attrib +h +s +r {hidden_dir}')
    lock_files(key_file, code_file)
    window.destroy()

# displays hidden vault
def show_vault():
    unlock_files(key_file, code_file)
    vault = Toplevel()
    vault.title('Hidden Vault')
    vault.iconbitmap(r'C:\\ProgramData\\Capulator\\images\\logo.ico')
    vault.config(bg='#003333')

    Button(vault, text='Open Hidden File Directory', padx=55, pady=20, bg='#000000', fg='#32c878', command=open_directory).grid(row=0, column=0)
    Button(vault, text='Change Password', padx=80, pady=20, bg='#000000', fg='#32c878', command=change_password).grid(row=1, column=0)
    Button(vault, text='Exit & Save', padx=98, pady=20, bg='#000000', fg='#32c878', command=lambda: exit_window(vault)).grid(row=2, column=0)

    Label(vault, text='Welcome to Your Secret Vault\n'+\
                      'Feel Free to Hide ANYTHING in Here.\n'+\
                      'Not Even Enabling Hidden Files Will Display These Contents...\n'+\
                      'Have Fun!', bg='#003333', fg='#ffffff').grid(row=1, column=1)

# popup that verifies code
def confirm():
    confirmation = messagebox.askquestion('Confirm', 'Do You Wish to Proceed?')
    # Label(root, text=confirmation).pack()

    if confirmation == 'yes':
        show_vault()
  
    else:
        pass

# detects if button is clicked
def pressed(numeric_key):
    calculator_entry.insert(END, numeric_key)

# gets value and returns math type for detection
def gets_value(type):
    # initialize global variables
    global original_value
    global math_type

    # get's currnt values
    original = calculator_entry.get()

    original_value = int(original)
    math_type = str(type)

    # clears calculator entry
    calculator_entry.delete(0, END)

# adds values
def addition():
    gets_value(addition_var)

# suntracts values
def subtraction():
    gets_value(subtraction_var)

# multiplies values
def multiplication():
    gets_value(multiplication_var)

# divides values
def division():
    gets_value(division_var)

# evaluate the equation, checks for code
def equalivent():
    new_value = calculator_entry.get()

    if calculator_entry.get() == code:
        confirm()
    
    calculator_entry.delete(0, END)
    
    # evaluates additions
    if math_type == addition_var:
        calculator_entry.insert(0, (original_value + int(new_value)))
 
    # evaluates subtraction
    if math_type == subtraction_var:
        calculator_entry.insert(0, (original_value - int(new_value)))
 
    # evaluates multiplication
    if math_type == multiplication_var:
        calculator_entry.insert(0, (original_value * int(new_value)))
    
    # evaluates division
    if math_type == division_var:
        calculator_entry.insert(0, (original_value / int(new_value)))
    

# clears calculator entry
def clear_entry():
    calculator_entry.delete(0, END)

# numeric buttons and allignment
Button(root, text='1', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(1)).grid(row=3, column=0)
Button(root, text='2', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(2)).grid(row=3, column=1)
Button(root, text='3', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(3)).grid(row=3, column=2)
Button(root, text='4', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(4)).grid(row=2, column=0)
Button(root, text='5', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(5)).grid(row=2, column=1)
Button(root, text='6', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(6)).grid(row=2, column=2)
Button(root, text='7', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(7)).grid(row=1, column=0)
Button(root, text='8', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(8)).grid(row=1, column=1)
Button(root, text='9', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(9)).grid(row=1, column=2)
Button(root, text='0', font=("", 12), padx=40, pady=20, bg='#000000', fg='#32c878', command=lambda: pressed(0)).grid(row=4, column=0)

# mathematic buttons and allignment
Button(root, text='+', font=("", 12), padx=39, pady=20, bg='#000000', fg='#32c878', command=addition).grid(row=4, column=1)
Button(root, text='-', font=("", 12), padx=40.4, pady=20, bg='#000000', fg='#32c878', command=subtraction).grid(row=4, column=2)
Button(root, text='×', font=("", 12), padx=39, pady=20, bg='#000000', fg='#32c878', command=multiplication).grid(row=5, column=1)
Button(root, text='÷', font=("", 12), padx=39, pady=20, bg='#000000', fg='#32c878', command=division).grid(row=5, column=2)
Button(root, text='=', font=("", 12), padx=39, pady=20, bg='#000000', fg='#32c878', command=equalivent).grid(row=5, column=0)
Button(root, text='CLEAR', font=("", 12), padx=121, pady=20, bg='#000000', fg='#32c878', command=clear_entry).grid(row=6, column=0, columnspan=3)

root.mainloop()
lock_files(key_file, code_file)
