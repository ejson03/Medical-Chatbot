import multer from 'multer';
// import uuid from 'uuid';

const MIME_TYPE_MAP = {
   'image/png': 'png',
   'image/jpeg': 'jpeg',
   'image/jpg': 'jpg',
   'application/pdf': 'pdf',
   'application/zip': 'zip',
   'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
   'application/msword': 'doc'
};

export const fileUpload = multer({
   limits: { fileSize: 20 * 1000 * 1000 },
   storage: multer.memoryStorage(), //multer.diskStorage({
   //    destination: (_req: any, _file: any, cb: any) => {
   //       cb(null, 'uploads/images');
   //    },
   //    filename: (_req: any, file: any, cb: any) => {
   //       const ext = MIME_TYPE_MAP[file.mimetype];
   //       cb(null, uuid + '.' + ext);
   //    }
   // }),
   fileFilter: (_req: any, file: any, cb: any) => {
      const isValid = !!MIME_TYPE_MAP[file.mimetype];
      let error = isValid ? null : new Error('Invalid mime type!');
      cb(error, isValid);
   }
});
