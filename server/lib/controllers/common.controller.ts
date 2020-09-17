import { Request, Response } from 'express';
import { ipfsService, rasaService, cryptoService, vaultService } from '../services';
import UserModel, { UserInterface } from '../models/user.models';

export const signUp = async (req: Request, res: Response) => {
   const users = await vaultService.getUsers();
   if (users.includes(req.body.username)) {
      return res.json({ success: false });
   } else {
      try {
         const asset: UserInterface = req.body as UserInterface;
         new UserModel(asset, req.body.password);
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
   if (req.body.schema == 'Patient') {
      return res.redirect('/user/home');
   } else {
      return res.redirect('/doctor/home');
   }
};

export const view = async (req: Request, res: Response) => {
   try {
      const status = String(req.body.url);
      let url1 = '';
      if (status === 'encrypted') {
         url1 = cryptoService.decrypt(req.body.b);
      } else {
         url1 = req.body.b;
      }

      let buffer = await ipfsService.GetFile(url1);
      buffer = cryptoService.decryptFile(buffer.toString('utf-8'), req.session?.user.secretKey);
      buffer = new Buffer(buffer, 'binary');
      await ipfsService.Download(res, buffer);
      return url1;
   } catch (err) {
      console.error(err);
      return res.sendStatus(404);
   }
};

export const rasa = async (req: Request, res: Response) => {
   try {
      const message = req.body.message;
      const sender = String(req.session?.name);
      const rasa = await rasaService.RASARequest(message, sender);
      return res.json(rasa);
   } catch (err) {
      console.error('Error: ', err);
      return res.status(500);
   }
};

export const rasaHistory = async (req: Request, res: Response) => {
   let email = req.body.rasa;
   try {
      let data = await rasaService.getRasaHistory(email);
      console.log(data);
      return res.render('patientrasahistory.ejs', {
         doc: data,
         email: req.session?.email
      });
   } catch (err) {
      console.error('Error: ', err);
      return res.status(500);
   }
};
