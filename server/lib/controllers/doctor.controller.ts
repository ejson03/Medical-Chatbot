import { getDoctorFiles } from '../utils/ehr';
import { bigchainService, cryptoService } from '../services';
import { Request, Response } from 'express';

export const getFiles = async (req: Request, res: Response) => {
   try {
      let data = await getDoctorFiles(req.session?.email);
      console.log(data);
      return res.render('doctorasset.ejs', { records: data });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const getDetails = async (req: Request, res: Response) => {
   try {
      return res.render('docprofile.ejs', { record: req.session?.user.user });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const getPrescription = async (req: Request, res: Response) => {
   let id = req.body.id;
   let description = req.body.description;
   let pkey = req.body.pkey;
   console.log(pkey);
   res.render('docprescribe.ejs', {
      id: id,
      description: description,
      pkey: pkey
   });
};

export const postPrescription = async (req: Request, res: Response) => {
   let assetID = req.body.id;
   let description = req.body.description;
   let pkey = req.body.pkey;
   let prescription = req.body.prescription;
   let id = cryptoService.generateCode();
   let data = {
      email: req.session?.email,
      assetID: assetID,
      description: description,
      prescription: prescription,
      id: id
   };
   let metadata = {
      email: req.session?.email,
      datetime: new Date().toString(),
      id: id
   };
   try {
      let tx = await bigchainService.createAsset(data, metadata, pkey, req.session?.key.privateKey);
      console.log('Transction id :', tx.id);
      return res.redirect('/doctor/home');
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};
