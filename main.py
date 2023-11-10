import socket
import signal
import threading
import time

# Telnetサーバーのホストとポート
HOST = '0.0.0.0'  # ホストIPアドレス
PORT = 14674  # ポート番号（任意のポートを選択）
flag = 0  # flagの初期化
ver = "0.1"  # バージョン


# Ctrl+Cで終了するためのハンドラを設定
def signal_handler(sig, frame):
    print('Telnetサーバーを終了します。')
    exit(0)


# クライアントとの通信を処理するスレッド
def handle_client(client_socket, client_address):
    # Telnetセッションを開始
    print(f"{client_address[0]} が接続しました。")
    client_socket.send(b'\x1b[H\x1b[J')
    f = open("rick.txt", "r")
    rick_source = f.readlines()
    f.close()
    for rick in rick_source:
        client_socket.send(rick.encode("utf-8"))
        time.sleep(0.04)
    # 画面を消去
    client_socket.send(b'\x1b[H\x1b[J')
    client_socket.send("Disconnect after 5 seconds...\r\n".encode("utf-8"))
    time.sleep(5)
    client_socket.close()


print(f"Telickroll Version {ver}\n")
signal.signal(signal.SIGINT, signal_handler)
# ソケットを作成してバインド
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        server_socket.bind((HOST, PORT))
        break
    except OSError:
        print(f"システムが{PORT}番ポートを使用中です、10秒後に再試行します。")
        time.sleep(10)
        continue
server_socket.listen(10)  # 接続を待ち受ける最大クライアント数
print(f"{PORT}番ポートでTelnetチャットが起動しました\n")

while True:
    client_socket, client_address = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
