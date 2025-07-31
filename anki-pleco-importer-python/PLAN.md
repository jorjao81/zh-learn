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


## Refactor: add a real domain model, and separate the domain from it's representation in HTML

Currently, the code base is mixing representation of HTML with the domain information. Think hard, look at the code and at how I represent it in Anki and try to find a domain model of python class or classes representing a chinese vocabulary item for spaced repetition learning. E.g, a word has hanzi chars, pinyin, a structural decomposition, examples, definitions. Examples are usually made of hanzi, pinyin and translation, whereas definitions are more complex; they can have part-of-speech, domain, usage, etc.