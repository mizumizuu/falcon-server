import json
import socket 
import threading

conns = dict()

with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)

SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = settings.get("SERVER")
PORT = int(settings.get("PORT"))
DC_MSG = settings.get("DC_MSG")
MAX_BYTES = int(settings.get("MAX_BYTES"))
FORMAT = settings.get("FORMAT")
ADDR = (SERVER, PORT)

def format_msg(addr, msg):
    return f"[{addr}:{PORT}]: {msg}".encode(FORMAT)

def handle_client(conn, addr):
    connected = True
    while connected:
        data = conn.recv(MAX_BYTES)
        if not data:
            continue
        msg = data.decode(FORMAT)
        if msg == DC_MSG:
            conn.sendall(DC_MSG.encode(FORMAT))
            break
        for k in conns:
            msg = format_msg(addr, msg)
            k.sendall(msg)
    del conns[conn]
    conn.close()

def main():
    print(f"listening on {ADDR}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVER, PORT))
        server.listen()
        while True:
            conn, addr = server.accept()
            print(f"{addr} connected")
            conns[conn] = conn
            threading.Thread(target=handle_client, args=[conn, addr]).start()
            print(f"{threading.active_count() - 1} active users")

main()
