
* In the current flash.txt the export to CSV made lots of mistakes with the examples, where it did not use the semantic markers correctly, eg, in 仿佛. Find out those examples, build test scenarios around them and fix them.

* In the current flash.txt, the word 三维 has 2 definitions, but they were identified as only 1. Add a test scenario around it and fix it.

* In the current flash.txt, in the words 转向 and 末日 you added the part-of-speech as it's own definition, ie, inside an <li> of it's own, while it should have been outside the <ol> as it applies to all definitions in those examples. Add test scenario and fix it.

* The cards are getting a bit too long vertically in practice. I see a few issues: 
* The pinyin below the chinese text takes a lot of space. We can fit it, together with the audio, on the side of Chinese characters.
* The structural analysis is almost always being rendered horizontally. Can you force the boxes to stay less wide and
so increase the changes it is rendered side-by-side? You can wrap long definitions. Also put the pinyin in the structural analysis next to the hanzi.
* Maybe also slightly reduce horizontal margins everywhere.