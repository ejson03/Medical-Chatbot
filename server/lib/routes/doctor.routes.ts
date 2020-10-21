import { Router, Request, Response } from 'express';
import { doctorController } from '../controllers';
import { fileUpload } from '../middleware/file-upload';

const doctorRouter: Router = Router();

doctorRouter.get('/list', doctorController.getFiles);

doctorRouter.get('/home', doctorController.getDetails);

doctorRouter.post('/prescribe', fileUpload.any(), doctorController.getPrescription);

doctorRouter.post('/prescription', doctorController.postPrescription);

doctorRouter.get('/profileupdate', function (req: Request, res: Response) {
   res.render('doctor/profileupdate.ejs', { data: req.session?.user.user, name: req.session?.user.user.name });
});

doctorRouter.get('/chatbot', function (req: Request, res: Response) {
   res.render('chatbot.ejs', { name: req.session?.user.user.name });
});

export default doctorRouter;
