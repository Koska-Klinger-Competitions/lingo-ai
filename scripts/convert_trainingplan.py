import markdown_to_json
import sys
import json

if len(sys.argv) != 3:
    print("Usage: convert_trainingplan.py <plan.md> <plan.json>")

value = open(sys.argv[1]).read()

dictified = markdown_to_json.dictify(value)
units = dictified.keys()

data = []

unitIdx = 1
for unit in units:
    unitName = unit.split(": ")[1].strip()
    lessons = []
    lessonIdx = 1
    for lesson in dictified[unit]:
        split = lesson.split(" - ")
        lessonName = split[1] if len(split) > 1 else lesson
        if not lessonName is None:
            lessons.append({ 'name': lessonName.strip(), 'type': 'lesson' })
            lessonIdx += 1
        else:
            print("Failed to handle", lesson)

    if len(lessons) >= 6:
        lessons.insert(int(len(lessons) / 2), { 'name': 'Personal Training', 'type': 'personal_training' })

    if len(lessons) >= 4:
        lessons.append({'name': 'Review', 'type': 'review' })

    for i in range(len(lessons)):
        lessons[i]['id'] = i + 1

    data.append({ 'id': unitIdx, 'name': unitName, 'lessons': lessons })
    unitIdx += 1

with open(sys.argv[2], "w") as outfile:
    json.dump(data, outfile)