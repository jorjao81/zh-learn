import {PlecoExport} from './types';
const toneConvert = require('pinyin-tone-convert')
import { getEntries } from "chinese-lexicon";

export class AnkiCard {
  hanzi: string
  pinyin: string
  definition: string
  semantic: string
  no_hearing: string = "y"
  passive: string = "y"
  local_pinyin: string
  // examples: string

  constructor(p : PlecoExport) {
    this.hanzi = p.hanzi
    this.pinyin = this.convertPinyin(p.pinyin_numbered)
    this.local_pinyin = this.pinyin.replaceAll(/[\s-]+/g, '').toLowerCase()
    this.definition = p.definition
    this.semantic = this.getSemantic(this.hanzi)
  }

  withDefinition(hanziChar: string) {
    console.log(hanziChar)
    let entries = getEntries(hanziChar)
    if(entries.length == 0) { return "" }
    // if(entries.length != 1) {
    //   return ""
    // }
    let correct = entries
    .filter((entry) => this.local_pinyin.startsWith(entry.pinyin))
    .map((entry) => {
     return entry.pinyin + " - " + entry.definitions.filter(filter_useless_definitions).join("/")
    });

    console.log(this.hanzi)
    console.log(entries)
    this.local_pinyin = this.local_pinyin.substring(entries[0].pinyin.length)


    return hanziChar + "(" + correct.join("/") + ")"
  }

  getSemantic(hanzi : string) : string {
    return hanzi.split(/(?:)/u).map((c) => this.withDefinition(c)).join(" + ");
  }

  convertPinyin(numbered : string) : string {
    return toneConvert(numbered.replaceAll("/", ""), {allowAnyChar: true})
  }


}

function filter_useless_definitions(definition : string) {
  if(definition.startsWith("CL:")) {
    return false
  }

  return true
}


