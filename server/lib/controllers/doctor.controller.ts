import { getDoctorFiles } from '../utils/ehr';
import { bigchainService, cryptoService } from '../services';
import { Request, Response } from 'express';

export const getFiles = async (req: Request, res: Response) => {
   try {
      let data = await getDoctorFiles(req.session?.user.user.username, req.session?.user.secrets.RSAPrivateKey);
      return res.render('doctor/assets.ejs', {
         records: data,
         name: req.session?.user.user.name
      });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const getDetails = async (req: Request, res: Response) => {
   try {
      console.log(req.session);
      return res.render('doctor/profile.ejs', { record: req.session?.user.user, name: req.session?.user.user.name });
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const getPrescription = async (req: Request, res: Response) => {
   const files = req.body.value;
   console.log(JSON.parse(files));
   res.render('doctor/prescribe.ejs', {
      records: JSON.parse(files),
      name: req.session?.user.user.name
   });
};

export const postPrescription = async (req: Request, res: Response) => {
   const { id, description, pkey, prescription } = req.body;
   const code = cryptoService.generateCode();
   let data = {
      username: req.session?.user.user.username,
      assetID: id,
      description: description,
      prescription: prescription,
      id: code,
      schema: 'record'
   };
   let metadata = {
      email: req.session?.user.user.email,
      datetime: new Date().toString(),
      id: code
   };
   try {
      let tx = await bigchainService.createAsset(data, metadata, pkey, req.session?.user.secrets.bigchainPrivateKey);
      console.log('Transction id :', tx.id);
      return res.redirect('/doctor/home');
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};
