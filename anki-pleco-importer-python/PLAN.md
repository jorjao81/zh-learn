Implement each feature in their own branch

## Feature: semantic markup

Goal: create Anki cards using only semantic markup, and no explicit formatting. This will make changes in the
presentation of cards possible by just changing a CSS; it will also make processing cards to extract meaningfull
information easier.

### Details:

* Part os speech markers such as noun, adjective, verb etc should be marked wit class "part-of-speech"
* Domain markers such as physiscs, sports, aerospace should be marked with class "domain"
* Pragma or usage markers such as "literary", "dated", "colloquial", "pejorative", should each be marked with 2 classes: the literal "usage" class and also the usage marker itself, eg, "literary", "dated".
* If you have better suggestions for the class names, let me know
* multiple definitions should use proper HTML list markers
* multiple examples should use proper HTML list markers
* each example should have a class "example"
* inside the examples, mark the classes "hanzi" for chinese characters, "pinyin" for pinyin and "translation" for the translation
* in the character decomposition, mark each part with the class "phonetic" or "semantic" or "unknown" accordingly, also mark the pinyin and the definition
* For the word decomposition, also use list to mark each part of the composition.

Plan in detail before implementing
