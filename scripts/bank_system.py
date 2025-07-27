import socket
from models.bank import Bank, process_transaction
from models.blockchain import BlockChain
import json

bank_host = "127.0.0.1"
bank_port = 8080

banks: list[Bank] = []
blockchain = BlockChain()


def gen_banks():
    # generate 3 banks with 2 users and 2 merchants each
    banks.append(Bank("SBI", "SBIN0001"))
    banks.append(Bank("HDFC", "HDFC0001"))
    banks.append(Bank("ICICI", "ICICI0001"))

    banks[0].register_user("John Doe", "password123", "1234", 1000, "9876543210")
    banks[0].register_user("Jane Doe", "password123", "5678", 2000, "9876543211")

    banks[0].register_merchant("Merchant 1", "password123", 5000)
    banks[0].register_merchant("Merchant 2", "password123", 10000)

    banks[1].register_user("Alice", "password123", "1111", 1500, "9876543212")
    banks[1].register_user("Bob", "password123", "2222", 2500, "9876543213")

    banks[1].register_merchant("Merchant 3", "password123", 7000)
    banks[1].register_merchant("Merchant 4", "password123", 12000)

    banks[2].register_user("Charlie", "password123", "3333", 3000, "9876543214")
    banks[2].register_user("Dave", "password123", "4444", 3500, "9876543215")

    banks[2].register_merchant("Merchant 5", "password123", 8000)
    banks[2].register_merchant("Merchant 6", "password123", 15000)


def main():
    gen_banks()
    # save the banks to a file
    with open("banks.json", "w") as f:
        json.dump([bank.to_dict() for bank in banks], f)


if __name__ == "__main__":
    # if the banks.json file does not exist, generate banks
    try:
        with open("banks.json", "r") as f:
            banks = json.load(f)
            banks = [Bank.from_dict(bank) for bank in banks]
    except FileNotFoundError:
        print("banks.json file not found, generating new banks...")
        main()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((bank_host, bank_port))
    server.listen(5)

    print(f"Bank Server Running on Port {bank_port}...")

    while True:
        # Accept a client connection
        client_socket, client_address = server.accept()
        print(f"Connection established with {client_address}")

        # Receive data from the client
        data = client_socket.recv(1024).decode()
        if not data:
            print("No data received from client.")
            client_socket.close()
            continue

        print("Received data:", data)
        transaction = json.loads(data)
        print("Transaction:", transaction)

        # Process the transaction
        print(transaction)
        res = process_transaction(
            banks=banks,
            amount=transaction["amount"],
            mmid=transaction["mmid"],
            pin=transaction["pin"],
            mid=transaction["mid"],
            blockchain=blockchain,
        )
        print("Transaction Status:", res["status"])
        print("Transaction Message:", res["message"])

        # Send response back to the client
        response = {"status": res["status"], "message": res["message"]}
        client_socket.send(json.dumps(response).encode())

        # save json
        with open("banks.json", "w") as f:
            json.dump([bank.to_dict() for bank in banks], f)

        # Close the client connection
        client_socket.close()
