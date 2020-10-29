import { UserInterface, RecordInterface, MetadataInterface, PresecriptionInterface } from '../models/user.models';
import { ODataFilterBuilder, BuilderFunc, BoolArg } from 'ts-odata-key';

type filterFunction<T> = BuilderFunc<T>;

export const queryFunction = (query: any) => {
   const filterList: filterFunction<RecordInterface>[] = [];
   for (const [key, value] of Object.entries(query)) {
      if (key == 'date') {
         const date = new Date(value as string);
         filterList.push(({ gt }, p) => gt(p.date, date));
      } else if (key == 'height') {
         filterList.push(({ eq }, p) => eq(p.height, value));
      } else if (key == 'weight') {
         filterList.push(({ eq }, p) => eq(p.weight, value));
      } else if (key == 'symptoms') {
         filterList.push(({ eq }, p) => eq(p.symptoms, value));
      } else if (key == 'allergies') {
         filterList.push(({ eq }, p) => eq(p.allergies, value));
      } else if (key == 'description') {
         filterList.push(({ eq }, p) => eq(p.description, value));
      } else if (key == 'bp') {
         filterList.push(({ eq }, p) => eq(p.bp, value));
      } else if (key == 'age') {
         filterList.push(({ eq }, p) => eq(p.age, value));
      }
   }
   return filterList;
};

export const filterRecords = (records, query) => {};
