import {
   createRecord,
   getAssetHistory,
   showAccess,
   showRevoke,
   createAccess,
   revokeAccess,
   getPrescription
} from '../utils/ehr.js';
import { bigchainService } from '../services';
import type { Request, Response } from 'express';
import UserModel from '../models/user.models';

export const getDoctorList = async (_req: Request, res: Response) => {
   try {
      let result = await bigchainService.getAsset('Doctor');
      result = result.map((data: { [x: string]: unknown }) => data['data']);
      console.log(result);
      return res.render('patientaccdoclist.ejs', { docs: result });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const getMedicalHistory = async (req: Request, res: Response) => {
   try {
      let records = req.session?.user.records;
      if (records.length === 0 && req.session) {
         const user = req.session.user as UserModel;
         user.getRecords(req.session.user.user.username);
         records = req.session?.user.records;
      }
      return res.render('patientmedhistory.ejs', { doc: records });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const postAccess = async (req: Request, res: Response) => {
   req.session!.demail = req.body.value;
   try {
      let data = await showAccess(req.session?.demail, req.session?.user.records);
      return res.render('patientaccesstrans.ejs', { doc: data });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const postRevoke = async (req: Request, res: Response) => {
   req.session!.demail = req.body.value;
   try {
      let data = await showRevoke(req.session?.demail, req.session?.user.records);
      // console.log("revoke data is....", data)
      return res.render('patientrevoketrans.ejs', { doc: data });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const check = async (req: Request, res: Response) => {
   const data: any[] = [];
   for (const item of req.body) if (item != null) data.push(item);

   try {
      await createAccess(
         data,
         req.session?.user.bigchainKeys.publicKey,
         req.session?.user.bigchainKeys.privateKey,
         req.session?.demail,
         req.session?.user.secretKey
      );
      return res.redirect('/user/home');
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const uncheck = async (req: Request, res: Response) => {
   let count = Object.keys(req.body).length;
   console.log(req.body);
   console.log('Objects checked is: ', count);
   let data: any = [];
   for (let i = 0; i < count; i++) {
      if (req.body[i] == undefined) {
         count++;
      } else {
         data.push(req.body[i]);
      }
   }
   console.log(data);
   try {
      await revokeAccess(
         data,
         req.session?.user.bigchainKeys.publicKey,
         req.session?.user.bigchainKeys.privateKey,
         req.session?.demail
      );
      return res.redirect('/user/home');
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const prescription = async (req: Request, res: Response) => {
   let demail = req.body.demail;
   try {
      let data = await getPrescription(req.session?.user.email, demail);
      return res.render('patientpresc.ejs', { doc: data });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const assetHistory = async (req: Request, res: Response) => {
   let assetid = req.body.history;
   try {
      let data = getAssetHistory(assetid);
      console.log(data);
      return res.render('patientassethistory.ejs', { doc: data });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const addRecord = async (req: Request, res: Response) => {
   if (req.files.length < 1) {
      return res.sendStatus(404).json({ status: 'File not uploaded' });
   }
   let fields = req.body;
   let fileBuffer = req.files[0].buffer;

   let data = {
      height: fields.height,
      weight: fields.weight,
      symptoms: fields.symptoms,
      allergies: fields.allergies,
      smoking: fields.smoking,
      exercise: fields.exercise,
      description: fields.d,
      schema: 'record'
   };
   try {
      let tx = await createRecord(
         data,
         req.session?.user.user.email,
         fileBuffer,
         req.session?.user.secrets.bigchainPublicKey,
         req.session?.user.secrets.bigchainPrivateKey,
         req.session?.user.secrets.secretKey
      );
      console.log('Transaction', tx.id, 'successfully posted.');
      return res.redirect('/user/medicalhistory');
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};
