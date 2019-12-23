import socket
import select
import errno #match specific error code



HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)
# not block recv method

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    # infinite attempt to get any message

    message = input(f'{my_username} > ')
    # this will look like user sending the message. ex:  Dav > 
    
    if message: # if user hit enter to by pass
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection close by the sever")
                print("system exiting out")
                sys.exit()
            # if we get no data, server closethe connection
            
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            # convert header to int value ; decode username

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            # get message info
            print(f'{username} > {message}')
    
    except IOError as e:
        # happens if no more message to receive
        # if we get error code that is not again or wouldblock
        #differ by os
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            print("system exiting out")
            sys.exit()

        # We did not receive anything
        continue
     
    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        print("system exiting out")
        sys.exit()




