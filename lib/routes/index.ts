import { Router } from 'express';
import commonRouter from './common.routes';

const router: Router = Router();

router.get('/status', (_req, res) => {
   res.json({ status: 'OK' });
});

router.use('/', commonRouter);

export default router;
