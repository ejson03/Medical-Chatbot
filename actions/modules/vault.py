import os
import hvac
import requests
import json
from Crypto.PublicKey import RSA
from Crypto import Random
from .config import *


class Config(object):
    def __init__(self, authority=[], path="data", policy="AppPolicy", 
                    endpoint=VAULT_URL, username="", 
                    secretMountPoint="secret", certificateMountPoint="certificate", 
                    token=VAULT_TOKEN):
        self.path = path
        self.policy = policy
        self.authority = authority
        self.endpoint=endpoint
        self.username = username
        self.secretMountPoint = secretMountPoint
        self.certificateMountPoint = certificateMountPoint
        self.token = token

class Vault(object):
    def __init__(self, config):
        self.config = config
        self.config.secretMountPoint = config.secretMountPoint.lower()
        self.config.path = f"{config.secretMountPoint}/{config.path}".lower()
        self.config.policy = config.policy.lower()
        self.config.username = config.username.lower()
        self.client = hvac.Client(self.config.endpoint, self.config.token) 

    def setup(self):
        self.initVault()
        self.enable()
        self.mount()

    def initVault(self):
        if self.client.sys.is_initialized():
            return
        shares = 1
        threshold = 1
        init = self.client.sys.initialize(shares, threshold)
        self.client.token = init['root_token']
        keys = init['keys'][0]
        self.client.sys.submit_unseal_key(keys)

    def enable(self):
        if 'userpass/' not in self.client.sys.list_auth_methods().keys():
            self.client.sys.enable_auth_method('userpass')

    def mount(self):
        mount = self.client.sys.list_mounted_secrets_engines()['data']
        if f"{self.config.path}/" not in mount.keys():
            self.client.sys.enable_secrets_engine(
                backend_type='kv',
                path= self.config.path
            )

    def listPolicy(self):
        try:
            policies = self.client.sys.list_policies()['data']['policies']
            return policies
        except:
            return []

    def addPolicy(self, policy=None, 
                mount_point=None, 
                authority=None, 
                policy_add=False):

        if(policy==None):
            policy=self.config.policy 
            mount_point=self.config.path 
            authority=self.config.authority
            policy_add=False

        if(not policy_add):
            policies = self.listPolicy()
            print("policies are : ", policies)
            if(f"{policy}/{self.config.username}" in policies):
                return None

        self.config.policy = f"{policy}/{self.config.username}"
        authority = json.dumps(authority, separators=(',', ':'))
        return self.client.sys.create_or_update_policy(
            name=self.config.policy,
            policy= f'path \"{mount_point}/{self.config.username}/*\" {{ capabilities = {authority} }}'
        )

    def writeRoute(self, password, username=None, policy=None):
        users = self.getUsers()
        print("USERS are: ", users)
        if username in users:
            return None
        self.config.username = username
        self.addPolicy()
        self.client.write(
            f'auth/userpass/users/{username}', 
            **{'password': password,  'policies': self.config.policy}
        )

    def getUsers(self):
        try:
            users = self.client.list('auth/userpass/users').get('data').get('keys')
            return users
        except:
            return []

    def signUp(self, password, username=None, policy=None):
        if(policy==None):
            policy=self.config.policy
        self.writeRoute(password, username, policy)
        self.config.username = username
        return self.client.create_userpass(self.config.username, password, self.config.policy)

    def login(self, password, username=None):
        if(username==None):
            username = self.config.username
        users = self.getUsers()
        if not username in users:
            raise Exception("User doesnt exist...")
        user = self.client.auth_userpass(username, password)
        self.config.username = username
        return user

    def write(self, key, value):
        return self.client.write(f"{self.config.path}/{self.config.username}/{key}",
                                **{"value": value})

    def read(self, key):
        return self.client.read(f"{self.config.path}/{self.config.username}/{key}")['data']['value']



config = Config(
    authority=["create", "read", "update", "delete", "list", "sudo"],
	path='path',
	policy='auth_policy',
	endpoint=VAULT_URL,
	username="username",
	secretMountPoint='secret_data',
    token=VAULT_TOKEN,
	certificateMountPoint="certificate"
)
if __name__ =='__main__':
    vault = Vault(config)
    vault.setup()
    # response = vault.login('12345678', 'sherwyn')
    # print(response)
    # print(vault.write("shaka", "moomzaga"))
    # print(vault.read("shaka"))
    # # random_generator = Random.new().read
    # # rsa_key = RSA.generate(1024, random_generator)
    # # response = vault.login('12345678', 'sherwyn')
    # # write = vault.write("shake", rsa_key.publickey().exportKey().decode('utf-8'))
    # # read = vault.read("shake")
    # # print(write)
    # # print(read)
    # response = vault.signUp('12345678', 'darlene')
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024, random_generator)
    response = vault.login('12345678', 'shewryn')
    write = vault.write("shake", rsa_key.publickey().exportKey().decode('utf-8'))
    read = vault.read("shake")
    print(write)
    print(read)

