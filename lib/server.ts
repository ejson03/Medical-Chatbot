import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import router from './routes';
// import { exec } from 'child_process';
import * as config from './config';
// console.log(
//    `cd ${config.actions_path} ; rasa run actions ; cd ${config.chatbot_path} ; rasa run -m models --endpoint endpoints.yml --credentials credentials.yml --enable-api --debug`
// );
// exec(
//    `cd ${config.actions_path} ; rasa run actions ; cd ${config.chatbot_path} ; rasa run -m models --endpoint endpoints.yml --credentials credentials.yml --enable-api --debug`,
//    (error, stdout, stderr) => {
//       if (error) {
//          console.log(`error: ${error.message}`);
//          return;
//       }
//       if (stderr) {
//          console.log(`stderr: ${stderr}`);
//          return;
//       }
//       console.log(`stdout: ${stdout}`);
//    }
// );

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
