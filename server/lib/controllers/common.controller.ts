import { Request, Response } from 'express';
import { ipfsService, rasaService, cryptoService, vaultService } from '../services';
import UserModel, { UserInterface } from '../models/user.models';
import { createIPFSHashFromFileBuffer } from '../utils/ehr';
import { SessionDestroy, SessionSave } from '../utils';

const doctorExclude = ['pass', 're_pass', 'signup'];
const patientExclude = [...doctorExclude, 'location', 'institute', 'specialization'];

export const signUp = async (req: Request, res: Response) => {
   const vault = vaultService.Vault;
   const users = await vaultService.getUsers(vault);
   console.log(users, req.body.username, users.includes(req.body.username));

   if (users.includes(req.body.username) || !req.body.username) {
      return res.status(401).json({ success: false });
   } else {
      try {
         const password = req.body.pass;
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
         if (user.user) {
            return res.redirect('/login');
         } else {
            await SessionDestroy(req);
            return res.sendStatus(404);
         }
      } catch (error) {
         console.error(error);
         return res.sendStatus(404);
      }
   }
   return null;
};

export const login = async (req: Request, res: Response) => {
   const vault = vaultService.Vault;
   const users = await vaultService.getUsers(vault);
   if (users.includes(req.body.username)) {
      const status = await vaultService.login(vault, req.body.pass, req.body.username);
      if (status) {
         const vaultClientToken = status.auth.client_token;
         const user = new UserModel();
         user.clientToken = vaultClientToken;
         await user.getBio(req.body.username, req.body.schema);
         await user.getRecords(req.body.username);
         req.session!.user = user;
         req.session!.client_token = vaultClientToken;
         await SessionSave(req);
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
      let decryptedBuffer;
      if (status === 'encrypted') {
         fileURL = cryptoService.decrypt(fileURL, req.session?.user.secrets.secretKey);
      }
      console.log(fileURL);
      const buffer = await ipfsService.GetFile(fileURL);
      if (req.body.hasOwnProperty('key')) {
         decryptedBuffer = cryptoService.decryptFile(buffer, req.body.key);
      } else {
         decryptedBuffer = cryptoService.decryptFile(buffer, req.session?.user.secrets.secretKey);
      }
      await ipfsService.Download(res, decryptedBuffer);
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
         message = await createIPFSHashFromFileBuffer(req.file.buffer, req.session?.user.secrets.secretKey);
         rasa = await rasaService.RASARequest(message, sender, req.session?.client_token);
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
      if (data.length != 0) {
         return res.render('doctor/history.ejs', {
            doc: data,
            name: req.session?.user.user.name
         });
      } else {
         return res.render('doctor/history.ejs', {
            doc: [],
            name: req.session?.user.user.name
         });
      }
   } catch (err) {
      console.error('Error: ', err);
      return res.status(500);
   }
};

export const rasaCharts = async (req: Request, res: Response) => {
   const username = req.body.rasa;
   try {
      const data = await rasaService.getRASACharts(username);
      return res.json({ data: data });
   } catch (err) {
      console.error('Error: ', err);
      return res.status(500);
   }
};
