import { Router, Request, Response } from 'express';
import { userController } from '../controllers';

const userRouter: Router = Router();

userRouter.get('/doctorlist', userController.getDoctorList);

userRouter.get('/medicalhistory', userController.getMedicalHistory);

userRouter.post('/access', userController.postAccess);
userRouter.post('/revoke', userController.postRevoke);

userRouter.get('/home', function (_req: Request, res: Response) {
   res.render('patientaddrec.ejs');
});

userRouter.post('/check', userController.check);

userRouter.post('/uncheck', userController.uncheck);

userRouter.post('/prescription', userController.prescription);

userRouter.post('/assethistory', userController.assetHistory);

// userRouter.post('/add', userController.addRecord);

export default userRouter;
