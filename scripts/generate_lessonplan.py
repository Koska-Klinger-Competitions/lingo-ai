import os.path

import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

import json

language = "german"
course = "beginner-basic"
unit = 1
lesson = 3

base_url = "plans/{}/{}".format(language, course)

learning_plan = open(base_url + '/summary.md').read()

vertexai.init(project="hackzurich23-8208", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison-32k")
parameters = {
    "max_output_tokens": 8192,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
chat = chat_model.start_chat(
    context="""You are a professor teaching {} at harvard. In the previous step you created a learning plan that is attached below.

Learning plan:
{}

You will be provided with a unit and lesson number (e.g. Unit 1, Lesson 1) and will create a detailed lesson plan.

Each lesson contains 4 to 6 levels and each level contains 8 to 14 different tasks.
The task types are: vocab, translate, transcribe_easy, transcribe_hard, speech. Avoid having 2 tasks of the same type in a row. The distribution should be vaguely equal.

# Vocab Task (vocab)
A single new word is presented in the language the are learning and the user should enter the english translation. The valid keys are new_word, translation.

# Translation Task (translate)
A sentence is provided in english, and the user should translate it to the language they are learning, provide up to 3 valid translations as an array. The valid keys are: sentence, translations.

# Transcription Task - Easy (transcribe_easy
A sentence is read out loud to the user in the language they are learning and they are provided with a array of different words that may appear in the sentence, at least half of the words should not appear in the sentence, and the students click on these words in the correct order to build the sentence they just heard. The valid keys are: sentence, options

# Transcription Task - Hard (transcribe_hard)
A sentence is read out loud to the user in the language they are learning and they should transcribe it to text. The valid keys are: sentence

# Speech (speech)
A sentence is given to the user in the language they are learning and they are supposed to say it out loud. The valid keys are: sentence

Words should be incrementally introduced using vocab tasks before being used in other tasks.

Use real names at all times. The names should be the most popular name in the language (e.g. Peter for German).

You will be asked to provide a detailed lesson plane:
Output the tasks as a JSON. Valid properties are: tasks.""".format(language, learning_plan),
)

lesson_path = "{}/{}/{}".format(base_url, unit, lesson)
if not os.path.exists(lesson_path):
    os.makedirs(lesson_path)

response = chat.send_message("How many levels should be created for Unit {} - Lesson {}. Only output the number of levels without comments.".format(unit, lesson)).text
number_of_levels = int(response)

for i in range(number_of_levels):
    response = chat.send_message("Create a detailed level plan for Unit {} - Lesson {} - Level {} that contains 8 - 12 tasks.".format(unit, lesson, i+1), **parameters)
    text = response.text.replace("```JSON", "").replace("```", "")
    tasks = json.loads(text)['tasks']

    for j in range(len(tasks)):
        tasks[j]['id'] = j+1

    with open("{}/{}.json".format(lesson_path, i+1), "w") as outfile:
        json.dump(tasks, outfile)