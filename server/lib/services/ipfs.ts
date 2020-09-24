import * as config from '../config';
import { Duplex } from 'stream';

const ipfsAPI = require('ipfs-api');
const ipfs = ipfsAPI(config.IPFS.url, config.IPFS.port, { protocol: 'https' });

export const Download = (res: any, buffer: any) => {
   function BufferToStream(buffer: any) {
      const stream = new Duplex();
      stream.push(buffer);
      stream.push(null);
      return stream;
   }
   return new Promise((resolve, reject) => {
      return BufferToStream(buffer)
         .pipe(res)
         .on('error', (error: any) => {
            reject(error);
         })
         .on('finish', function () {
            resolve();
         })
         .on('end', function () {
            resolve();
         });
   });
};

export const GetFile = async (ipfsName: any) => {
   const files = await ipfs.files.get(ipfsName);
   return files[0].content;
};

export const AddFile = async (fileBuffer: any) => {
   return (await ipfs.files.add(fileBuffer))[0]['hash'];
};
