import { Router, Request, Response } from 'express';
import { doctorController } from '../controllers';
import { fileUpload } from '../middleware/file-upload';
import { GOOGLE_MAPS_KEY } from '../config';

const doctorRouter: Router = Router();

doctorRouter.get('/list', doctorController.getFiles);

doctorRouter.get('/home', doctorController.getDetails);

doctorRouter.post('/prescribe', doctorController.getPrescription);

doctorRouter.post('/prescription', fileUpload.any(), doctorController.postPrescription);

doctorRouter.get('/profileupdate', function (req: Request, res: Response) {
   res.render('doctor/profileupdate.ejs', { data: req.session?.user.user, name: req.session?.user.user.name });
});

doctorRouter.get('/chatbot', function (req: Request, res: Response) {
   res.render('doctor/chatbot.ejs', { name: req.session?.user.user.name, map: GOOGLE_MAPS_KEY });
});

export default doctorRouter;
