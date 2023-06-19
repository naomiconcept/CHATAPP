
import socket
from threading import Thread


#TO LISTEN FOR CONNECTION
# server's IP address
SERVER_HOST = "0.0.0.0" #this tells server to "listen" for and accept connections from any IP address
SERVER_PORT = 5002 #to exchange info gotten from the server_host btween the webserver and the web client
seperator_token = "<SEP>" #this is to seperate the client name and message 


#Initialise list/set all conncected clients's sockets.
myClient_sockets = set()

#create a TCP socket
s = socket.socket()

#make the port as reuseable port(asper resuse the same IP and port)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))

#listen for upcoming connections
##############################################change this client number later
s.listen(5) #this is to listen up to 5clients
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


#TO ACCEPT CONNECTIONS
#this function keep listening for a message from 'cs' socket.
#whenever a message is received, broadcasts it to all other connected clients.
def listen_for_clients(cs):
    while True:
        try:
            #this keeps listening for a message from 'cs' socket
            message = cs.recv(1024).decode()
        except Exception as e :
            #client no longer connected
            #remove it(the client connection) from the set
            print(f"[!] Error: {e}")
            myClient_sockets.remove(cs)

        else:
            #if we recieve a message, replace the <SEP> token with ":"
            message = message.replace(seperator_token, ":")

        #iterate over all connected sockets
        for myClient_socket in myClient_sockets:
            #send the message 
            myClient_socket.send(message.encode())

    while True:
        #constant listening for new connections
        myClient_socket, myClient_address = s.accept()
        print(f"[+] {myClient_address} connected")

        #to add the new connected client to connected sockets.
        myClient_sockets.add(myClient_socket)

        #start a new thread that listens for each client's messages.
        t = Thread(target=listen_for_clients, args=(myClient_socket,))

        #make the thread daemon so it ends whenever the main thread ends
        t.daemon = True

        #start the thread
        t.start()

    #close client sockets
    for cs in myClient_sockets:
        cs.close()

    #close server socket
    s.close()