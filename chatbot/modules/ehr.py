import uuid, os, json, bip39, requests
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair, CryptoKeypair
from datetime import datetime
from encryption import *
from vault import Vault, Config

config = Config(
    authority=["create", "read", "update", "delete", "list", "sudo"],
	path='path',
	policy='auth_policy',
	endpoint='http://192.168.33.150:8200',
	username="username",
	secretMountPoint='secret_data',
    token="myroot",
	certificateMountPoint="certificate"
)
vault = Vault(config)

def write(key, value):
    vault.write(key, value)
def read(key):
    return vault.read(key)

bdb = BigchainDB('http:192.168.33.160:9984/api/v1')
class User(object):
    def __init__(self, email=None, schema=None, password=None):
        self.registered = None
        self.records = None
        self.user = self.get_bio(email, schema)
        if not self.registered:
            self.user = self.create_user(email, schema)
        if self.records == None:
            self.get_records()

    def get_bio(self, email, schema, password):
        records = bdb.assets.get(search=self.email)
        records = filter(records, 'schema', schema)

        if len(records) == 1:
            self.registered = True
            vault.login(password, email)
            self.read_keys()
            return records[0]['data']
        
        self.registered = False
        return

    def write_keys(self, email):
        self.bigchain_keys = generate_keypair(encrypt(email, email))
        random_generator = Random.new().read
        self.rsa_keys = RSA.generate(1024, random_generator)
        value = [self.bigchain_keys.private_key, self.bigchain_keys.public_key,
                self.rsa_keys.privatekey().exportKey().decode('utf-8'),
                self.rsa_keys.publickey().exportKey().decode('utf-8')]
        keys = ['bigchain_private_key', 'bigchain_public_key', 'rsa_private_key', 'rsa_public_key']
        for key,value in zip(keys,value):
            self.write(vault.write(key, value))

    def read_keys(self):
        self.bigchain_keys.private_key = read('bigchain_private_key')
        self.bigchain_keys.public_key = read('bigchain_public_key')
        self.rsa_keys.private_key = read('rsa_private_key')
        self.rsa_keys.public_key = read('rsa_public_key')


    def create_user(self, email, schema, password):
        vault.signup(password, email)
        self.write_keys(email)
        data = {
            'schema': schema,
            'email': email,
            'date': datetime.now()
            'bigchain_key': self.bigchain_keys.public_key,
            'rsa_key': self.rsa_keys.publickey().exportKey().decode('utf-8')
        }
        tx = bdb.transactions.prepare(
            operation='CREATE',
            signers=self.bigchain_keys.public_key,
            asset={'data': data}
        )
        signed_tx = bdb.transactions.fulfill(
            tx,
            private_keys=self.bigchain_keys.private_key
        )
        sent = bdb.transactions.send(signed_tx)
        self.registered = True
        return sent.asset.data

    def get_records(self):
        if self.records is None:
            self.records = bdb.assets.get(search=self.user)
        return list(filter(lambda record: record if record.get('schema') == "record" and 
                                self.record.get("user").get('bigchain_key') == self.user.bigchain_key, self.records))

    def get_single_file(self, description):
        return filter(lambda record : record['form']['description'] == description, self.records)['file']

    def get_transaction_history(self):
        pass

    def write_record(self, ipfs_hash, form):
        id = uuid.uuid4()
        data = {
            'schema': 'record'
            'form': form
            'user': self.bio['user'],
            'file': ipfs_hash,
            'file_hash': hash(ipfs_hash)
            'id' : id,
            'date': datetime.now(),
        }
        metadata = {
            'doclist': [],
            'id': id
            'date': datetime.now()
        }
        
        tx = bdb.transactions.prepare(
            operation='CREATE',
            signers=current_user['bigchain'].public_key,
            asset={'data': data},
            metadata=metadata
        )
        signed_tx = bdb.transactions.fulfill(
            tx,
            private_keys=current_user['bigchain'].private_key
        )
        sent = bdb.transactions.send(signed_tx)
        return sent 

    def transfer_medblock(self, tx, ):
        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': 0,
                'transaction_id': tx['id'],},
            'owners_before': output['public_keys'],}
        if tx['operation'] == 'TRANSFER':
            asset_id = tx['asset']['id']
        else:
            asset_id = tx['id']

        transfer_asset = {
            'id':asset_id,
        }
        if metadata is None:
            prepared_tx = bdb.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                recipients=self.bio['bigchain'],
            )
        else:
            prepared_tx = bdb.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                recipients=self.bio['bigchain'],
                metadata=metadata
            )
        signed = bdb.transactions.fulfill(
            prepared_tx,
            private_keys=current_user['bigchain'].private_key
        )
        for attempt in range(10):
            block = bdb.blocks.get(txid=tx['id'])
    
        tx = bdb.transactions.send(signed)




    
    
    

    
   

   