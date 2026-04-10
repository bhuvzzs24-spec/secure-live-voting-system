import socket
import ssl
import threading
import config
from security import verify_hmac

votes = {"A": 0, "B": 0, "C": 0}
voted_clients = set()
clients = []

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", config.SERVER_PORT))
server_socket.listen(5)

print("🔐 Secure TLS Voting Server running...")


def handle_client(client_socket, addr):
    print(f"📡 Client connected: {addr}")

    try:
        while True:
            data = client_socket.recv(config.BUFFER_SIZE).decode()
            if not data:
                break

            parts = data.split("|")

            if len(parts) != 3:
                client_socket.send("Invalid format".encode())
                continue

            client_id, vote, received_hmac = parts
            message = f"{client_id}|{vote}"

            # 🔐 HMAC verification
            if not verify_hmac(message, received_hmac):
                client_socket.send("⚠️ Tampered message detected!".encode())
                continue

            # 🚫 Duplicate vote prevention
            if client_id in voted_clients:
                client_socket.send("⚠️ You already voted!".encode())
                continue

            voted_clients.add(client_id)

            if vote in votes:
                votes[vote] += 1

            print(f"🗳️ Vote from {client_id}: {vote}")

            result = f"RESULTS | A={votes['A']} B={votes['B']} C={votes['C']}"

            # 📡 Broadcast results
            for c in clients:
                try:
                    c.send(result.encode())
                except:
                    pass

    except Exception as e:
        print("⚠️ Client error:", e)

    finally:
        print(f"❌ Client disconnected: {addr}")
        clients.remove(client_socket)
        client_socket.close()


while True:
    client_sock, addr = server_socket.accept()
    secure_client = context.wrap_socket(client_sock, server_side=True)

    clients.append(secure_client)

    threading.Thread(target=handle_client, args=(secure_client, addr)).start()

