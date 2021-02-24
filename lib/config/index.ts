const dotenv = require('dotenv');

dotenv.config();

export const PORT: number = Number(process.env.PORT || 5000);
export const MONGO_URL: string = String(process.env.MONGO_URL || 'mongodb://localhost:27017/');
export const RASA_URL: string = String(process.env.RASA_URL || 'http://localhost:5005');
