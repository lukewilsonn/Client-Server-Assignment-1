import socket
import hashlib
import tkinter
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import os
import time

#function to determine the file hash to send to the server
def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        bytes = f.read()  #read the entire file as bytes
        hash_value = hashlib.sha256(bytes).hexdigest()  # calculate the hash value as hexadecimal string
        return hash_value
    
#Defines the connection protocol to the server
messagebox.askokcancel(title = "Setup", message = "Welcome to File Share!\nWould you like to connect to the server?")
port_input = simpledialog.askinteger(title="Input", prompt="What port number will you use?")
ip_input = simpledialog.askstring(title="Input", prompt="What is the IP address of the server you wish to connect to?")
    
# Initialize Socket Instance
sock = socket.socket()
print ("Socket created successfully.")

# Defining port and host
port = port_input
host = ip_input

# Connect socket to the host and port
try:
    sock.connect((host, port))
    print('Connection Established.')
except Exception as e:
    print(f"Failed to connect to {host}:{port}: {e}")
    sock.close()
    exit()

# Send a greeting to the server
sock.send("A client has connected".encode())

# Ask user if they're signing in or creating an account
choice = simpledialog.askstring(title="Input", prompt="Would you like to Login (L) or Create an Account(C)?")

while choice != "L" and choice != "C":
    messagebox.showerror("Invalid option, please try again!")
    choice = simpledialog.askstring(title="Input", prompt="Would you like to Login (L) or Create an Account(C)?")
sock.send(choice.encode())

# Send user details to server for verification or for account creation
if choice == "L":
    login_username = simpledialog.askstring(title="Input", prompt="Please enter your username: ")
    login_password = simpledialog.askstring(title="Input", prompt="Please enter your password: ")
    sock.send((login_username+" "+login_password).encode())
if choice == "C":
    signIn_username = simpledialog.askstring(title="Input", prompt="Please enter your username (Example: joe_123): ")
    signIn_password = simpledialog.askstring(title="Input", prompt="Please enter a password: ")
    sock.send((signIn_username+" "+signIn_password).encode())

# print the outcome of the operation
outcome = sock.recv(4096)
dOutcome = outcome.decode()
print(dOutcome)

choice = ''
if dOutcome=='Account created' or dOutcome=='User logged in.':
    choice = input("Would you like to send (s) or receive (r) a file? ")
    sock.send(choice.encode())
else:
    sock.close()
    print('Connection closed.')

if choice == "r":
    sock.send(choice.encode())
    # Receives the possible files the client can download
    filesCanUpload = sock.recv(4096)
    filesCanUpload = filesCanUpload.decode()
    #print(filesCanUpload)
    userfile = simpledialog.askstring(title="Input", prompt= filesCanUpload + "\n\nPlease type in name of file you would like to download: ")
    sock.send(userfile.encode())
    # Receives message about whether or not client has input a valid file to download
    fileFound = sock.recv(4096)
    fileFound = fileFound.decode()
    if fileFound[0] == "D":
    # Write File in binary
        file = open("downloads/" + userfile, 'wb')

        # Keep receiving data from the server
        line = sock.recv(4096)

        while(line):
            file.write(line)
            line = sock.recv(4096)
        print()
        messagebox.showinfo(message = userfile + " has been downloaded successfully.")

        file.close()
    else:
        # Not valid file was requested to download
        messagebox.showerror("Error, no such file exists or you do not have permission to access this file. ")

    sock.close()
    print('Connection Closed.')

if choice == "s":
    # Sending file to server
    # Open file dialog to allow user to select a file
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    sock.send(file_path.encode())

    #Sending hash value to the server
    hash_value = calculate_hash(file_path)
    sock.send(hash_value.encode())

    # Asks whether file should be open or protected
    OpOrProt = simpledialog.askstring(title="Input", prompt = "Would you like this file to be open (O) or protected (P)? ")
    sock.send(OpOrProt.encode())
    file = open(file_path, 'rb')
    line = file.read(1024)
    # Keep sending data to the client
    while(line):
        sock.send(line)
        line = file.read(4096)
    print()
    print(file_path + ' has been uploaded successfully.')
    messagebox.showinfo(message = file_path + " has been uploaded successfully.")
    file.close()

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    print('Connection Closed.')
