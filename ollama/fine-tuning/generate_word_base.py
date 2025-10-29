import json
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Lemma, Synset
from nltk.corpus import brown
from nltk import pos_tag
from nltk.probability import FreqDist

TARGET_COUNT = 2500
LANG = "eng"

class Word:
    def __init__(self, name, pos, freq, definition=None, examples=None, synonyms=None, translations=None):
        self.name = name
        self.pos = pos
        self.freq = freq
        self.definition = definition or ""
        self.examples = examples or []
        self.synonyms = synonyms or []
        self.translations = translations or []

    def as_dict(self):
        return {
            "word": self.name,
            "pos": self.pos,
            "frequency": self.freq,
            "definition": self.definition,
            "examples": self.examples,
            "synonyms": self.synonyms,
            "translations": self.translations
        }

def get_wordnet_pos(tag: str):
    if tag.startswith('N'):
        return 'n'
    elif tag.startswith('V'):
        return 'v'
    elif tag.startswith('J'):
        return 'a'
    return None

def get_word_info(word, pos=None, lang='eng', target_lang='pol'):
    synsets = wn.synsets(word, pos=pos, lang=lang)
    if not synsets:
        return None
    s = synsets[0]
    return {
        "definition": s.definition(),
        "examples": s.examples(),
        "synonyms": [lemma.name() for lemma in s.lemmas(lang=lang)],
        "translations": [lemma.name() for lemma in s.lemmas(lang=target_lang)] if target_lang in wn.langs() else []
    }

words = [w.lower() for w in brown.words() if w.isalpha()]
fdist = FreqDist(words)
common = [w for w, _ in fdist.most_common(10000)]
tagged = pos_tag(common)
filtered = [(w, get_wordnet_pos(t)) for w, t in tagged if get_wordnet_pos(t)]

word_objects = []
for w, pos in filtered[:TARGET_COUNT]:
    info = get_word_info(w, pos, lang=LANG)
    if info:
        word_objects.append(Word(
            name=w,
            pos=pos,
            freq=fdist[w],
            definition=info["definition"],
            examples=info["examples"],
            synonyms=info["synonyms"],
            translations=info["translations"]
        ))

data = [w.as_dict() for w in word_objects]
with open(f"top_{TARGET_COUNT}_{LANG}.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(data)} words to top_{TARGET_COUNT}_{LANG}.json")
