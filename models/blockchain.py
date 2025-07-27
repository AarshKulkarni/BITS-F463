import hashlib
import json
import time


class Block:
    def __init__(self, index, timestamp, data, previous_hash=""):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = (
            f"{self.index}{self.previous_hash}{self.timestamp}{self.data}".encode()
        )

        return hashlib.sha256(block_string).hexdigest()


class BlockChain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_genesis_block(self):
        genesis_block = Block(0, str(time.time()), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    # data is a dictionary
    def add_block(self, data):
        b = Block(
            index=len(self.chain),
            timestamp=str(time.time()),
            data=str(data),  # Convert dictionary to string for hashing
            previous_hash=self.get_last_block().hash,
        )

        self.chain.append(b)

    def check_is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if (
                current.hash != current.calculate_hash()
                or current.previous_hash != previous.hash
            ):
                return False

        return True

    def save_chain(self):
        with open("blockchain.json", "w") as f:
            json.dump([block.__dict__ for block in self.chain], f)

    def load_chain(self):
        try:
            with open("blockchain.json", "r") as f:
                data = json.load(f)
                self.chain = [Block(**block) for block in data]
        except FileNotFoundError:
            print("No blockchain file found, creating a new one.")
            self.create_genesis_block()

    def print_chain(self):
        for block in self.chain:
            print(
                f"Index: {block.index}, Timestamp: {block.timestamp}, Data: {block.data}, Hash: {block.hash}, Previous Hash: {block.previous_hash}"
            )

    def get_chain(self):
        return [block.__dict__ for block in self.chain]
