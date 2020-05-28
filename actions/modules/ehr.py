import uuid, os, json, requests
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair, CryptoKeypair
from datetime import datetime
from encryption import *
from vault import Vault, Config

VAULT_URL = os.environ.get("VAULT_URL")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN")

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


bdb = BigchainDB('http://192.168.33.160:9984')
class User(object):
    def __init__(self, email=None, schema=None, password=None):
        self.registered = None
        self.records = None
        self.bigchain_keys = {}
        self.rsa_keys = {}
        self.vault = vault
        self.user = self.get_bio(email, schema, password)
        print("User is ", self.user)
        if not self.registered:
            self.user = self.create_user(email, schema, password)
            print("User is ", self.user)
        if self.records == None:
            self.records = self.get_records()
            print("REcords", self.records)

    def get_bio(self, email, schema, password):
        try:
            records = bdb.assets.get(search=email)
            records = list(filter(lambda record : record['data']['schema'] == schema, records))
            self.registered = True
            vault.login(password, email)
            self.read_keys()
            return records[0]['data']
        except:
            self.registered = False
            return

    def write_keys(self, email):
        self.secret_key = generate_random_aes_key()
        self.bigchain_keys = generate_keypair(encrypt(email, self.secret_key))
        self.rsa_keys = generate_rsa_key()
        value = [self.bigchain_keys.private_key, self.bigchain_keys.public_key,
                self.rsa_keys.exportKey().decode('utf-8'),
                self.rsa_keys.publickey().exportKey().decode('utf-8'), self.secret_key]
        keys = ['bigchain_private_key', 'bigchain_public_key', 'rsa_private_key', 'rsa_public_key', 'secret_key']
        for key,value in zip(keys,value):
            self.write(key, value)

    def read_keys(self):
        self.bigchain_keys['private_key'] = self.read('bigchain_private_key')
        self.bigchain_keys['public_key'] = self.read('bigchain_public_key')
        self.rsa_keys['private_key'] = self.read('rsa_private_key')
        self.rsa_keys['public_key'] = self.read('rsa_public_key')
        self.secret_key = self.read('secret_key')

    def write(self, key, value):
        self.vault.write(key, value)
    def read(self, key):
        return self.vault.read(key)

    def create_user(self, email, schema, password):
        vault.signUp(password, email)
        self.write_keys(email)
        data = {
            'schema': schema,
            'email': email,
            'date': datetime.now().strftime("%s"),
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
        sent = bdb.transactions.send_commit(signed_tx)
        self.registered = True
        return sent['asset']['data']

    def check(self,record):
        if record['data']['schema'] == 'record':
            if record['data']['user']['bigchain_key'] == self.user['bigchain_key']:
                return record
        elif record['data']['schema'] in ('patinet', 'doctor'):
            return record['data']['rsa_key']


    def get_records(self):
        if self.records is None:
            try:
                self.records = self.get_assets(self.user['email'])
            except:
                return []

        return list(filter(lambda record: self.check(record), self.records))

    def get_single_file(self, description):
        return list(filter(lambda record : record['data']['form']['description'] == description, self.records))[0]['data']['file']

    def get_assets(self, query):
        asset = bdb.assets.get(search=query)
        return asset

    def get_single_asset(self, id):
        asset = bdb.transactions.get(asset_id=id, operation='CREATE')
        return asset

    def get_metadata(self, meta):
        metadata = bdb.metadata.get(meta)
        return metadata


    def get_transactions(self, id):
        transactions = bdb.transactions.get(asset_id=id)
        return transactions

    def write_record(self, ipfs_hash, form):
        print(self.bigchain_keys['public_key'])
        id = uuid.uuid4()
        data = {
            'schema': 'record',
            'form': form,
            'user': self.user,
            'file': ipfs_hash,
            'file_hash': hash(ipfs_hash),
            'id' : str(id),
            'date': datetime.now().strftime("%s")
        }
        metadata = {
            'doclist': [],
            'id': str(id),
            'date': datetime.now().strftime("%s")
        }
        
        tx = bdb.transactions.prepare(
            operation='CREATE',
            signers=self.bigchain_keys['public_key'],
            asset={'data': data},
            metadata=metadata
        )
        signed_tx = bdb.transactions.fulfill(
            tx,
            private_keys=self.bigchain_keys['private_key']
        )
        sent = bdb.transactions.send_commit(signed_tx)
        return sent 

    def get_transfer_details(self, tx):
        output = tx['outputs'][0]
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
        return transfer_asset, transfer_input

    def get_doctor_key(self, dname):
        asset = self.get_assets(dname)
        rsa_key = list(filter(lambda record : check(record), asset))[0]
        return rsa_key

    def get_meta_details(self, tx, doclist):
        metadata = tx['metadata']
        doc = metadata['doclist']
        for doctor in doclist:
            key = RSA.importKey(self.get_doctor_key(doctor))
            doc.append({
                'email': doctor,
                'key': encrypt_rsa(self.secret_key.encode(), key).decode()
            })
        metadata['doclist'] = doc
        metadata['date'] = datetime.now().strftime("%s")
        return metadata

    def transfer_record(self, asset=None, doclist=[]):
        asset = self.get_assets(asset)
        tx = self.get_transactions(asset[0]['id'])[-1]
        transfer_asset, transfer_input = self.get_transfer_details(tx)
        
        metadata = self.get_meta_details(tx, doclist)
        prepared_tx = bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=self.bigchain_keys['public_key'],
            metadata=metadata
        )

        signed = bdb.transactions.fulfill(
            prepared_tx,
            private_keys=self.bigchain_keys['private_key']
        )
    
        tx = bdb.transactions.send_commit(signed)
        return tx

if __name__ =='__main__':
    vault = Vault(config)
    vault.setup()
    user = User('pratik', 'doctor', '12345678')

    # print(user.write_record("sadaedeafefef", {"description": "get allah....lamo"}))
    # transfer = user.transfer_record(asset="get allah....lamo", doclist=['ajacku'])
    # print(transfer)
    # asset = user.get_assets("get allah....lamo")
    # tx = user.get_transactions(id=asset[0]['id'])
    # print(tx[-1])
    #print(user.get_single_asset(id='d7ac1bb86f149f48b8b291f822867d55423a3e1204a1b2ccf8fd9c6389c53484'))
    # print(user.get_transactions(id='ca9b52f9f80ef3e2371be172be43f95655d150a93b576cbc5ff09f3a74674b9a'))
    #print(user.get_single_file('abdullahhh'))

    
    
    

    
   

   