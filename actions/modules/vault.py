import os
import hvac
import requests
import json
from Crypto.PublicKey import RSA
from Crypto import Random
from .config import *

class Vault(object):
    def __init__(self, token):
        self.client = hvac.Client(url=VAULT_URL, token=token)
        self.token = token
        self.username = self.client.lookup_token()['data']['meta']['username']

    def read(self, key, path="path"):
        return self.client.read(f"secret_zone/{path}/{self.username}/{key}")['data']['value']\

   