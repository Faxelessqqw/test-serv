import socket  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
client_socket.connect(('localhost', 8080))  
client_socket.send("Привет, сервер!".encode('utf-8'))  
response = client_socket.recv(1024).decode('utf-8')  
print(f"Ответ от сервера: {response}")  
client_socket.close()  