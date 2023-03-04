import socket

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
    with open('users.txt') as f:
        while True:
            line = f.readline()
            if not line:
                break
            #checks if username and password match
            UP = User + ' ' + Pass
            if line == UP:
                return True
    return False


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
    print('Connected with ', addr)
    

    # Get data from the client
    data = con.recv(1024)
    print(data.decode())
    
    # Receives choice of login or create account
    LorC = con.recv(1024)
    dLorC = LorC.decode()
    #creates account if create is chosen
    if dLorC == "create":
        print('Creating account.')
        #gets user details
        UnamePass = con.recv(1024)
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
    if dLorC == "LogIn":
        print('Verifying login detaails.')
        details = con.recv(1024)
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
    choicedata = con.recv(1024)
    choice = choicedata.decode()
    if choice == "r":
        print("Uploading file to client")
        data2 = con.recv(1024)
        # Read File in binary
        file = open(data2.decode(), 'rb')
        line = file.read(1024)
        # Keep sending data to the client
        while(line):
            con.send(line)
            line = file.read(1024)
        
        file.close()
        print(data2.decode()+' has been downloaded successfully.')
    if choice == "s":
        print("Receiving file from client")
        data3 = con.recv(1024)
        receivedfile = data3.decode()
        # Write File in binary
        file = open("uploaded " + receivedfile, 'wb')

        # Keep receiving data from the client
        line = con.recv(1024)

        while(line):
            file.write(line)
            line = con.recv(1024)
        print()
        print(receivedfile + ' has been uploaded successfully.')
        file.close()
    print('Connection Closed.')

    con.close()
