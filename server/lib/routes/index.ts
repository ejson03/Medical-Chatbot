import { Router } from 'express';
import doctorRouter from './doctor.routes';
import userRouter from './user.routes';
import commonRouter from './common.routes';
import chatbotRouter from './chatbot.routes';

const router: Router = Router();

router.get('/status', (_req, res) => {
   res.json({ status: 'OK' });
});

router.use('/', commonRouter);
router.use('/user', userRouter);
router.use('/doctor', doctorRouter);
router.use('/chatbot', chatbotRouter);

export default router;
