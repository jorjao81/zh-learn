#!/usr/bin/env node

import * as fs from 'fs';
import * as path from 'path';
import { parse } from 'csv-parse';
import {PlecoExport} from './types';
import {AnkiCard} from './anki-card';

import {createObjectCsvWriter as createCsvWriter} from 'csv-writer';

(() => {
  const csvFilePath = path.resolve('flash.txt');

  const headers = ['hanzi', 'pinyin_numbered', 'definition'];

  const fileContent = fs.readFileSync(csvFilePath, { encoding: 'utf-8' });
  const csvWriter = createCsvWriter({
    path: 'processed.csv',
    header: [
  'pinyin',
'hanzi',
'pronunciation',
'definition',
'examples',
 'phonetic',
'semantic',
'similar',
'passive',
'alternate',
'no_hearing'
    ]
  });

  parse(fileContent, {
    delimiter: '\t',
    columns: headers,
    relax_column_count: true,
    relax_quotes: true
  }, (error, result: PlecoExport[]) => {
    if (error != undefined) {
      console.error(error);
    }

    const anki = result.map((e) => new AnkiCard(e))
    csvWriter.writeRecords(anki)       // returns a promise
    .then(() => {
      console.log('...Done');
    });

  });
})();
export {};
