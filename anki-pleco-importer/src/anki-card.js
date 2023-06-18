"use strict";
exports.__esModule = true;
exports.AnkiCard = void 0;
var chinese_lexicon_1 = require("chinese-lexicon");
var pinyin_tone_convert_1 = require("pinyin-tone-convert");
var AnkiCard = /** @class */ (function () {
    // examples: string
    function AnkiCard(p) {
        this.no_hearing = 'y';
        this.passive = 'y';
        this.hanzi = p.hanzi;
        this.pinyin = this.convertPinyin(p.pinyin_numbered);
        this.local_pinyin = this.pinyin.replaceAll(/[\s-]+/g, '').toLowerCase();
        this.definition = p.definition;
        this.semantic = this.getSemantic(this.hanzi);
    }
    AnkiCard.prototype.withDefinition = function (hanziChar) {
        var _this = this;
        console.log(hanziChar);
        var entries = (0, chinese_lexicon_1.getEntries)(hanziChar);
        if (entries.length == 0) {
            return '';
        }
        // if(entries.length != 1) {
        //   return ""
        // }
        var correct = entries
            .filter(function (entry) { return _this.local_pinyin.startsWith(entry.pinyin); })
            .map(function (entry) {
            return entry.pinyin + ' - ' + entry.definitions.filter(filter_useless_definitions).join('/');
        });
        console.log(this.hanzi);
        console.log(entries);
        this.local_pinyin = this.local_pinyin.substring(entries[0].pinyin.length);
        return hanziChar + '(' + correct.join('/') + ')';
    };
    AnkiCard.prototype.getSemantic = function (hanzi) {
        var _this = this;
        return hanzi.split(/(?:)/u).map(function (c) { return _this.withDefinition(c); }).join(' + ');
    };
    AnkiCard.prototype.convertPinyin = function (numbered) {
        return (0, pinyin_tone_convert_1["default"])(numbered.replaceAll('/', ''), { allowAnyChar: true });
    };
    return AnkiCard;
}());
exports.AnkiCard = AnkiCard;
// eslint-disable-next-line func-style
function filter_useless_definitions(definition) {
    if (definition.startsWith('CL:')) {
        return false;
    }
    return true;
}
