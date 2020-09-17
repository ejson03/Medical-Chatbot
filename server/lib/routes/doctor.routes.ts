import { Router } from 'express';
import { doctorController } from '../controllers';

const doctorRouter: Router = Router();

doctorRouter.get('/list', doctorController.getFiles);

doctorRouter.get('/home', doctorController.getDetails);

doctorRouter.post('/prescribe', doctorController.getPrescription);

doctorRouter.post('/prescription', doctorController.postPrescription);

export default doctorRouter;
