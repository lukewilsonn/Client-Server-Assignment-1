import socket
import hashlib

# Receives username and password to add to users. returns false if ussername already exists and true if the account has been added
def addUser(User, password):
    uExists=False
    with open('users.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            # check if username already exists
            str = line.split()
            if User == str[0]:
                uExists=True
    if uExists == True:
        return False
    else:
        # add user details to users.txt 
        with open('users.txt','a') as f:
            f.write(User + ' ' + password)
            f.write('\n')
        return True
# Logs into existing account. Returns true or false if account is successfully signed in or not
def signIN(User, Pass):
    with open('users.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            #checks if username and password match
            UP = User + ' ' + Pass
            if line == UP:
                return True
    return False

#function to determine the file hash to send to the server
def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        bytes = f.read()  # read the entire file as bytes
        hash_value = hashlib.sha256(bytes).hexdigest()  # calculate the hash value as hexadecimal string
        return hash_value


USER = ''


# Initialize Socket Instance
sock = socket.socket()
print ("Socket created successfully.")

# Defining port and host
port = 8800
host = ''

# binding to the host and port
sock.bind((host, port))

# Accepts up to 10 connections
sock.listen(10)
print('Socket is listening...')

while True:
    # Establish connection with the clients.
    con, addr = sock.accept()
    print('Established connection with ', addr)

    # Get data from the client
    data = con.recv(4096)
    print(data.decode())
    
    # Receives choice of login or create account
    LorC = con.recv(4096)
    dLorC = LorC.decode()
    #creates account if create is chosen
    if dLorC == "C":
        print('Creating account.')
        #gets user details
        UnamePass = con.recv(4096)
        UP = UnamePass.decode()
        user, password = UP.split()
        #calls addUser()
        signedIn = addUser(user, password)
        #returns appropriate response
        if signedIn:
            print('Account created.')
            message = 'Account created'
            con.send(message.encode())
            USER = user
        else:
            print('Could not create account. Username already exists.')
            message = 'Could not create account. Username already exists.'
            con.send(message.encode())
    #logs into account
    if dLorC == "L":
        print('Verifying login details.')
        details = con.recv(4096)
        info = details.decode()
        user, password = info.split()
        logIn = signIN(user, password)
        if logIn:
            print('User logged in.')
            message = 'User logged in.'
            con.send(message.encode())
            USER = user
        else:
            print('Log in unsuccessful. Username or password incorrect.')
            message = 'Log in unsuccessful. Username or password incorrect.'
            con.send(message.encode())
    # Receives choice user makes, either receiving or sending data
    choicedata = con.recv(4096)
    choice = choicedata.decode()
    if choice == "r":
        # Checks which files the User has access to
        with open('listOfFiles.txt', 'r') as f:
            availFiles = []
            while True:
                line = f.readline()
                if not line:
                    break
                str = line.split()
                if USER == str[1] or "open" == str[1]:
                    availFiles.append(str[0])
        stringFiles = "Your downloadable files are: \n"
        for item in availFiles:
            stringFiles += item + "\n"
        con.send(stringFiles.encode())

        # Uploading the requested file to client
        print("Uploading file to client")
        data2 = con.recv(4096)
        fileName = data2.decode()

        # Checks if file requested is available for client to download
        if fileName not in availFiles:
            noFileFound = "Error, no such file exists or you do not have permission to access this file. "
            print(noFileFound)
            con.send(noFileFound.encode())
        else:
            con.send("Downloading file")
            # Read File in binary
            file = open(fileName, 'rb')
            
            line = file.read(4096)
            # Keep sending data to the client
            while(line):
                con.send(line)
                line = file.read(4096) 
            file.close()
            print(fileName+' has been downloaded successfully.')

    if choice == "s":
        # Receives the file from client
        print("Receiving file from client")
        receivedfile = con.recv(4096).decode()
        #receivedfile = receivedfile.decode()
        file_hash = con.recv(4096).decode()

        # compare the received hash with the calculated hash
        if file_hash == calculate_hash(receivedfile):
            # if the hashes match, send a success message to the client
            con.send("File upload successful".encode())
        else:
            # if the hashes don't match, send an error message to the client
            con.send("File upload failed: Hash mismatch".encode())

        # Receives whether file should be open or protected
        OpenOrProtected = con.recv(4096)
        OpenOrProtected = OpenOrProtected.decode()
        # Keeps track of open and protected files
        with open('listOfFiles.txt', 'a') as f:
            if OpenOrProtected == "P":
                f.write(receivedfile + " " + USER+ "\n")
            if OpenOrProtected == "O":
                f.write(receivedfile + " open"+"\n")

        # Write File in binary
        file = open("uploaded/ " + receivedfile, 'wb')

        # Keep receiving data from the client
        line = con.recv(4096)

        while(line):
            file.write(line)
            line = con.recv(4096)
        print()
        print(receivedfile + ' has been uploaded successfully.')
        file.close()
    print('Connection Closed.')

    con.close()
