import { Router, Request, Response } from 'express';
import { userController } from '../controllers';
import { fileUpload } from '../middleware/file-upload';
import { GOOGLE_MAPS_KEY } from '../config';

const userRouter: Router = Router();

userRouter.get('/doctorlist', userController.getDoctorList);

userRouter.get('/medicalhistory', userController.getMedicalHistory);

userRouter.post('/access', userController.postAccess);
userRouter.post('/revoke', userController.postRevoke);

userRouter.get('/home', function (req: Request, res: Response) {
   console.log('Home session is ', req.session);
   res.render('patient/profile.ejs', { data: req.session?.user.user, name: req.session?.user.user.name });
});

userRouter.get('/profileupdate', function (req: Request, res: Response) {
   res.render('patient/profileupdate.ejs', { data: req.session?.user.user, name: req.session?.user.user.name });
});

userRouter.get('/chatbot', function (req: Request, res: Response) {
   res.render('patient/chatbot.ejs', { name: req.session?.user.user.name, map: GOOGLE_MAPS_KEY });
});

userRouter.get('/add', function (req: Request, res: Response) {
   res.render('patient/addrecord.ejs', { name: req.session?.user.user.name });
});

userRouter.post('/check', userController.check);

userRouter.post('/uncheck', userController.uncheck);

userRouter.post('/prescription', userController.prescription);

userRouter.post('/assethistory', userController.assetHistory);

userRouter.post('/add', fileUpload.any(), userController.addRecord);

export default userRouter;
