import os


BIGCHAINDB_URL= os.environ.get("BIGCHAINDB_URL")
VAULT_URL = os.environ.get("VAULT_URL")
VAULT_TOKEN = os.environ.get("VAULT_DEV_ROOT_TOKEN_ID")
IPFS_URL = os.environ.get("IPFS_URL", '/dns/ipfs.infura.io/tcp/5001/https')
MONGODB_STRING = os.environ.get("MONGODB_STRING")
WEATHER_KEY= os.environ.get("WEATHER_KEY")
WEATHER_ID= os.environ.get("WEATHER_ID")