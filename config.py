import json
from pathlib import Path
import dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import sys
import dotenv

ACCOUNTS = []

with open("proxy.txt", "r") as file:
    PROXIES = [row.strip() for row in file]

with open("addresses.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

if ACCOUNTS.count == 0:
    raise ValueError('Accounts array is empty')
