
import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back


###FIRST PART(CHECK NOTES)
# initializing colorama to be able to use it
init()

#setting available colors
colors = [Fore.CYAN, Fore.BLUE, Fore.GREEN, Fore.LIGHTBLACK_EX,
        Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
        Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
        Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
        ]

#Choose a random color for the client
myClient_color = random.choice(colors)

#server's IP adress
#if the server is not on this machine,
#put the private(network) IP address (e.g 192.168.1.2)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
serperator_token = "<SEP>" #we use this to seperate client name & message

#initializing TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

#connect to the server 
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

#ask client for name 
myClient_name = input("Hi there, kindly input your name:")


###SECOND PART(CHECK NOTES)
def listen_for_messages():
    while True:
        messages = s.recv(1024).decode()
        print("\n" + messages)

#making a thread that listens for messages to this client & print them.
t = Thread(target=listen_for_messages)

#make the thread daemon so it ends whenever the main thread ends
t.daemon = True

#start the thread
t.start()


###THIRD PART
while True:
    #asking the client to input the message he wants to send to the server
    to_send = input()

    #a way to exit the program
    if to_send.lower() == "q":
        break
    
    #adding the date&time, name & color of the sender
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    to_send = f"{myClient_color}[{current_date}] {myClient_name}{serperator_token}{to_send}{Fore.RESET}"

    #send message 
    s.send(to_send.encode())

#close the socket
s.close()