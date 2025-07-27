import socket
import json

upi_host = "0.0.0.0"
upi_port = 5001


def start_upi_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((upi_host, upi_port))
    server.listen(5)
    print(f"UPI Machine Running on Port {upi_port}...")

    while True:
        client, addr = server.accept()
        print(f"Received connection from {addr}")

        data = client.recv(1024).decode()
        if not data:
            print("Error: Received empty transaction data!")
            client.close()
            continue

        print("Transaction received:", data)
        transaction = json.loads(data)

        # Forward request to Bank
        bank_host = "127.0.0.1"
        bank_port = 8080
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bank_socket:
            try:
                bank_socket.connect((bank_host, bank_port))
                bank_socket.send(json.dumps(transaction).encode())
                response = bank_socket.recv(1024).decode()
                print("Response from Bank:", response)
            except Exception as e:
                print("Error: Could not connect to Bank Server!", str(e))
                response = json.dumps(
                    {"status": "failed", "message": "Bank Server Error"}
                )

        # Send response to User Device
        client.send(response.encode())
        client.close()


if __name__ == "__main__":
    start_upi_server()
