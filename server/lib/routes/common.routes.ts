import { Router } from 'express';
import type { Request, Response } from 'express';
import { commonController } from '../controllers';

const commonRouter: Router = Router();

commonRouter.get('/', function (_req: Request, res: Response) {
   return res.render('index.html');
});

commonRouter.get('/login', function (_req: Request, res: Response) {
   return res.render('login.html');
});
commonRouter.get('/signup', function (_req: Request, res: Response) {
   return res.render('signup.html');
});

commonRouter.post('/signup', commonController.signUp);
commonRouter.post('/login', commonController.login);
// commonRouter.post("/otp", commonController.getOTP);

commonRouter.post('/view', commonController.view);

commonRouter.post('/rasa', commonController.rasa);

commonRouter.post('/logout', function (req: Request, res: Response) {
   req.session?.destroy(err => console.log(err));
   res.render('index.html');
});

export default commonRouter;
