import { Request, Response } from 'express';
import { rasaService } from '../services';

export const rasa = async (req: Request, res: Response) => {
   try {
      const sender = 'vortex';
      const message = req.body.message;
      const rasa = await rasaService.RASARequest(message, sender);
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
      if (data.length != 0) {
         return res.render('history.ejs', {
            doc: data,
            name: 'vortex'
         });
      } else {
         return res.render('history.ejs', {
            doc: [],
            name: 'vortex'
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
