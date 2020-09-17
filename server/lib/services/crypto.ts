import crypto from 'crypto';

export const createSecretKey = () => {
   return crypto.randomBytes(32).toString('hex').slice(0, 32);
};

export const generateIV = () => {
   return crypto.randomBytes(16).toString('hex').slice(0, 16);
};

export const encrypt = (text: any, key = 'd6F3Efeq') => {
   let cipher = crypto.createCipher('aes-256-cbc', key);
   let crypted = cipher.update(text, 'utf8', 'hex');
   crypted += cipher.final('hex');
   return crypted;
};

export const decrypt = (text = '', key = 'd6F3Efeq') => {
   let decipher = crypto.createDecipher('aes-256-cbc', key);
   let dec = decipher.update(text, 'hex', 'utf8');
   dec += decipher.final('utf8');
   return dec;
};

export const decryptFile = (text: string, key = 'd6F3Efeq') => {
   let decipher = crypto.createDecipher('aes-256-cbc', key);
   let dec = decipher.update(text, 'hex', 'binary');
   dec += decipher.final('binary');
   return dec;
};

export const hash = (text: string) => {
   return crypto.createHash('sha1').update(JSON.stringify(text)).digest('hex');
};

export const generateRSAKeys = () => {
   const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
      modulusLength: 4096,
      publicKeyEncoding: {
         type: 'pkcs1',
         format: 'pem'
      },
      privateKeyEncoding: {
         type: 'pkcs1',
         format: 'pem',
         cipher: 'aes-256-cbc',
         passphrase: ''
      }
   });
   return {
      privateKey: privateKey,
      publicKey: publicKey
   };
};

export const encryptRSA = (data: any, publicKey: string) => {
   const buffer = Buffer.from(data, 'utf8');
   const encrypted = crypto.publicEncrypt(publicKey, buffer);
   return encrypted.toString('base64');
};

export const decryptRSA = (data: any, privateKey: string) => {
   const buffer = Buffer.from(data, 'base64');
   const decrypted = crypto.privateDecrypt(
      {
         key: privateKey.toString(),
         passphrase: ''
      },
      buffer
   );
   return decrypted.toString('utf8');
};

export const generateCode = () => {
   let digits = '0123456789';
   let OTP = '';
   for (let i = 0; i < 4; i++) {
      OTP += digits[Math.floor(Math.random() * 10)];
   }
   return OTP;
};
