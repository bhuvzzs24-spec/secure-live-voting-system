import socket
import ssl
import tkinter as tk
import threading
import config
from security import generate_hmac

server_ip = input("Enter Server IP: ")

context = ssl.create_default_context()
context.load_verify_locations("server.crt")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_sock = context.wrap_socket(sock, server_hostname=server_ip)

# 🔐 Connection + SSL validation
try:
    secure_sock.connect((server_ip, config.SERVER_PORT))
    print("✅ Secure connection established")

    cert = secure_sock.getpeercert()
    print("\n🔐 SSL HANDSHAKE SUCCESSFUL")
    print("Certificate Info:", cert)

except ssl.SSLCertVerificationError:
    print("❌ SSL verification failed")
    exit()

except ConnectionRefusedError:
    print("❌ Server not running or wrong IP")
    exit()

except Exception as e:
    print("❌ Connection error:", e)
    exit()


client_id = input("Enter Client ID: ")


def send_vote(option):
    msg = f"{client_id}|{option}"
    hmac_val = generate_hmac(msg)
    final_msg = f"{msg}|{hmac_val}"

    secure_sock.send(final_msg.encode())


def listen_server():
    while True:
        try:
            data = secure_sock.recv(config.BUFFER_SIZE).decode()

            if "RESULTS" in data:
                parts = data.split("|")[1].split()
                result_text = f"A: {parts[0].split('=')[1]}   B: {parts[1].split('=')[1]}   C: {parts[2].split('=')[1]}"
                result_label.config(text=result_text)
            else:
                result_label.config(text=data)

        except:
            break


# 🎨 GUI
root = tk.Tk()
root.title("Live Poll Voting")
root.geometry("500x400")
root.configure(bg="#1e1e2f")

title = tk.Label(root, text="🗳️ LIVE POLL SYSTEM", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2f")
title.pack(pady=20)

btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=20)

btnA = tk.Button(btn_frame, text="A", font=("Arial", 16), width=8, bg="#4CAF50", fg="white",
                 command=lambda: send_vote("A"))
btnA.grid(row=0, column=0, padx=10)

btnB = tk.Button(btn_frame, text="B", font=("Arial", 16), width=8, bg="#2196F3", fg="white",
                 command=lambda: send_vote("B"))
btnB.grid(row=0, column=1, padx=10)

btnC = tk.Button(btn_frame, text="C", font=("Arial", 16), width=8, bg="#f44336", fg="white",
                 command=lambda: send_vote("C"))
btnC.grid(row=0, column=2, padx=10)

result_title = tk.Label(root, text="📊 RESULTS", font=("Arial", 16, "bold"), fg="white", bg="#1e1e2f")
result_title.pack(pady=10)

result_label = tk.Label(root, text="Waiting for votes...", font=("Arial", 14), fg="white", bg="#1e1e2f")
result_label.pack(pady=10)

threading.Thread(target=listen_server, daemon=True).start()

root.mainloop()