import socket
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(BASE_DIR, "client_workspace")

HOST = '127.0.0.1'
PORT = 9999

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    print("Connected to File Server. Options: LIST, DOWNLOAD <filename>, UPLOAD <filename>, EXIT")
    
    while True:
        cmd_input = input("Enter command: ")
        if cmd_input.upper() == "EXIT":
            break
            
        client.send(cmd_input.encode('utf-8'))
        parts = cmd_input.split()
        command = parts[0].upper()
        
        if command == "LIST":
            response = client.recv(4096).decode('utf-8')
            print(f"Server Directory Layout:\n{response}")
            
        elif command == "DOWNLOAD":
            filename = parts[1]
            response = client.recv(1024).decode('utf-8')
            if response == "OK":
                filepath = os.path.join(WORKSPACE_DIR, filename)
                data = client.recv(1024 * 1024) # 1MB limit for proof of concept
                with open(filepath, 'wb') as f:
                    f.write(data)
                print("[+] Download complete.")
            else:
                print(response)
                
        elif command == "UPLOAD":
            filename = parts[1]
            filepath = os.path.join(WORKSPACE_DIR, filename)
            if not os.path.exists(filepath):
                print("[-] Local file does not exist.")
                continue
                
            response = client.recv(1024).decode('utf-8')
            if response == "REPyADY":
                with open(filepath, 'rb') as f:
                    client.sendall(f.read())
                client.send(b"EOF") # Signal completion
                status = client.recv(1024).decode('utf-8')
                print(f"[+] Server status: {status}")

    
        elif command == "DELETE":
            if len(parts) < 2:
                print("[-] Please specify a filename. Usage: DELETE <filename>")
                continue
                
            response = client.recv(1024).decode('utf-8')
            print(f"[+] Server status: {response}")
    client.close()     
if __name__ == "__main__":
    main()