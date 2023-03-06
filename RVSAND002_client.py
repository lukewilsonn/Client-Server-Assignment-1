import socket
import hashlib
# Creating the socket
sock = socket.socket()
print ("Socket created successfully.")

# function to determine the file hash to send to the server
def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        bytes = f.read()  # read the entire file as bytes
        hash_value = hashlib.sha256(bytes).hexdigest()  # calculate the hash value
        return hash_value

# Defining port and host
portNumb = int(input("What port number would you like to connect to? "))
hostIP = input("What IP would you like to connect to? ")
port = portNumb
host = hostIP


# Connects the socket to host and port
try:
    sock.connect((host, port))
    print('Connection Established.')
except Exception as e:
    print(f"Failed to connect to {host}:{port}: {e}")
    sock.close()
    exit()


# Greeting message to server
welcomeMessage = "Client has connected to the server on port number "+str(port)
sock.send(welcomeMessage.encode())

# Ask user if they're signing in or creating an account
choice = input('Would you like to Login (L) or Create an Account(C)? ')
while choice != "L" and choice != "C":
    choice = input("Invalid option, please try again: ")
sock.send(choice.encode())

# Send user details to server for verification or for account creation
if choice == "L":
    print("Log in ")
    logUsername = input("Username: ")
    logPassword = input("Password: ")
    sock.send((logUsername+" "+logPassword).encode())
if choice == "C":
    print("Create account")
    createUsername = input("Please enter your username (Example: joe_123): ")
    createPassword = input("Please enter a password: ")
    sock.send((createUsername+" "+createPassword).encode())

# Prints whether user successfully logs in
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
    print('Connection closed.')

if choice == "r":
    # Receives the possible files the client can download
    filesCanUpload = sock.recv(4096)
    filesCanUpload = filesCanUpload.decode()
    print(filesCanUpload)

    userFile = input("Please type in name of file you would like to download: ")
    sock.send(userFile.encode())

    # Receives message about whether or not client has input a valid file to download
    fileFound = sock.recv(4096)
    fileFound = fileFound.decode()
    if fileFound[0] == "D":
        # Puts file into "Downloads" folder
        file = open("downloads/" + userFile, 'wb')

        # Keep receiving data from the server
        line = sock.recv(4096)

        while(line):
            file.write(line)
            line = sock.recv(4096)
        print()
        print(userFile + ' has been downloaded successfully.')

        file.close()
    else:
        # Not valid file was requested to download
        print("Error, no such file exists or you do not have permission to access this file. ")
    sock.close()
    print('Connection Closed.')

if choice == "s":
    # Sending file to server
    sendFile = input("Please type in name of file you would like to upload: ")
    sock.send(sendFile.encode())

    # Sending hash value to the server
    hashValue = calculate_hash(sendFile)
    sock.send(hashValue.encode())
    hashMessage = sock.recv(4096).decode()

    # Asks whether file should be open or protected
    OpOrProt = input("Would you like this file to be open (O) or protected (P)? ")
    print(hashMessage)
    sock.send(OpOrProt.encode())
    file = open(sendFile, 'rb')
    line = file.read(1024)
    # Keep sending data to the client
    while(line):
        sock.send(line)
        line = file.read(4096)
    
    file.close()
    print(sendFile + ' has been uploaded successfully.')
    print("Connection closed. ")
    sock.close()
