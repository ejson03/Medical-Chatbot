import { cryptoService, ipfsService, bigchainService } from '../services';
import fs from 'fs';

export const getRSAKey = async (email: string, schema: string) => {
   let asset = await bigchainService.getAsset(email);
   asset.filter((data: any) => {
      return data['data']['schema'] == schema;
   });
   return asset[0]['data']['rsa_key'];
};

export const getBigchainPublicKey = async (email: string, schema: string) => {
   let asset = await bigchainService.getAsset(email);
   asset.filter((data: any) => {
      return data['data']['schema'] == schema;
   });
   return asset[0]['data']['bigchain_key'];
};

export const getEmail = async (key: any, schema: string) => {
   let asset = await bigchainService.getAsset(key);
   asset.filter((data: any) => {
      return data['data']['schema'] == schema;
   });
   return asset[0]['data']['email'];
};

export const getMultipleEmail = async (schema: string) => {
   let asset = await bigchainService.getAsset({});
   let data = asset.filter((data: any) => {
      if (data['data']['schema'] == schema) return data['email'];
   });
   return data;
};

export const createAccess = async (
   dlist: any,
   publicKey: any,
   privateKey: any,
   doctorEmail: string,
   secretKey: string
) => {
   for (const index in dlist) {
      let transaction = await bigchainService.listTransactions(dlist[index]);
      const data = {
         email: doctorEmail,
         key: cryptoService.encryptRSA(secretKey, await getRSAKey(doctorEmail, 'doctor'))
      };
      let metadata = transaction[transaction.length - 1].metadata;
      metadata['doclist'].push(data);
      metadata = JSON.stringify(metadata);
      console.log('metadata is ', metadata);

      let tx = await bigchainService.transferAsset(
         transaction[transaction.length - 1],
         metadata,
         publicKey,
         privateKey
      );
      console.log(tx.id);
   }
};

export const revokeAccess = async (dlist: any, publicKey: string, privateKey: string, doctorEmail: string) => {
   for (const index in dlist) {
      let transaction = await bigchainService.listTransactions(dlist[index]);
      let metadata = transaction[transaction.length - 1].metadata;
      let doclist = metadata.doclist;
      console.log('Before', doclist.length);
      doclist = doclist.filter((item: any) => item.email != doctorEmail);
      console.log('After', doclist.length);
      metadata.doclist = doclist;
      metadata = JSON.stringify(metadata);
      console.log('metadata is ', metadata);
      let tx = await bigchainService.transferAsset(
         transaction[transaction.length - 1],
         metadata,
         publicKey,
         privateKey
      );
      console.log(tx.id);
   }
};
////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const showAccess = async (demail: string, records: any) => {
   let data: any = [];
   for (const asset of records) {
      const transaction = await bigchainService.listTransactions(asset.id);
      const doclist = transaction[transaction.length - 1].metadata.doclist;
      let result = doclist.filter((st: any) => st.email.includes(demail));
      if (result.length == 0) {
         data.push(asset);
      }
   }
   return data;
};
////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const showRevoke = async (demail: string, records: any) => {
   let data: any = [];

   for (const asset of records) {
      const transaction = await bigchainService.listTransactions(asset.id);
      const doclist = transaction[transaction.length - 1].metadata.doclist;
      let result = doclist.filter((st: any) => st.email.includes(demail));
      if (result.length != 0) {
         data.push(asset);
      }
   }
   return data;
};
////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const createRecord = async (
   data: any,
   email: string,
   fpath: any,
   publicKey: string,
   privateKey: string,
   secretKey: string
) => {
   let file = fs.readFileSync(fpath);
   let cipher = cryptoService.encrypt(file, secretKey);
   let fileBuffer = new Buffer(cipher);

   let ipfsURL = await ipfsService.AddFile(fileBuffer);
   let fileIPFSEncrypted = cryptoService.encrypt(ipfsURL, secretKey);
   let id = cryptoService.generateCode();

   data = {
      ...data,
      email: email,
      file: fileIPFSEncrypted,
      fileHash: cryptoService.hash(cipher),
      id: id
   };

   let metadata = {
      email: email,
      datetime: new Date().toString(),

      doclist: [],
      id: id
   };

   let tx = await bigchainService.createAsset(data, metadata, publicKey, privateKey);
   return tx;
};

export const getAssetHistory = async (assetid: any) => {
   const data: any = [];
   let transactions = await bigchainService.listTransactions(assetid);
   for (const transaction of transactions) {
      const filterTransaction: any = {
         operation: transaction.operation,
         date: transaction.metadata.datetime,
         doctor: []
      };
      if (transaction.operation == 'TRANSFER') {
         if (transaction.metadata.doclist.length > 0) {
            for (const doc of transaction.metadata.doclist) {
               filterTransaction['doctor'].push(doc.email);
            }
         }
      }
      data.push(filterTransaction);
   }
   return data;
};

export const getPrescription = async (email: string, demail: string) => {
   const data: any = [];
   let assets = await bigchainService.getAsset(demail);
   for (const id in assets) {
      let inter = await bigchainService.getAsset(assets[id].data.assetID);
      if (inter[0].data.email == email) {
         data.push({
            prescription: assets[0].data.prescription,
            file: cryptoService.decrypt(inter[0].data.file)
         });
      }
   }
   return data;
};
///////////////////////////////////////////////////////////////////////////////////////////////////
export const getDoctorFiles = async (email: string) => {
   let metadata = await bigchainService.getMetadata(email);
   let data: any = [];
   let assetSet = new Set();

   for (const meta of metadata) {
      const tx = await bigchainService.listTransactions(meta.id);
      assetSet.add(tx[tx.length - 1].asset.id);
   }
   let assetList = [...assetSet];
   assetList = assetList.filter(function (element: any) {
      return element !== undefined;
   });
   for (const asset of assetList) {
      const tx = await bigchainService.listTransactions(asset);
      const docs = tx[tx.length - 1].metadata.doclist;
      let result = docs.filter((st: any) => st.email.includes(email));
      if (result.length != 0) {
         let ass = await bigchainService.getAsset(asset);

         data.push({
            email: ass[0].data.email,
            file: cryptoService.decrypt(ass[0].data.file),
            description: ass[0].data.description,
            id: asset,
            pkey: tx[tx.length - 1].outputs[0].public_keys[0]
         });
      }
   }
   console.log(data);
   return data;
};

//////////////////////////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////////////////////////////////
// const getSingleDoctor = async(email, pass, action) => {
//     let data = {}
//     let db = await MongoClient.connect(url);
//     let dbo = db.db("project");
//     let result = await dbo.collection("dsignup").findOne({ email: email });
//     console.log(result);
//     if (action == "login") {
//         if (email == result.email && pass == result.password) {
//             data = {
//                 'email': decrypt(result.email),
//                 'name': `${result.fname} ${result.lname}`,
//                 'qualification': result.qual,
//                 'specialty': result.spl,
//                 'current': result.cw
//             }
//             console.log("login succesful.........");
//         } else {
//             console.log("not okay");
//         }
//     } else {
//         data = {
//             'email': decrypt(result.email),
//             'name': `${result.fname} ${result.lname}`,
//             'qualification': result.qual,
//             'specialty': result.spl,
//             'current': result.cw
//         }
//         console.log("Retrieved dctor deatilas successfully.....");
//     }
//     db.close();
//     return data;

// };
///////////////////////////////////////////////////////////////////////////////////////////////
// const insertDetails = async(collection, myobj) => {
//     let db = await MongoClient.connect(url);
//     let dbo = db.db("project");
//     let result = await dbo.collection(collection).insertOne(myobj);
//     console.log(`Inserted detils into ${collection}`);
//     db.close();
//     return result
// };
/////////////////////////////////////////////////////////////////////////////////////////////////
// const getMultipleDoctors = async() => {
//     let db = await MongoClient.connect(url);
//     let dbo = db.db("project");
//     let result = await dbo.collection('dsignup').find({}).toArray();
//     return result
// };
/////////////////////////////////////////////////////////////////////////////////////////////////
// const getPatient = async(email, pass) => {
//     let data = {}
//     let db = await MongoClient.connect(url);
//     let dbo = db.db("project");
//     let result = await dbo.collection("psignup").findOne({ email: email });

//     console.log(result);
//     if (email == result.email && pass == result.password) {
//         db.close();
//         data = { 'email': result.email }
//         return data;
//     } else {
//         db.close();
//         console.log("not okay");
//     }
// };
