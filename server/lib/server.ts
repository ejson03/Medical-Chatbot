import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import router from './routes';

import * as config from './config';

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());

app.use('/api', router);

app.listen(config.PORT, function () {
   console.log(`App listening on port ${config.PORT}`);
});
