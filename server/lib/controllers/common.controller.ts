import { Request, Response } from 'express';
import { ipfsService, rasaService, cryptoService, vaultService } from '../services';
import UserModel, { UserInterface } from '../models/user.models';
import { createIPFSHashFromFileBuffer } from '../utils/ehr';

const doctorExclude = ['pass', 're_pass', 'signup'];
const patientExclude = [...doctorExclude, 'location', 'institute', 'specialization'];

export const signUp = async (req: Request, res: Response) => {
   const users = await vaultService.getUsers();
   if (users.includes(req.body.username)) {
      return res.status(401).json({ success: false });
   } else {
      try {
         const password = req.body.pass;
         req.session!.password = password;
         const asset: UserInterface = req.body as UserInterface;
         if (req.body.institute === '') {
            patientExclude.forEach(key => {
               delete asset[key];
            });
         } else {
            doctorExclude.forEach(key => {
               delete asset[key];
            });
         }
         const user = new UserModel();
         await user.createUser(asset, password);
         req.session!.user = user;
         console.log(req.session);
         if (asset.schema == 'Patient') {
            return res.redirect('/user/home');
         } else {
            res.redirect('/doctor/home');
         }
      } catch (error) {
         console.log(error);
         return res.sendStatus(404);
      }
   }
   return null;
};

export const login = async (req: Request, res: Response) => {
   const users = await vaultService.getUsers();
   if (users.includes(req.body.username)) {
      const status = await vaultService.login(req.body.pass, req.body.username);
      if (status) {
         req.session!.pass = req.body.pass;
         const user = new UserModel();
         await user.getBio(req.body.username, req.body.schema);
         await user.getRecords(req.body.username);
         req.session!.user = user;
         console.log(req.session);
         if (req.body.schema == 'Patient') {
            return res.redirect('/user/home');
         } else {
            return res.redirect('/doctor/home');
         }
      } else {
         return res.status(401).json({ success: 'Password is incorrect' });
      }
   } else {
      return res.status(401).json({ success: 'User does not exist' });
   }
};

export const view = async (req: Request, res: Response) => {
   try {
      const status = String(req.body.status);
      let fileURL = String(req.body.fileURL);
      if (status === 'encrypted') {
         fileURL = cryptoService.decrypt(fileURL, req.session?.user.secrets.secretKey);
      }
      console.log(fileURL);
      let buffer = await ipfsService.GetFile(fileURL);
      buffer = cryptoService.decryptFile(buffer.toString('utf-8'), req.session?.user.secrets.secretKey);
      buffer = new Buffer(buffer, 'binary');
      await ipfsService.Download(res, buffer);
      return fileURL;
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const rasa = async (req: Request, res: Response) => {
   try {
      const sender = String(req.session?.user.user.username) || 'vortex';
      let message: any;
      let rasa: any;
      if (req.file) {
         message = await createIPFSHashFromFileBuffer(req.file.buffer, 'edededwe'); //req.user.secretKey
         rasa = await rasaService.RASARequest(message, sender, 'edededwe'); //req.session?.user.secrets.secretKey);
      } else {
         message = req.body.message;
         rasa = await rasaService.RASARequest(message, sender);
      }
      return res.status(200).json(rasa);
   } catch (err) {
      console.error('Error: ', err);
      return res.status(500);
   }
};

export const rasaHistory = async (req: Request, res: Response) => {
   const username = req.body.rasa;
   try {
      let data = await rasaService.getRasaHistory(username);
      console.log(data);
      return res.render('doctor/history.ejs', {
         doc: data,
         name: req.session?.user.user.name
      });
   } catch (err) {
      console.error('Error: ', err);
      return res.status(500);
   }
};
