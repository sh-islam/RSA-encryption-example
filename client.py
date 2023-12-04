import socket
import rsa

public_key, private_key = rsa.newkeys(1024)

def main():
    server_address = 'localhost'
    server_port = 5555
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_address, server_port))
        print("Connected to the server at {}:{}".format(server_address, server_port))
        
        # Exchange keys
        client_socket.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))
        print("Received public key from the server:", public_partner)

        # Send encrypted message
        message = "Hello, Server!"
        encrypted_message = rsa.encrypt(message.encode(), public_partner)
        client_socket.send(encrypted_message)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error:", e)
    
    client_socket.close()
    print("Program has finished.")

if __name__ == "__main__":
    main()
