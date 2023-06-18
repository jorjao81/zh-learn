#!/usr/bin/env node
"use strict";
exports.__esModule = true;
var fs = require("fs");
var path = require("path");
var csv_parse_1 = require("csv-parse");
var anki_card_1 = require("./anki-card");
var csv_writer_1 = require("csv-writer");
(function () {
    var csvFilePath = path.resolve('flash.txt');
    var headers = ['hanzi', 'pinyin_numbered', 'definition'];
    var fileContent = fs.readFileSync(csvFilePath, { encoding: 'utf-8' });
    var csvWriter = (0, csv_writer_1.createObjectCsvWriter)({
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
    (0, csv_parse_1.parse)(fileContent, {
        delimiter: '\t',
        columns: headers,
        relax_column_count: true,
        relax_quotes: true
    }, function (error, result) {
        if (error != undefined) {
            console.error(error);
        }
        var anki = result.map(function (e) { return new anki_card_1.AnkiCard(e); });
        csvWriter.writeRecords(anki) // returns a promise
            .then(function () {
            console.log('...Done');
        });
    });
})();
