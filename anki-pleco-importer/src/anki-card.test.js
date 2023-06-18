"use strict";
exports.__esModule = true;
var globals_1 = require("@jest/globals");
var anki_card_1 = require("./anki-card");
(0, globals_1.test)('adds 1 + 2 to equal 3', function () {
    var t = {
        hanzi: '悄无声息',
        pinyin_numbered: 'qiao3wu2sheng1xi1',
        definition: '1 quietly 2 noiselessly'
    };
    (0, globals_1.expect)(new anki_card_1.AnkiCard(t)).toEqual({
        hanzi: '悄无声息',
        pinyin: 'qiǎowúshēngxī',
        definition: '1 quietly 2 noiselessly'
    });
});
(0, globals_1.describe)('semantics', function () {
    (0, globals_1.test)('adds definition to characters', function () {
        (0, globals_1.expect)(new anki_card_1.AnkiCard({
            hanzi: '打鱼',
            pinyin_numbered: 'da3//yu2',
            definition: ''
        })).toEqual({
            hanzi: '打鱼',
            pinyin: 'dǎyú',
            definition: '',
            semantic: '打(to beat) + 鱼(fish)'
        });
    });
});
