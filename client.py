import socket
import threading

class CentrateaClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = False
    
    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(f"Server: {message}")
                else:
                    break
            except:
                break
    
    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            
            name = input("Introdu numele tau: ")
            self.client_socket.send(name.encode())
            
            response = self.client_socket.recv(1024).decode()
            print(f"Server: {response}")
            
            if "deja folosit" in response:
                self.client_socket.close()
                return False
            
            self.running = True
            
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Eroare la conectare: {e}")
            return False
    
    def play_game(self):
        if not self.connect_to_server():
            return
        
        print("Scrie 'quit' pentru a iesi din joc")
        
        try:
            while self.running:
                guess = input("Ghiceste numarul (4 cifre diferite): ")
                
                if guess.lower() == 'quit':
                    break
                
                if len(guess) != 4 or not guess.isdigit():
                    print("Introdu exact 4 cifre!")
                    continue
                
                if len(set(guess)) != 4:
                    print("Cifrele trebuie sa fie diferite!")
                    continue
                
                self.client_socket.send(guess.encode())
                
        except KeyboardInterrupt:
            print("\nIesire din joc...")
        finally:
            self.running = False
            if self.client_socket:
                self.client_socket.close()

if __name__ == "__main__":
    client = CentrateaClient()
    client.play_game()