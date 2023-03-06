import socket
import hashlib

#function to determine the file hash to send to the server
def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        bytes = f.read()  # read the entire file as bytes
        hash_value = hashlib.sha256(bytes).hexdigest()  # calculate the hash value as hexadecimal string
        return hash_value
    
# Initialize Socket Instance
sock = socket.socket()
print ("Socket created successfully.")

# Defining port and host

host = input('Enter Host IP: ')
port = input('Enter port number: ')

# Connect socket to the host and port
try:
    sock.connect((host, int(port)))
    print('Connection Established.')
except Exception as e:
    print(f"Failed to connect to {host}:{port}: {e}")
    sock.close()
    exit()


# Send a greeting to the server
sock.send("Hello Server!".encode())

# Ask user if they're signing in or creating an account
choice = input('Would you like to Login (L) or Create an Account(C)? ')
while choice != "L" and choice != "C":
    choice = input("Invalid option, please try again: ")
sock.send(choice.encode())

# Send user details to server for verification or for account creation
if choice == "L":
    dLogin = input("Please enter your username followed by your password(Example: Arsenal Champ2023): ")
    sock.send(dLogin.encode())
if choice == "C":
    signIn_username = input("Please enter your username (Example: User1): ")
    signIn_password = input("Please enter a password: ")
    sock.send((signIn_username+" "+signIn_password).encode())

# print the outcome of the operation
outcome = sock.recv(4096)
dOutcome = outcome.decode()
print(dOutcome)

# code only advances if log in or account creation was successful
choice = ''
if dOutcome=='Account created' or dOutcome=='User logged in.':
    choice = input("Would you like to send (s) or receive (r) a file? ")
    sock.send(choice.encode())
else:
    sock.close()
    print('Connection has been closed.')

if choice == "r":
    # Receives the files the client can download and prints them as a list
    filesCanUpload = sock.recv(4096)
    filesCanUpload = filesCanUpload.decode()
    print(filesCanUpload)
    userfile = input("Enter the name of file you would like to download: ")
    sock.send(userfile.encode())
    # Receive message from server
    fileFound = sock.recv(4096)
    fileFound = fileFound.decode()
    if fileFound[0] == "D":
    # Write File in binary
        file = open("downloads/" + userfile, 'wb')

        # Receivce data from server line by line
        line = sock.recv(4096)

        while(line):
            file.write(line)
            line = sock.recv(4096)
        print()
        print(userfile + ' was downloaded successfully.')

        file.close()
    else:
        # Not valid file was requested to download
        print("Error, no such file exists or you do not have permission to access this file. ")
    sock.close()
    print('Connection Closed.')

if choice == "s":
    # Sending file to server
    sendfile = input("Enter the name of the file you would like to upload: ")
    sock.send(sendfile.encode())

    # Sending hash value to the server
    hash_value = calculate_hash(sendfile)
    sock.send(hash_value.encode())

    # Asks whether file should be open or protected
    oORp = input("Open file can be viewed and downloaded by other users while protected files are only available to the user who uploaded them." + '\n' + "Enter P if you want the file to be protected or O if you want it to be open: ")
    sock.send(oORp.encode())
    file = open(sendfile, 'rb')
    line = file.read(1024)
    # Keep sending data to the client
    while(line):
        sock.send(line)
        line = file.read(4096)
    
    file.close()
    print(sendfile + ' was uploaded successfully.')
    
    sock.close()
str = input()