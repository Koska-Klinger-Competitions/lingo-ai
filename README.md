# 🌎 LingoLearn
An extendable platform for teaching complex things, the easy way

## 📋 Features
Through state of the art Machine Learning learning is made easier using a system that you don't just learn from, but that also learns from you. 
- [x] Open Source
- [x] Advanced Machine Translation 
- [x] Using industry leading Large Language Models
- [x] Fully autonomous, with safty belt attached 

## 📖 Documentation 
The AI-Backend for LingoLearn has been implemented in Python. 

The aim of this section of LingoLearn is to generate task subject plans, meaning plans about how one is approach the teaching of a given subject, course plans and then also concrete lesson plans. 
All this was written with the thought of extendability and dynamisation front and center in mind. Through this aforementioned highly structured approach the system is able to provide the best value for teaching in most subjects, whilst it's high customisability allows for a custom tailored learning experience for every user. 

## 📝 License
Licensed under the MIT license.

## Lexion Of Scripts 
1. generate_lessonplans.py 
	The centerpiece: This script converts our course plans into concrete lessons using the Google "chat-bison-32k" LLM
2. process_lessonplans.py
	This script converts the chosen phrases that are to be used for spoken exercises, converts them into spoken language for the learner to hear
3. generate_vocab_translations.py
	This script utalises the lecture plans to generated vocab specifically targeted towards the learners language. 
4. generate_trainingplan.py
	This script generates the foundational course plans needed to structure the education. 
5. convert_trainingsplan.py 
	This script converts the trainingplan from the incoming markdown to the more useful json. 