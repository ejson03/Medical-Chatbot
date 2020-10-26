import uuid, os, json, requests
from bigchaindb_driver import BigchainDB
from datetime import datetime
from .encryption import *
from .vault import Vault
from .config import *

bdb = BigchainDB(BIGCHAINDB_URL)

def read_keys(token):
    secrets = {}
    vault = Vault(token)
    for key in ['bigchainPrivateKey', 'bigchainPublicKey', 'RSAPrivateKey', 'RSAPublicKey', 'secretKey']:
        secrets[key] = vault.read(key)
    return secrets

def get_records(query):
    try:
        records = bdb.assets.get(search=query)
        records = list(filter(lambda record : record['data']['schema'] == 'record', records))
        return records
    except:
        return []

def write_record(data, token):
    secrets = read_keys(token)
    id = uuid.uuid4()
    data['file'] = encrypt(data['file'], secrets.secretKey)
    data.update({
        'schema': 'record',
        'fileHash': hash(data['file']),
        'id' : str(id),
        'date': datetime.now().strftime("%s")
    })

    metadata = {
        'doclist': [],
        'id': str(id),
        'date': datetime.now().strftime("%s")
    }
        
    tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=secrets.bigchainPublicKey,
        asset={'data': data},
        metadata=metadata
    )
    signed_tx = bdb.transactions.fulfill(
        tx,
        private_keys=secrets.bigchainPrivateKey
    )
    transaction = bdb.transactions.send_commit(signed_tx)
    return transaction.id


    
    
    

    
   

   