import vertexai
from vertexai.preview.language_models import TextGenerationModel

import markdown_to_json
import os
import sys
import json

level_descriptions = {
    "beginner": "complete beginner (no prior knowledge)",
    "basic": "basic language knowledge (less than A1)",
    "a1": "CEFR Level A1 (Beginner)",
    "a2": "CEFR Level A2 (Elementary)",
    "b1": "CEFR Level B1 (Intermediate)",
    "b2": "CEFR Level B2 (Upper intermediate)",
    "c1": "CEFR Level C1 (Advanced)",
    "c2": "CEFR Level C2 (Proficient)",
}

vertexai.init(project="hackzurich23-8208", location="us-central1")
parameters = {
    "max_output_tokens": 4096,
    "temperature": 0,
    "top_p": 0.8,
    "top_k": 40
}

model = TextGenerationModel.from_pretrained("text-bison-32k")

def generate_plan(language, start, goal):
    response = model.predict(
        """You are a professor teaching spanish at Harvard, who specializes in creating custom learning plans to help people learn the spanish language and get from any language level to another. These levels are usually given in CEFR levels (e.g. A1, B1, ...).

The levels are: complete beginner, basic language knowledge, A1, A2, B1, B2, C1, C2

For later courses (starting at B1), specific real-world topics, such as Culture or Business, should be included. The tutors teaching the earlier courses are not knowledgable in these specific topics as they are non-native speakers and are not able to teach these topics.

The learning plan should be made up of exactly 48 lessons outlined into units (exactly 8 units), levels (exactly 6 levels per unit). Units and levels should be signified by their identifier and a name. Unit and levels names should be at most 6 words long and simple sentences. Output withouts prefixes.

Each lessons will later, by another professor, be separated into individual levels that will each contain 12 different tasks. These tasks will have one of the following types:
- Vocab: A new word
- Translate sentence: A sentence will be given in the persons native language, they will translate it to the language they are learning
- Transcribe sentence: A tutor will read a sentence out loud, and the person will transcribe the sentence into words
- Mix and Match: The student will be given a list of words in their native language and a list of the translate words in the language they are learning, and they will match them.

Do not include tasks or levels in your plan. They are only given so you are aware what will happen later and can ensure that the lessons or units are not specific (only reading or only writing, as both reading and writing will be done in each lesson).

The tutors using the plans ensure that lessons learned are reviewed, there is no need for you to add specific lessons for this.

Output the learning plan as a markdown with each Unit being a level-1 header and Lessons being included in the form of a list.

Request: Please create a language learning plan for a complete beginner (no prior knowledge) to get to an basic language knowledge (less than A1) level.
Learning Plan:""".format(language, language, level_descriptions[start], level_descriptions[goal]),
        **parameters
    )
    value = response.text

    print("Got response from PaLM, value")

    base_directory = "plans/{}/{}-{}".format(language, start, goal)

    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    dictified = markdown_to_json.dictify(value)
    units = dictified.keys()

    data = []

    for unit in units:
        split = unit.split(": ")
        unitName = split[1] if len(split) > 1 else unit
        lessons = []
        for lesson in dictified[unit]:
            split = lesson.split(": ")
            lessonName = split[1] if len(split) > 1 else lesson
            if not lessonName is None:
                lessons.append(lessonName.strip())
            else:
                print("Failed to handle", lesson)

        data.append({ 'name': unitName.strip(), 'lessons': lessons })

    with open("{}/summary.json".format(base_directory), "w") as outfile:
        json.dump(data, outfile)

levels = ["beginner", "basic", "a1", "a2", "b1", "b2", "c1", "c2"]

for i in range(0, len(levels) - 1):
    print(sys.argv[1], levels[i], levels[i+1])
    generate_plan(sys.argv[1], levels[i], levels[i+1])