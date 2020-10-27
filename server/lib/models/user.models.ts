import { cryptoService, bigchainService, vaultService } from '../services';

export interface UserInterface {
   email: string;
   name: string;
   username: string;
   schema: string;
   gender: string;
   institute?: string;
   specialization?: string;
   location?: string;
   RSAKey?: string;
   bigchainKey?: string;
   date?: string;
}

interface SecretInterface {
   bigchainPrivateKey: string;
   bigchainPublicKey: string;
   RSAPrivateKey: string;
   RSAPublicKey: string;
   secretKey: string;
}

export default class UserModel {
   public registered: boolean = false;
   public records: [] = [];
   public user = {} as UserInterface;
   public secrets = {} as SecretInterface;
   public clientToken: string = '';

   constructor(user?: UserModel) {
      if (user) {
         this.secrets = user.secrets;
         this.user = user.user;
         this.registered = user.registered;
         this.records = user.records;
      }
   }

   async getBio(username: string, schema: string) {
      try {
         const records = await bigchainService.getAsset(username);
         const filteredRecords = records.filter(record => record.data.schema == schema);
         this.registered = true;
         this.user = filteredRecords[0]['data'];
         await this.readKeys();
      } catch (error) {
         console.error(error);
         this.registered = false;
      }
   }

   async writeKeys(username: string) {
      try {
         const clientVault = await vaultService.vaultFromToken(this.clientToken);
         this.secrets!.secretKey = cryptoService.createSecretKey();
         const bigchainKeys = bigchainService.createBigchainKeys(
            cryptoService.encrypt(username, this.secrets.secretKey)
         );
         this.secrets!.bigchainPrivateKey = bigchainKeys.privateKey;
         this.secrets!.bigchainPublicKey = bigchainKeys.publicKey;
         const { privateKey, publicKey } = cryptoService.generateRSAKeys();
         this.secrets!.RSAPrivateKey = privateKey;
         this.secrets!.RSAPublicKey = publicKey;
         for (const secret in this.secrets) {
            vaultService.write(clientVault, secret, this.secrets[secret]);
         }
      } catch (error) {
         console.error(error);
      }
   }

   async readKeys() {
      const clientVault = await vaultService.vaultFromToken(this.clientToken);
      this.secrets.bigchainPrivateKey = await vaultService.read(clientVault, 'bigchainPrivateKey');
      this.secrets.bigchainPublicKey = await vaultService.read(clientVault, 'bigchainPublicKey');
      this.secrets.RSAPrivateKey = await vaultService.read(clientVault, 'RSAPrivateKey');
      this.secrets.RSAPublicKey = await vaultService.read(clientVault, 'RSAPublicKey');
      this.secrets.secretKey = await vaultService.read(clientVault, 'secretKey');
   }

   async createUser(asset: UserInterface, password: string) {
      try {
         const vault = vaultService.Vault;
         await vaultService.signUp(vault, password, asset.username);
         await this.writeKeys(asset.username);
         asset.bigchainKey = this.secrets.bigchainPublicKey.toString();
         asset.RSAKey = this.secrets.RSAPublicKey.toString();
         asset.date = new Date().toString();
         let tx = await bigchainService.createAsset(
            asset,
            null,
            this.secrets.bigchainPublicKey,
            this.secrets.bigchainPrivateKey
         );
         this.registered = true;
         this.user = tx.asset.data;
         return tx.asset.data;
      } catch (error) {
         console.error('Error is', error);
         return false;
      }
   }

   async getRecords(username: string) {
      try {
         const records = await bigchainService.getAsset(username);
         const filterRecords = records.filter(
            record => record.data.schema == 'record' && record.data.username == username
         );
         this.records = filterRecords;
         return filterRecords;
      } catch (err) {
         console.error(err);
         return [];
      }
      return [];
   }
}
