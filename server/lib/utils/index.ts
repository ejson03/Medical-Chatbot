import { Request } from 'express';

export async function SessionSave(req: Request) {
   return await new Promise((resolve, reject) => {
      req.session?.save(err => {
         if (err == null) resolve();
         else reject(err);
      });
   });
}

export async function SessionDestroy(req: Request) {
    return await new Promise((resolve, reject) => {
       req.session?.destroy(err => {
          if (err == null) resolve();
          else reject(err);
       });
    });
 }
 