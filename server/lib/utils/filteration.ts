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
function filterSingle(query: Partial<RecordInterface>, record: RecordInterface) {
   if (query.date != null && query.date.getTime() < record.date.getTime()) return false;
   if (query.height != null && query.height !== record.height) {
      return false;
   }
   if (query.bp != null && query.bp !== record.bp) {
      return false;
   }
   if (query.age != null && query.age !== record.age) {
      return false;
   }
   if (query.weight != null && query.weight !== record.weight) {
      return false;
   }
   if (query.symptoms != null && record.symptoms != null && !record.symptoms.includes(query.symptoms)) {
      return false;
   }
   if (query.allergies != null && record.allergies != null && !record.allergies.includes(query.allergies)) {
      return false;
   }
   if (query.description != null && record.description != null && !record.description.includes(query.description)) {
      return false;
   }
   return true;
}

export function filterRecords(records: RecordInterface[], query: Partial<RecordInterface>) {
   return records.filter(record => filterSingle(query, record));
}
