# Secure Live Voting System

A Python-based secure voting system that uses TLS (SSL) for encrypted communication and HMAC (SHA-256) for message integrity. Clients can vote (A/B/C) through a GUI and receive live results from the server.

---

## Files in this Project

- client_gui.py – GUI client that connects to the server securely, sends votes, and displays live results  
- server.py – TLS-enabled server that handles clients, verifies votes, and broadcasts results  
- security.py – Handles HMAC generation and verification  
- config.py – Stores server port and buffer size  
- generate_cert.py – Generates SSL certificate (server.crt) and private key (server.key)  
- server.crt – SSL certificate used for secure communication  
- server.key – Private key for the server  

---

## How to Run

### 1. Generate Certificate
python generate_cert.py

### 2. Start Server
python server.py

### 3. Run Client
python client_gui.py

---

## Working

- Client connects to server using SSL  
- User enters Client ID and selects a vote (A/B/C)  
- Vote is sent as:  
  clientID | vote | HMAC  
- Server verifies HMAC before accepting vote  
- Duplicate votes are rejected  
- Vote count is updated  
- Results are sent to all connected clients  
- GUI displays live results  

---

## Security Used

- TLS (SSL) for encrypted communication  
- HMAC (SHA-256) for message integrity  
- Client ID tracking to prevent multiple votes  
