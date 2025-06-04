import socket
import threading
import sys
import time

class CentrateaClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = False
        self.name = None
    
    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    if self.name in message:
                        print(f"{message}")
                    else:
                        print(f"Server: {message}")
                    time.sleep(0.1)
            except:
                print("Conexiunea cu serverul a fost inchisa.")
                self.running = False
                break
    
    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            
            while True:
                self.name = input("Introdu numele tau (minim 3 caractere): ").strip()
                if len(self.name) >= 3:
                    break
                print("Numele trebuie sa aiba minim 3 caractere!")
            
            self.client_socket.send(self.name.encode())
            
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
            
        except ConnectionRefusedError:
            print("Nu s-a putut realiza conexiunea cu serverul. Verifica daca serverul ruleaza.")
            return False
        except Exception as e:
            print(f"Eroare la conectare: {e}")
            return False
    
    def validate_guess(self, guess):
        if guess.lower() == 'quit' or guess.lower() == 'stats':
            return True, guess
        
        if len(guess) != 4 or not guess.isdigit():
            print("Eroare: Introdu exact 4 cifre!")
            return False, None
        
        if len(set(guess)) != 4:
            print("Eroare: Cifrele trebuie sa fie diferite!")
            return False, None
            
        return True, guess
    
    def play_game(self):
        if not self.connect_to_server():
            return
        
        print("Instructiuni:")
        print("- Ghiceste un numar de 4 cifre diferite")
        print("- Vei primi feedback despre cate cifre sunt:")
        print("  * Centrate (cifre corecte pe pozitia corecta)")
        print("  * Necentrate (cifre corecte dar pe pozitie gresita)")
        print("- Scrie 'quit' pentru a iesi din joc")
        print("- Scrie 'stats' pentru a vedea incercarile celorlalti jucatori\n")
        
        try:
            while self.running:
                guess = input("Ghiceste numarul (4 cifre diferite), 'stats' sau 'quit': ")
                
                valid, validated_guess = self.validate_guess(guess)
                if not valid:
                    continue
                
                if validated_guess == "quit":
                    try:
                        self.client_socket.send("quit".encode())
                    except:
                        pass
                    break
                
                self.client_socket.send(validated_guess.encode())
                
        except KeyboardInterrupt:
            print("Iesire din joc...")
        except Exception as e:
            print(f"Eroare neasteptata: {e}")
        finally:
            self.running = False
            if self.client_socket:
                self.client_socket.close()

if __name__ == "__main__":
    client = CentrateaClient()
    client.play_game()