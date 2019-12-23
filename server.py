import socket
import select
# "select" will enable multi platform: whether mac or windows.

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# create a socket object, and create a server
# AF_INET refers to addresses from the internet; AddressFamily_Internet
# socket_stream - TCP, connection-based
# socket(ip, address)

server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#allow us to reconnect

server_socket.bind((IP,PORT))
server_socket.listen()


sockets_list = [server_socket]
#create a list of client, in this case, server_socket

clients = {}
# socket -> key, 
# data -> value
print(f'Listening for connections on {IP}:{PORT}...')

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH) 
        # receive message header

        if not len(message_header):
            return False
        # if we get nothing, return false
        
        message_length = int(message_header.decode("utf-8").strip())
        return {'header': message_header, 'data':client_socket.recv(message_length)}
        # header contains how low is the user name

    except:
        # if error
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    # select takes 3 parameters: read list (things that read in), write list, exceptions)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            #ip , adress
            
            user = receive_message(client_socket)
              
           
            if user is False:
                continue
             #if client disconnected before he sent his name

            sockets_list.append(client_socket)
            # Add accepted socket to select.select() list

            clients[client_socket] = user
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
        #if new connection just connected, and the server needs to accept it

        else:
            # if existing socket is sending a message
            message = receive_message(notified_socket)

            if message is False:
                
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')



            for client_socket in clients:
                if client_socket != notified_socket:
                    # if sender doesnt send to self
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    # on the client side, we display user name and mesage ( user name data and the mesasge itself)
    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
    # handles socket exception, just in case

            


  


