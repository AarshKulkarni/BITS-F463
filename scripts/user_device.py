import socket
import json
from speck import SpeckCipher

user_host = "192.168.109.216"
user_port = 5001


def initiate_payment():
    mmid = input("Enter MMID: ")
    pin = input("Enter PIN: ")
    amount = input("Enter Amount: ")
    encrypted_mid = input("Enter encrypted MID from QR: ")

    encrypted_mid = int(encrypted_mid)
    speck = SpeckCipher(0x123456789ABCDEF00FEDCBA987654321)
    decrypted_mid = hex(speck.decrypt(encrypted_mid))

    print("Decrypted MID:", decrypted_mid)

    transaction = {
        "mmid": mmid,
        "pin": pin,
        "amount": amount,
        "mid": str(decrypted_mid)[2:],
    }

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((user_host, user_port))
    client.send(json.dumps(transaction).encode())

    response = client.recv(1024).decode()

    if not response:
        print("Error: No response from UPI Machine!")
        return

    try:
        response_data = json.loads(response)
        print("Transaction Status:", response_data["status"])
    except json.JSONDecodeError:
        print("Error: Received invalid JSON response!", response)


initiate_payment()
