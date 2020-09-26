import { Router } from 'express';
import type { Request, Response } from 'express';
import { commonController } from '../controllers';
import { fileUpload } from '../middleware/file-upload';

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

commonRouter.get('/chatbot', (_req, res) => {
   res.render('chatbot.ejs');
});

commonRouter.post('/signup', commonController.signUp);
commonRouter.post('/login', commonController.login);

commonRouter.post('/view', commonController.view);

commonRouter.post('/rasa', fileUpload.single('file'), commonController.rasa);

commonRouter.post('/logout', function (req: Request, res: Response) {
   req.session?.destroy(err => console.log(err));
   res.render('index.html');
});

export default commonRouter;
