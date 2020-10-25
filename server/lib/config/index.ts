import dotenv from 'dotenv';

dotenv.config();

export const PORT: number = Number(process.env.PORT || 8000);
export const SECRET: string = String(process.env.SECRET);
export const JWT_SECRET: string = String(process.env.JWT_SECRET);
export const VAULT: any = {
   url: String(process.env.VAULT_URL),
   token: String(process.env.VAULT_TOKEN)
};
export const MONGO_URL: string = String(process.env.MONGO_URL || 'mongodb://192.168.99.103:27017/');
export const RASA_URL: string = String(process.env.RASA_URL || 'http://localhost:5005');
export const BIGCHAIN_URL: string = String(process.env.BIGCHAIN_URL || 'http://192.168.99.103:9984/api/v1');
export const IPFS: any = {
   url: String(process.env.IPFS_URL || 'ipfs.infura.io'),
   port: String('5001')
};
export const GOOGLE_MAPS_KEY: string = String(process.env.GOOGLE_MAPS_KEY);
