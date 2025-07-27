import time
from models.blockchain import BlockChain
from models.merchant import Merchant
from models.user import User


class Bank:
    def __init__(self, bank_name: str, ifsc_code: str):
        self.name: str = bank_name
        self.ifsc_code: str = ifsc_code
        self.merchants: list[Merchant] = []
        self.users: list[User] = []

    def register_merchant(self, name: str, password: str, initial_balance: float):
        self.merchants.append(
            Merchant(
                name=name,
                ifsc_code=self.ifsc_code,
                password=password,
                initial_balance=initial_balance,
            )
        )
        print(f"Merchant Registered! MID: {self.merchants[-1].mid}")

    def register_user(self, name, password, pin, balance, mobile):
        self.users.append(
            User(
                name=name,
                ifsc_code=self.ifsc_code,
                password=password,
                pin=pin,
                balance=balance,
                mobile=mobile,
            )
        )
        print(f"User Registered! UID: {self.users[-1].uid}")

    def to_dict(self):
        return {
            "bank_name": self.name,
            "ifsc_code": self.ifsc_code,
            "merchants": [merchant.to_dict() for merchant in self.merchants],
            "users": [user.to_dict() for user in self.users],
        }

    @staticmethod
    def from_dict(data):
        bank = Bank(bank_name=data["bank_name"], ifsc_code=data["ifsc_code"])
        bank.merchants = [Merchant.from_dict(m) for m in data["merchants"]]
        bank.users = [User.from_dict(u) for u in data["users"]]
        return bank


def process_transaction(
    banks: list[Bank], mmid, mid, amount, pin, blockchain: BlockChain
):
    amount = float(amount)
    for bank in banks:
        for user in bank.users:
            if user.mmid == mmid and user.pin == pin:
                if user.balance < amount:
                    return {
                        "status": "failure",
                        "message": "Insufficient Balance",
                    }
                else:
                    for b in banks:
                        for merchant in b.merchants:
                            if merchant.mid == mid:
                                # update balances
                                user.balance -= amount
                                merchant.balance += amount
                                # update blockchain
                                blockchain.add_block(
                                    {
                                        "from": user.uid,
                                        "to": merchant.mid,
                                        "amount": amount,
                                        "timestamp": str(time.time()),
                                    }
                                )
                                # verify blockchain
                                if not blockchain.check_is_valid():
                                    return {
                                        "status": "failure",
                                        "message": "Transaction Failed, Blockchain Invalid",
                                    }
                                else:
                                    # save the blockchain
                                    blockchain.save_chain()
                                return {
                                    "status": "success",
                                    "message": "Transaction Successful",
                                }

                    return {
                        "status": "failure",
                        "message": "Merchant Not Found",
                    }

    return {"status": "failure", "message": "User Not Found"}
