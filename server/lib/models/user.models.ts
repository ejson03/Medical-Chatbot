import { cryptoService, bigchainService, vaultService } from '../services';

export interface UserInterface {
   email: string;
   name: string;
   schema: string;
   gender: string;
   institute?: string;
   qualification?: string;
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
   public user!: UserInterface;
   public secrets!: SecretInterface;

   constructor(user: UserInterface, password?: string) {
      if (password) {
         this.getBio(user.name, user.schema, password).then(user => {
            this.user = user;
            console.log('User is ', this.user);
         });

         if (!this.registered) {
            this.createUser(user, password).then(user => {
               this.user = user;
               this.registered = true;
               console.log('User created is ', this.user);
            });
         }
      } else {
      }

      if (this.records.length === 0 && this.registered) {
         this.getRecords(user.name).then(record => {
            this.records = record;
            console.log('Records', this.records);
         });
      }
   }

   async getBio(username: string, schema: string, password: string) {
      try {
         let records = await bigchainService.getAsset(username);
         records = records.filter(function (data: any | UserInterface) {
            return data.schema == schema;
         });
         this.registered = true;
         await vaultService.login(password, username);
         await this.readKeys();
         return records[0]['data'];
      } catch {
         this.registered = false;
      }
      return null;
   }

   writeKeys(username: string) {
      try {
         this.secrets.secretKey = cryptoService.createSecretKey();
         const bigchainKeys = bigchainService.createBigchainKeys(
            cryptoService.encrypt(username, this.secrets.secretKey)
         );
         this.secrets.bigchainPrivateKey = bigchainKeys.privateKey;
         this.secrets.bigchainPublicKey = bigchainKeys.publicKey;
         const { privateKey, publicKey } = cryptoService.generateRSAKeys();
         this.secrets.RSAPrivateKey = privateKey;
         this.secrets.RSAPublicKey = publicKey;
         Object.keys(this.secrets).forEach(([key, value]) => {
            vaultService.write(key, value);
         });
      } catch (error) {
         console.log(error);
      }
   }

   async readKeys() {
      this.secrets.bigchainPrivateKey = await vaultService.read('bigchainPrivateKey');
      this.secrets.bigchainPublicKey = await vaultService.read('bigchainPublicKey');
      this.secrets.RSAPrivateKey = await vaultService.read('rsaPrivateKey');
      this.secrets.RSAPublicKey = await vaultService.read('rsaPublicKey');
      this.secrets.secretKey = await vaultService.read('secretKey');
   }

   async createUser(asset: UserInterface, password: string) {
      try {
         await vaultService.signUp(password, asset.name);
         this.writeKeys(asset.name);
         asset.bigchainKey = this.secrets.bigchainPublicKey.toString();
         asset.RSAKey = this.secrets.RSAPublicKey.toString();
         asset.date = new Date().toString();
         let tx = await bigchainService.createAsset(
            asset,
            null,
            this.secrets.bigchainPublicKey,
            this.secrets.bigchainPrivateKey
         );
         return tx.asset.data;
      } catch (error) {
         console.log('Error is', error);
         return false;
      }
   }

   async getRecords(username: string) {
      try {
         let records = await bigchainService.getAsset(username);
         records = records.filter(
            (record: any) => record.data.schema == 'record' && record.data.user.bigchainKey == this.user.bigchainKey
         );
         return records;
      } catch (err) {
         console.log(err);
      }
      return [];
   }
}
