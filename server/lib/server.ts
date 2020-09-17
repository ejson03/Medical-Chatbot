import express from 'express';
import bodyParser from 'body-parser';
import session from 'express-session';
import MongoStore from 'connect-mongo';
import cors from 'cors';
import router from './routes';

import * as config from './config';

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());

const MongoStoreSession = MongoStore(session);

app.use(
   session({
      store: new MongoStoreSession({
         url: config.MONGO_URL
      }),
      secret: config.SECRET,
      resave: false,
      saveUninitialized: false,
      cookie: {
         maxAge: 1000 * 60 * 60 * 24 * 7 * 2 // two weeks
      }
   })
);
app.use(express.static('./public'));
app.set('views', './views');
app.set('view engine', 'ejs');
app.engine('.html', require('ejs').renderFile);

app.use('/', router);

app.listen(config.PORT, function () {
   console.log(`App listening on port ${config.PORT}`);
});
