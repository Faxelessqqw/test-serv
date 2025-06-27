import socket  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
server_socket.bind(('localhost', 12345))  
server_socket.listen(5)  
print("Сервер запущен. Ожидание подключений...")  
while True:  
    client_socket, address = server_socket.accept()  
    print(f"Подключение от {address}")  
    message = client_socket.recv(1024).decode('utf-8')  
    print(f"Получено сообщение: {message}")  
    client_socket.send("Привет от сервера!".encode('utf-8'))  
    client_socket.close()  