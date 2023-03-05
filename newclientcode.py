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
port = 8800
host = 'localhost'

# Connect socket to the host and port
sock.connect((host, port))
print('Connection Established.')

# Send a greeting to the server
sock.send('A message from the client'.encode())

# Ask user if they're signing in or creating an account
choice = input('Would you like to log in(LogIn) or create an account(create)? ')
while choice != "LogIn" and choice != "create":
    choice = input("Invalid option, please try again: ")
sock.send(choice.encode())

# Send login details or new user details
if choice == "LogIn":
    logIn = input("Please enter log in details(Example: Tristan password) ")
    sock.send(logIn.encode())
if choice == "create":
    signIn = input("Please enter new user details(Example: Arsenal Champ2023) ")
    sock.send(signIn.encode())

# print the outcome of the operation
outcome = sock.recv(1024)
dOutcome = outcome.decode()
print(dOutcome)

choice = input("Would you like to send (s) or receive (r) a file? ")
sock.send(choice.encode())

if choice == "r":
    # Receives the possible files the client can download
    filesCanUpload = sock.recv(1024)
    filesCanUpload = filesCanUpload.decode()
    print(filesCanUpload)
    userfile = input("Please type in name of file you would like to download: ")
    sock.send(userfile.encode())
    # Receives message about whether or not client inputted a valid file to download
    fileFound = sock.recv(1024)
    fileFound = fileFound.decode()
    if fileFound[0] == "D":
    # Write File in binary
        file = open("Downloaded " + userfile, 'wb')

        # Keep receiving data from the server
        line = sock.recv(1024)

        while(line):
            file.write(line)
            line = sock.recv(1024)
        print()
        print(userfile + ' has been downloaded successfully.')

        file.close()
    else:
        # Not valid file was requested to download
        print("Error, no such file exists or you do not have permission to access this file. ")
    sock.close()
    print('Connection Closed.')

if choice == "s":
    # Sending file to server
    sendfile = input("Please type in name of file you would like to upload: ")
    sock.send(sendfile.encode())

    # Sending hash value to the server
    hash_value = calculate_hash(input)
    sock.send(hash_value.encode())

    # Asks whether file should be open or protected
    OpOrProt = input("Would you like this file to be open (O) or protected (P)? ")
    sock.send(OpOrProt.encode())
    file = open(sendfile, 'rb')
    line = file.read(1024)
    # Keep sending data to the client
    while(line):
        sock.send(line)
        line = file.read(1024)
    
    file.close()
    print(sendfile + ' has been uploaded successfully.')

    sock.close()
