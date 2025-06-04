import socket
import threading
import random
import json

class CentrateaServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = {}
        self.secret_number = self.generate_secret_number()
        self.attempts = {}
        
    def generate_secret_number(self):
        digits = list(range(10))
        random.shuffle(digits)
        return ''.join(map(str, digits[:4]))
    
    def calculate_score(self, guess, secret):
        centrate = 0
        necentrate = 0
        
        for i in range(4):
            if guess[i] == secret[i]:
                centrate += 1
            elif guess[i] in secret:
                necentrate += 1
                
        return centrate, necentrate
    
    def broadcast_message(self, message, exclude_client=None):
        for client_socket, client_name in self.clients.items():
            if client_socket != exclude_client:
                try:
                    client_socket.send(message.encode())
                except:
                    pass
    
    def handle_client(self, client_socket, address):
        try:
            client_name = client_socket.recv(1024).decode().strip()
            
            if client_name in self.clients.values():
                client_socket.send("Nume deja folosit".encode())
                client_socket.close()
                return
                
            self.clients[client_socket] = client_name
            self.attempts[client_name] = 0
            
            print(f"Client {client_name} conectat de la {address}")
            client_socket.send("Conectat cu succes! Ghiceste numarul de 4 cifre diferite.".encode())
            
            while True:
                guess = client_socket.recv(1024).decode().strip()
                
                if not guess or len(guess) != 4 or not guess.isdigit():
                    client_socket.send("Introdu un numar de 4 cifre!".encode())
                    continue
                
                if len(set(guess)) != 4:
                    client_socket.send("Cifrele trebuie sa fie diferite!".encode())
                    continue
                
                self.attempts[client_name] += 1
                centrate, necentrate = self.calculate_score(guess, self.secret_number)
                
                if centrate == 4:
                    win_message = f"{client_name} a ghicit numarul {self.secret_number} in {self.attempts[client_name]} incercari!"
                    self.broadcast_message(win_message)
                    client_socket.send(f"Felicitari! Ai ghicit numarul {self.secret_number}!".encode())
                    
                    self.secret_number = self.generate_secret_number()
                    self.attempts = {name: 0 for name in self.attempts}
                    
                    print(f"Numar nou generat: {self.secret_number}")
                    self.broadcast_message("Joc nou inceput!")
                else:
                    response = f"Centrate: {centrate}, Necentrate: {necentrate}"
                    client_socket.send(response.encode())
                    
        except Exception as e:
            print(f"Eroare cu clientul {address}: {e}")
        finally:
            if client_socket in self.clients:
                del self.clients[client_socket]
            client_socket.close()
    
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"Serverul porneste pe {self.host}:{self.port}")
        print(f"Numarul secret este: {self.secret_number}")
        
        try:
            while True:
                client_socket, address = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("Serverul se opreste...")
        finally:
            server_socket.close()

if __name__ == "__main__":
    server = CentrateaServer()
    server.start_server()