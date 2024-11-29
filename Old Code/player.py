import json


class Player:
    def __init__(self, username, symbol, sock):
        self.username = username
        self.symbol = symbol
        self.sock = sock
        self.active = True