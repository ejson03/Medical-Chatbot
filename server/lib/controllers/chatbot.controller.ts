import { createRecord } from '../utils/ehr.js';
import { vaultService } from '../services';
import type { Request, Response } from 'express';
import UserModel from '../models/user.models';

export const getFilteredRecords = async (req: Request, res: Response) => {
   const { username } = req.body;
   const query = req.params;
   const user = new UserModel();
   const records = await user.getRecords(username);

   return res.json(records);
};

export const getAll = async (req: Request, res: Response) => {
   const { username } = req.body;
   console.log(username);
   const user = new UserModel();
   const records = await user.getRecords(username);
   console.log(records);
   return res.json(records);
};

export const addRecord = async (req: Request, res: Response) => {
   const { token, asset } = req.body;
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
      console.log(tx);
      return res.json(tx.id);
   } catch (err) {
      console.error(err);
      return res.json('error');
   }
};
