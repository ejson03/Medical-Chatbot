const driver = require('bigchaindb-driver');
import bdb from 'easy-bigchain';

import { BIGCHAIN_URL } from '../config';

const conn = new driver.Connection(BIGCHAIN_URL);

export const createBigchainKeys = (email: string) => {
   return bdb.generateKeypair(email);
};

export const createAsset = async (asset: any, metadata: any, publicKey: string, privateKey: string) => {
   const txCreateAliceSimple = driver.Transaction.makeCreateTransaction(
      asset,
      metadata,
      [driver.Transaction.makeOutput(driver.Transaction.makeEd25519Condition(publicKey))],
      publicKey
   );

   const txCreateAliceSimpleSigned = driver.Transaction.signTransaction(txCreateAliceSimple, privateKey);
   const tx = await conn.postTransactionCommit(txCreateAliceSimpleSigned);
   return tx;
};

export const transferAsset = async (transaction: any, metadata: any, publicKey: string, privateKey: string) => {
   let txTransferBob = driver.Transaction.makeTransferTransaction(
      [{ tx: transaction, output_index: 0 }],
      [driver.Transaction.makeOutput(driver.Transaction.makeEd25519Condition(publicKey))],
      metadata
   );
   const txTransferBobSigned = driver.Transaction.signTransaction(txTransferBob, privateKey);
   const transfer = await conn.postTransactionCommit(txTransferBobSigned);
   return transfer;
};

export const getAsset = async (query: any) => {
   return await conn.searchAssets(query);
};

export const getMetadata = async (query: any) => {
   return await conn.searchMetadata(query);
};

export const getTransaction = async (query: any) => {
   return await conn.getTransaction(query);
};

export const listTransactions = async (query: any | string) => {
   return await conn.listTransactions(query);
};
