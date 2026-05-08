"""
script zum auflisten der Fragen
Parameter: Quiz im json Format
Ergebnis: html File
"""

import json
import sys
import os
import time

if len(sys.argv) < 2:
	DataFileName = "quiz.json"
else:
	DataFileName = sys.argv[1]
print ("opening file " + DataFileName)
try:
	with open(DataFileName) as data_file:
		data = json.load(data_file)
except Exception as e:
	print (str(e))
	sys.exit()

outFile = open ("questions.html", "w")
outFile.write ("<h1>Fragen aus " + DataFileName + "</h1>")
outFile.write ("<font size=+2>")
outFile.write ("Stand von " + time.ctime(os.path.getmtime(DataFileName)))
outFile.write ("<p>")

count = 0
for quiz_question_json in data:
	question = quiz_question_json["question"]
	print (question)
	outFile.write (question + "<br>")
	count = count+1

outFile.write  ("</p>")
outFile.write  (str(count) + " Fragen<br>")
outFile.write  ("</font>")

outFile.close()

