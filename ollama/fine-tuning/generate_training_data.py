import LLM
import os
from pathlib import Path

PROMPT_TEMPLATE = """
You are an expert linguist and data scientist. Your task is to generate high-quality, structured JSON data for fine-tuning a multilingual translation model. The data must follow a precise format.
**Format Rules:**

1.  The output must be a list of valid JSON objects.
2.  Each JSON object must contain two keys: "prompt" and "completion".
3.  The value of "prompt" must be a JSON string with three keys:
    * `word`: The word to be translated (in the native language).
    * `native`: The two-letter code for the source language.
    * `foreign`: The two-letter code for the target language.
4.  The value of "completion" must be a JSON string with five keys:
    * `translation`: The translated word (in the foreign language).
    * `meaning`: A brief definition of the `word` (in the native language).
    * `type`: The part of speech of the `word` (e.g., "noun", "verb", "adjective", in the native language's grammar terms if possible).
    * `synonyms`: A list of 3 synonyms for the `word` (in the native language).
    * `examples`: A list of 3 natural-sounding example sentences using the `translation` (in the foreign language).
**High-Quality Examples:**
Here are three examples of the required format and quality. Follow this structure exactly.
**Example 1 (Polish to English Noun):**
{
  "prompt": "{\"word\": \"dom\", \"native\": \"pl\", \"foreign\": \"en\"}",
  "completion": "{\"translation\": \"house\", \"meaning\": \"budynek mieszkalny, miejsce zamieszkania\", \"type\": \"rzeczownik\", \"synonyms\": [\"mieszkanie\", \"budynek\", \"siedziba\"], \"examples\": [\"My house is located in the suburbs.\", \"The old house needs renovation.\", \"They bought a new house last year.\"]}"
}
**Example 2 (German to Italian Adjective):**
{
  "prompt": "{\"word\": \"blau\", \"native\": \"de\", \"foreign\": \"it\"}",
  "completion": "{\"translation\": \"blu\", \"meaning\": \"Farbe des Himmels an einem sonnigen Tag\", \"type\": \"Adjektiv\", \"synonyms\": [\"himmelblau\", \"azurblau\", \"türkis\"], \"examples\": [\"Il cielo blu è meraviglioso.\", \"La mia macchina blu è nuova.\", \"Il mare blu è molto profondo.\"]}"
}
**Example 3 (French to Spanish Noun):**
{
  "prompt": "{\"word\": \"maison\", \"native\": \"fr\", \"foreign\": \"es\"}",
  "completion": "{\"translation\": \"casa\", \"meaning\": \"bâtiment destiné à l'habitation\", \"type\": \"nom féminin\", \"synonyms\": [\"demeure\", \"habitation\", \"logis\"], \"examples\": [\"Mi casa está cerca del parque.\", \"La casa tiene un jardín hermoso.\", \"Vamos a casa después del trabajo.\"]}"
}
"""
"""
**Your Task:**

Now, generate {BATCH_SIZE} new and unique entries for the following language pair, based on this list of words: [WORD_LIST].
* `native`: "{NATIVE_LANG_CODE}"
* `foreign`: "{FOREIGN_LANG_CODE}"
"""

# training_data for every language pair will follow the following structure:
#   en/
#       de.json
#       es.json
#       ...
#   de/
#       en.json
#       es.json
#       ...
#   ...

supported_languages = [
    "en",
    "de",
    "es",
    "fr",
    "it",
    "pl",
    "ja",
]

base_dir = Path("./training_data")
for native_lang in supported_languages:
    # print(native_lang + "/")
    languages_to_generate = [x for x in supported_languages if x != native_lang]

    native_dir = base_dir / native_lang
    native_dir.mkdir(exist_ok=True)

    for foreign_lang in languages_to_generate:
        training_data_path = native_dir / f"{foreign_lang}.json"
        training_data_path.touch(exist_ok=True)


ENTRIES_PER_FILE = 2000
BATCH_SIZE = 50

for native_dir in base_dir.iterdir():
    print(native_dir)
    if native_dir.is_dir() and native_dir.name in supported_languages:
        native_lang = native_dir.name

        for json_file in native_dir.glob("*.json"):
            foreign_lang = json_file.stem                             # Note: .stem gives bare name, without the extension
            final_prompt = PROMPT_TEMPLATE.format(
                
            )


# try:
#     model_testowy = LLM.initialize_model()
#     response = model_testowy.generate_content("Powiedz 'kupa' po angielsku.")
#     print("Response:", response.text.strip())
# except ValueError as e:
#     print(e)