import {PlecoExport} from './types';
import { getEntries } from 'chinese-lexicon';

import toneConvert from 'pinyin-tone-convert';

export class AnkiCard {
  hanzi: string
  pinyin: string
  definition: string
  semantic: string
  no_hearing = 'y'
  passive = 'y'
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
    const entries = getEntries(hanziChar)
    if(entries.length == 0) { return '' }
    // if(entries.length != 1) {
    //   return ""
    // }
    const correct = entries
    .filter((entry) => this.local_pinyin.startsWith(entry.pinyin))
    .map((entry) => {
     return entry.pinyin + ' - ' + entry.definitions.filter(filter_useless_definitions).join('/')
    });

    console.log(this.hanzi)
    console.log(entries)
    this.local_pinyin = this.local_pinyin.substring(entries[0].pinyin.length)


    return hanziChar + '(' + correct.join('/') + ')'
  }

  getSemantic(hanzi : string) : string {
    return hanzi.split(/(?:)/u).map((c) => this.withDefinition(c)).join(' + ');
  }

  convertPinyin(numbered : string) : string {
    return toneConvert(numbered.replaceAll('/', ''), {allowAnyChar: true})
  }


}

// eslint-disable-next-line func-style
function filter_useless_definitions(definition : string) {
  if(definition.startsWith('CL:')) {
    return false
  }

  return true
}


