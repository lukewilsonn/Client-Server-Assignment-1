import socket

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