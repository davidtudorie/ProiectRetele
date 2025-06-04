# Centratea

Centratea este un joc multiplayer in care jucatorii incearca sa ghiceasca un numar secret generat de server. Jocul permite mai multi jucatori sa se conecteze simultan si sa concureze pentru a ghici numarul in cat mai putine incercari.

## Descriere

- Serverul genereaza un numar secret de 4 cifre diferite.
- Jucatorii se conecteaza la server folosind un nume unic.
- Fiecare jucator poate trimite o incercare pentru a ghici numarul secret.
- Serverul raspunde cu:
  - **Centrate**: cifre corecte pe pozitia corecta.
  - **Necentrate**: cifre corecte, dar pe pozitia gresita.
- Serverul notifica toti jucatorii cand cineva ghiceste numarul secret si incepe o noua runda.

## Instalare

1. Cloneaza acest repository sau descarca fisierele.
2. Asigura-te ca ai Python instalat pe sistemul tau.

## Utilizare

### Pornire server

1. Deschide un terminal.
2. Ruleaza comanda:
   ```bash
   python server.py
   ```

### Conectare client

1. Deschide un terminal.
2. Ruleaza comanda:
   ```bash
   python client.py
   ```
3. Introdu un nume unic pentru a te conecta la server.

### Comenzi client

- **numar**: Introdu un numar de 4 cifre diferite.
- **`stats`**: Afiseaza numarul de incercari ale celorlalti jucatori.
- **`quit`**: Deconecteaza-te de la server.
