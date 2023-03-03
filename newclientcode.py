import socket

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
choice = input("Would you like to send (s) or receive (r) a file? ")
sock.send(choice.encode())

if choice == "r":
    userfile = input("Please type in name of file you would like to download: ")
    sock.send(userfile.encode())
    # Write File in binary
    file = open("Downloaded " + userfile, 'wb')

    # Keep receiving data from the server
    line = sock.recv(1024)

    while(line):
        file.write(line)
        line = sock.recv(1024)
    print()
    print(userfile + ' has been received successfully.')

    file.close()
    sock.close()
    print('Connection Closed.')
if choice == "s":
    sendfile = input("Please type in name of file you would like to upload: ")
    sock.send(sendfile.encode())
    file = open(sendfile, 'rb')
    line = file.read(1024)
    # Keep sending data to the client
    while(line):
        sock.send(line)
        line = file.read(1024)
    
    file.close()
    print(sendfile + ' has been uploaded successfully.')

    sock.close()