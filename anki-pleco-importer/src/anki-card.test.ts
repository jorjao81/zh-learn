import {describe, expect, test} from '@jest/globals';
import {PlecoExport} from './types';
import {AnkiCard} from './anki-card';

test('adds 1 + 2 to equal 3', () => {
  const t : PlecoExport = {
    hanzi: '悄无声息',
    pinyin_numbered: 'qiao3wu2sheng1xi1',
    definition: '1 quietly 2 noiselessly'
  }
  expect(new AnkiCard(t)).toEqual({
    hanzi: '悄无声息',
    pinyin: 'qiǎowúshēngxī',
    definition: '1 quietly 2 noiselessly'
  });

});

describe('semantics', () => {
  test('adds definition to characters', () => {
    expect(new AnkiCard({
      hanzi: '打鱼',
      pinyin_numbered:	'da3//yu2',
      definition:	''
    })).toEqual({
          hanzi: '打鱼',
          pinyin: 'dǎyú',
          definition: '',
          semantic: '打(to beat) + 鱼(fish)'
        }
    )
  })
})
