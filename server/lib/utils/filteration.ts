import { RecordInterface } from '../models/user.models';
// export const queryFunction = (query: any) => {
//    for (const [key, value] of Object.entries(query)) {
//       if (key == 'date') {
//          const date = new Date(value as string);
//       } else if (key == 'height') {
//       } else if (key == 'weight') {
//       } else if (key == 'symptoms') {
//       } else if (key == 'allergies') {
//       } else if (key == 'description') {
//       } else if (key == 'bp') {
//       } else if (key == 'age') {
//       }
//    }
//    return filterList;
// };
function filterSingle(query: Partial<RecordInterface>, record: any) {
   if (query.date != null && new Date(query.date).getTime() == new Date(record.data.date).getTime()) return false;
   if (query.height != null ) {//&& query.height !== record.data.height) {
      return false;
   }
   if (query.bp != null ) {//&& query.bp !== record.data.bp) {
      return false;
   }
   if (query.age != null){ // && query.age !== record.data.age) {
      return false;
   }
   if (query.weight != null) {//  && query.weight !== record.data.weight) {
      return false;
   }
   if (query.symptoms != null) {// && record.data.symptoms != null && !record.data.symptoms.includes(query.symptoms)) {
      return false;
   }
   if (query.allergies != null){ // && record.data.allergies != null && !record.data.allergies.includes(query.allergies)) {
      return false;
   }
   if (query.description != null) {// && record.data.description != null && !record.data.description.includes(query.description)) {
      return false;
   }
   return true;
}

export function filterRecords(records: RecordInterface[], query: Partial<RecordInterface & {key : string[]}>) {
   let frecords = records.filter(record => filterSingle(query, record));
   if (query.key == null || query.key.length === 0) {
      return frecords;
   } 
   const result = frecords.map(frecord => {
      const newRecord: Partial<RecordInterface> = {}
      Object.keys(query).forEach(key => {
            newRecord[key] = frecord['data'][key]
      })
      return newRecord;
   })
   console.log(result)
   return result;
     
}
