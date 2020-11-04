import { createRecord } from '../utils/ehr.js';
import { vaultService } from '../services';
import type { Request, Response } from 'express';
import UserModel, { RecordInterface } from '../models/user.models';
import { filterRecords } from '../utils/filteration.js';

export const getFilteredRecords = async (req: Request, res: Response) => {
   const { username } = req.body;
   const query = req.body as Partial<RecordInterface>;
   console.log(username, query)
   const user = new UserModel();
   const records = await user.getRecords(username);
   const filtered = filterRecords(records, query);
   return res.json(filtered);
};

export const getAll = async (req: Request, res: Response) => {
   const { username } = req.body;
   const user = new UserModel();
   const records = await user.getRecords(username);
   return res.json(records);
};

export const addRecord = async (req: Request, res: Response) => {
   const token = req.body.token;
   const asset = req.body.asset;
   const clientVault = await vaultService.vaultFromToken(token);
   const bigchainPrivateKey = await vaultService.read(clientVault, 'bigchainPrivateKey');
   const bigchainPublicKey = await vaultService.read(clientVault, 'bigchainPublicKey');
   const secretKey = await vaultService.read(clientVault, 'secretKey');
   try {
      const tx = await createRecord(
         asset,
         asset.username,
         asset.file,
         bigchainPublicKey,
         bigchainPrivateKey,
         secretKey,
         'rasa'
      );
      return res.json(tx.id);
   } catch (err) {
      console.error(err);
      return res.json('error');
   }
};
