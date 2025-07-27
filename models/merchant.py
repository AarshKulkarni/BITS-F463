import time
from utils.helpers import simple_hash

from speck import SpeckCipher


class Merchant:
    def __init__(self, name, ifsc_code, password, initial_balance, mid=None, vmid=None):
        self.name = name
        self.ifsc_code = ifsc_code
        self.password = password
        self.balance = initial_balance
        if mid is None:
            self.mid = simple_hash(name + str(time.time()) + password)
        else:
            self.mid = mid
        if vmid is None:
            speck = SpeckCipher(0x123456789ABCDEF00FEDCBA987654321)
            temp = int(self.mid, 16)  # Convert the complete mid to an integer
            self.vmid = str(speck.encrypt(temp))
        else:
            self.vmid = vmid

    def to_dict(self):
        return {
            "name": self.name,
            "ifsc_code": self.ifsc_code,
            "password": self.password,
            "balance": self.balance,
            "mid": self.mid,
            "vmid": self.vmid,
        }

    @staticmethod
    def from_dict(data):
        merchant = Merchant(
            name=data["name"],
            ifsc_code=data["ifsc_code"],
            password=data["password"],
            initial_balance=data["balance"],
            mid=data["mid"],
            vmid=data["vmid"],
        )
        return merchant
