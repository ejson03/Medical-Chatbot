import { Router } from 'express';
import * as commonController from '../controllers';

const commonRouter: Router = Router();

commonRouter.get('/', (_req, res) => {
   res.render('chatbot.ejs');
});
commonRouter.post('/getrasahistory', commonController.rasaHistory);

commonRouter.post('/rasa', commonController.rasa);
commonRouter.post('/charts', commonController.rasaCharts);

export default commonRouter;
