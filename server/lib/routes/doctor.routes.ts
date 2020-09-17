import { Router } from 'express';
import { doctorController } from '../controllers';
import { fileUpload } from '../middleware/file-upload';

const doctorRouter: Router = Router();

doctorRouter.get('/list', doctorController.getFiles);

doctorRouter.get('/home', doctorController.getDetails);

doctorRouter.post('/prescribe', fileUpload.any(), doctorController.getPrescription);

doctorRouter.post('/prescription', doctorController.postPrescription);

export default doctorRouter;
