import { Router, Request, Response } from 'express';
import { userController } from '../controllers';
import { fileUpload } from '../middleware/file-upload';

const userRouter: Router = Router();

userRouter.get('/doctorlist', userController.getDoctorList);

userRouter.get('/medicalhistory', userController.getMedicalHistory);

// userRouter.post('/access', userController.postAccess);
// userRouter.post('/revoke', userController.postRevoke);

userRouter.get('/home', function (req: Request, res: Response) {
   res.render('patient/profile.ejs', { data: req.session?.user.user });
});

userRouter.get('/add', function (_req: Request, res: Response) {
   res.render('patient/addrecord.ejs');
});

userRouter.post('/check', userController.check);

userRouter.post('/uncheck', userController.uncheck);

userRouter.post('/prescription', userController.prescription);

userRouter.post('/assethistory', userController.assetHistory);

userRouter.post('/add', fileUpload.any(), userController.addRecord);

export default userRouter;
