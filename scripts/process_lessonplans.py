import json
import os.path
import sys
import glob
import hashlib
from google.cloud import texttospeech

if len(sys.argv) != 4:
    print("Usage: process_lessonplans.py <language> <course> <unit/lesson>")
    sys.exit(1)

client = texttospeech.TextToSpeechClient()
english_voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Studio-M")

language = sys.argv[1]
if language == "spanish":
    spanish_voice = texttospeech.VoiceSelectionParams(language_code="es-US", name="es-US-Studio-B")
elif language == "german":
    spanish_voice = texttospeech.VoiceSelectionParams(language_code="de-DE", name="de-DE-Polyglot-1")
else:
    print("Unsupported language {}. Support: german, english".format(language))
    sys.exit(1)

audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=1)

sentence_list_path = "plans/" + sys.argv[1] + "/sentences"
word_list_foreign_path = "plans/" + sys.argv[1] + "/" + sys.argv[2] + "/word_list_foreign.json"
word_list_native_path = "plans/" + sys.argv[1] + "/" + sys.argv[2] + "/word_list_native.json"

if not os.path.exists(sentence_list_path):
    os.makedirs(sentence_list_path)
    generated_sentences = []
else:
    generated_sentences = list(map(lambda x: x.split("/")[-1].split(".")[0], os.listdir(sentence_list_path)))

if os.path.exists(word_list_foreign_path):
    word_list_foreign = set[str](json.loads(open(word_list_foreign_path).read()))
else:
    word_list_foreign = set[str]()

if os.path.exists(word_list_native_path):
    word_list_native = set[str](json.loads(open(word_list_native_path).read()))
else:
    word_list_native = set[str]()

def add_to_native_word_list(sentence):
    for word in sentence.split(" "):
        word_list_native.add(''.join(filter(str.isalnum, word)).lower())

def add_to_foreign_word_list(sentence):
    for word in sentence.split(" "):
        word_list_foreign.add(''.join(filter(str.isalnum, word)).lower())

def handle_phrase(phrase: str, is_english: bool = False) -> str:
    hash_code = hashlib.md5(phrase.encode()).hexdigest()
    if not generated_sentences.__contains__(hash_code):
        input_text = texttospeech.SynthesisInput(text=phrase)
        synthResponse = client.synthesize_speech(
            request={"input": input_text, "voice": english_voice if is_english else spanish_voice, "audio_config": audio_config}
        )
        with open(sentence_list_path + "/{}.mp3".format(hash_code), "wb") as out:
            out.write(synthResponse.audio_content)

    return hash_code

for file in glob.glob("plans/{}/{}/{}/*.json".format(sys.argv[1], sys.argv[2], sys.argv[3])):
    tasks = json.loads(open(file).read())
    for task in tasks:
        if task['type'] == 'vocab':
            task['spoken_id'] = handle_phrase(task["new_word"])
            add_to_foreign_word_list(task['new_word'])
            add_to_native_word_list(task['translation'])
        elif 'transcribe_' in task['type']:
            add_to_foreign_word_list(task['sentence'])
            task['spoken_id'] = handle_phrase(task["sentence"])
        elif task['type'] == 'translate':
            task['spoken_id'] = handle_phrase(task["sentence"], is_english=True)
            for trans in task['translations']:
                add_to_foreign_word_list(trans)
            add_to_native_word_list(task['sentence'])

    with open(file, "w") as outfile:
        json.dump(tasks, outfile)

    print("File processed")

with open(word_list_foreign_path, "w") as outfile:
    json.dump(list(word_list_foreign), outfile)

with open(word_list_native_path, "w") as outfile:
    json.dump(list(word_list_native), outfile)