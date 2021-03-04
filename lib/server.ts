import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import router from './routes';
import * as config from './config';

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());

app.use(express.static('./public'));
app.set('views', './views');
app.set('view engine', 'ejs');
app.engine('.html', require('ejs').renderFile);

app.use('/', router);

app.listen(config.PORT, function () {
   console.log(`App listening on port ${config.PORT}`);
});
