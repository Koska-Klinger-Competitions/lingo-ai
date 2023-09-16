import sys
import json

import vertexai
from vertexai.preview.language_models import TextGenerationModel, InputOutputTextPair

if len(sys.argv) != 3:
    print("Usage: generate_vocab_translations.py <language> <course>")
    sys.exit(1)

language = sys.argv[1]
course = sys.argv[2]

base_path = "plans/{}/{}".format(language, course)
foreign_words = json.loads(open(base_path + "/word_list_foreign.json").read())
native_words = json.loads(open(base_path + "/word_list_native.json").read())

vertexai.init(project="hackzurich23-8208", location="us-central1")
parameters = {
    "max_output_tokens": 256,
    "temperature": 0,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison@001")

foreign_translations = {}
native_translations = {}

for word in foreign_words:
    response = model.predict(
        """You are a professor teaching {} at harvard. You will be asked to translate phrases from/to english to the language you teach.

    Please translate the given phrase to English. Please output only the best valid translation without any extra info.

    Phrase: {}
    Translation:""".format(language, word),
        **parameters
    ).text
    print(word, response)
    foreign_translations[word] = response

for word in native_words:
    response = model.predict(
        """You are a professor teaching {} at harvard. You will be asked to translate phrases from/to english to the language you teach.

    Please translate the given phrase from English to Spanish. Please output only the best valid translation without any extra info.

    Phrase: {}
    Translation:
    """.format(language, word),
        **parameters
    ).text
    print(word, response)
    native_translations[word] = response

with open(base_path + "/translations_foreign.json", "w") as out:
    json.dump(foreign_translations, out)

with open(base_path + "/translations_native.json", "w") as out:
    json.dump(native_translations, out)
