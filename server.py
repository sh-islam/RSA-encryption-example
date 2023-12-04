import socket
from _thread import *
import threading
import select
import rsa

public_key, private_key = rsa.newkeys(1024)

server = "localhost"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = {}
public_partners = {}

try:
    s.bind((server, port))
except socket.error as e:
    print(f"Error binding to address {server}:{port}: {e}")
    exit()

s.listen(2)
print("Waiting for a connection, Server Started")

def main():
    exit_flag = threading.Event()

    while exit_flag.isSet:
        try:
            if select.select([s], [], [], 0)[0]:    
                client_socket, client_addr = s.accept()
                print(f"Accepted connection from {client_addr}")

                # Exchange keys
                public_partner = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))
                print(f"Received public key from {client_addr}: {public_partner}")
                client_socket.send(public_key.save_pkcs1("PEM"))

                # Receive and decrypt the message
                encrypted_message = client_socket.recv(1024)
                decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()
                print(f"Received and decrypted message from {client_addr}: {decrypted_message}")
                
        except KeyboardInterrupt:
            exit_flag.set()
            break

    s.close()
    print("Server socket closed")

if __name__ == "__main__": 
    main()
