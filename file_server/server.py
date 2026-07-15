import socket
import threading
import os

# Resolve absolute path dependencies to handle execution context safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "server_storage")

HOST = '0.0.0.0'  # Listen on all interfaces inside the Codespace
PORT = 9999

def handle_client(client_socket, addr):
    print(f"[+] New connection from {addr}")
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            
            command, *args = request.split()
            
            if command == "LIST":
                files = os.listdir(STORAGE_DIR)
                client_socket.send("\n".join(files).encode('utf-8') if files else b"Empty storage")
                
            elif command == "DOWNLOAD":
                filename = args[0] if args else ""
                filepath = os.path.join(STORAGE_DIR, filename)
                if filename and os.path.exists(filepath):
                    client_socket.send(b"OK")
                    with open(filepath, 'rb') as f:
                        client_socket.sendall(f.read())
                else:
                    client_socket.send(b"ERROR: File not found")
                    
            elif command == "UPLOAD":
                filename = args[0] if args else ""
                filepath = os.path.join(STORAGE_DIR, filename)
                client_socket.send(b"READY")
                
                # Receive file data
                with open(filepath, 'wb') as f:
                    while True:
                        data = client_socket.recv(4096)
                        if b"EOF" in data: # Basic delimiter for end of transmission
                            f.write(data.replace(b"EOF", b""))
                            break
                        f.write(data)
                client_socket.send(b"SUCCESS")

            elif command == "DELETE":
                filename = args[0] if args else ""
                filepath = os.path.join(STORAGE_DIR, filename)
                
                # Prevent path traversal attacks and verify file exists
                if filename and os.path.exists(filepath) and os.path.isfile(filepath):
                    os.remove(filepath)
                    client_socket.send(b"SUCCESS: File deleted from server.")
                else:
                    client_socket.send(b"ERROR: File not found on server.")
    except Exception as e:
        print(f"[-] Error handling client {addr}: {e}")
    finally:
        client_socket.close()
        print(f"[-] Connection closed with {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}")
    
    while True:
        client_sock, addr = server.accept()
        # Handle multiple clients asynchronously using threading
        client_handler = threading.Thread(target=handle_client, args=(client_sock, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
