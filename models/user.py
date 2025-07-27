import time

from utils.helpers import simple_hash


class User:
    def __init__(
        self, name, ifsc_code, password, pin, balance, mobile, uid=None, mmid=None
    ):
        self.name = name
        self.ifsc_code = ifsc_code
        self.password = password
        self.pin = pin
        self.balance = balance
        self.mobile_number = mobile
        self.uid = uid if uid else simple_hash(name + str(time.time()) + password)
        self.mmid = mmid if mmid else simple_hash(self.uid + self.mobile_number)

    def to_dict(self):
        return {
            "name": self.name,
            "ifsc_code": self.ifsc_code,
            "password": self.password,
            "pin": self.pin,
            "balance": self.balance,
            "mobile_number": self.mobile_number,
            "uid": self.uid,
            "mmid": self.mmid,
        }

    @staticmethod
    def from_dict(data):
        return User(
            name=data["name"],
            ifsc_code=data["ifsc_code"],
            password=data["password"],
            pin=data["pin"],
            balance=data["balance"],
            mobile=data["mobile_number"],
            uid=data["uid"],
            mmid=data["mmid"],
        )
