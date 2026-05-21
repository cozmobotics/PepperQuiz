# -*- coding: iso-8859-1 -*-

# The filename is passed as a command line argument --quiz (default: "quiz.json"). 
# The IP address is passed as a command line argument --ip
# Each question and possible answers are displayed on the screen and pronounced by Pepper

# known issues:
# screensaver (moving dots) is activated sometimes  

# todo:
# Umlaute workaround
# buttons groesser
# optional: info bei jeder Frage
# feedback (alter, geschlecht, war es lehrreich/lustig,...)
# json syntax test (try/except)

import sys

if (sys.version_info.major) != 2:
	print ("Bittte nur in Python 2 starten!!!")
	sys.exit()

import json
from random import randrange, shuffle
import argparse
import datetime

from doJavascript import setupJavascript
from doJavascript import introduction
from doJavascript import askQuestion
from doJavascript import showResult
from doJavascript import finish
from doJavascript import endJavascript



#======================================================================================
class QuizQuestion:
	"""A single multiple choice question with 4 choices, one correct.
	
	Args:
		question (str): The question.
		answer_options (list of str): 4 multiple choice answers where the
			1st element is the correct answer. (Choices will be shuffled each time.)
	Raises:
		:class:`ValueError` if not supplied exactly 4 answer_options.
	"""
	def __init__(self, question, answer_options, info):
		if len(answer_options) != 4:
			raise ValueError("Expected 4 answer_options, got %s" % len(answer_options))
		self.question = question
		self._answer_index = 0
		self.answer_options = list(answer_options)  # copy the answer_options, so we can shuffle them
		self.info = info
		# self.shuffle_answer_options()

	@property
	def answer_number(self):
		"""int: The number (i.e. 1, 2, 3 or 4) representing the correct answer."""
		return self._answer_index + 1

	@property
	def answer_str(self):
		"""str: The string representing the correct answer."""
		return self.answer_options[self._answer_index]

	# def shuffle_answer_options(self):
		# """Shuffle the answer_options so that they're not always read in the same order."""

		# # to shuffle whilst keeping track of the answer, we first pop the
		# # answer out, shuffle the rest, and then insert the answer at a random
		# # known point.
		# answer = self.answer_options.pop(self._answer_index)
		# shuffle(self.answer_options)
		# self._answer_index = randrange(len(self.answer_options)+1)
		# self.answer_options.insert(self._answer_index, answer)


#=================================================================================


# #--------------------------------------------------------------------------------------
def shuffle_answer_options(MyQuestion):
	"""Shuffle the answer_options so that they're not always read in the same order."""

	# to shuffle whilst keeping track of the answer, we first pop the
	# answer out, shuffle the rest, and then insert the answer at a random
	# known point.
	global answer_index
	
	answer = MyQuestion.answer_options.pop(0)
	# print ("popped: " + answer)
	shuffle(MyQuestion.answer_options)
	answer_index = randrange(len(MyQuestion.answer_options)+1)
	MyQuestion.answer_options.insert(answer_index, answer)
	# print ("inserted at: " + str(answer_index))


#--------------------------------------------------------------------------------------
def get_next_question():
	global questions
	global LQuestion
	global Options
	global TimeRemaining
	global NumQuestions
	global QuestionNr
	
	if len(questions) > 0:
		i = randrange(len(questions))
		question = questions.pop(i)
		
		shuffle_answer_options(question)
		
		
		
		#print ("\n**************************************")
		#print ("question: "+ question.question) 
		#print ("correct: " + question.answer_options[answer_index])

		
		return question
	else:
		print("Out of questions!")
		return None




	
#------------------------------------------------------------------------------------
def clearGuesses ():
	global players
	global Options
	
	for Count in range (3):
		Player = players[Count]
		Player.guess = 4 # invalid 
		players[Count] = Player
		
	
#----------------------------------------------------------------------------------------------------
def prepareProtocol (Filename):

	FileHandle = open (Filename, "a")
	
	if (FileHandle):
		FileHandle.write ("============================================================\n")
		datetime_object = datetime.datetime.now()
		FileHandle.write (str(datetime_object))
		FileHandle.write ("\n")
		FileHandle.close()
	else:
		print ("error opening output file " + Filename)
		
#----------------------------------------------------------------------------------------------------
def protocolResult (Question, QuestionNr, NumQuestions, Answer, answer_index, Filename):

	FileHandle = open (Filename, "a")
	
	if (FileHandle):
		try:
			FileHandle.write ("-----------------------------------------\n")
			FileHandle.write ("Frage " + str(QuestionNr) + " von " + str(NumQuestions) + "\n")
			FileHandle.write (Question.question + "\n")
			FileHandle.write ("korrekt: " + Question.answer_options[answer_index] + "\n")
		except Exception as e:
			print (str (e))
		
		if ((Answer > 0) and (Answer < 4)): 
			if (Answer != answer_index):
				try:
					FileHandle.write ("falsch: " + Question.answer_options[Answer] + "\n")
				except Exception as e:
					print (str (e))
		else:
			try:
				FileHandle.write ("timeout\n")
			except Exception as e:
				print (str (e))
		try:
			FileHandle.write ("\n")
			FileHandle.close()
		except Exception as e:
			print (str (e))
	else:
		print ("error opening output file " + Filename)
		


#---------------------------------start-working-------------------------

Options = ["a","b","c","d","?"]
AnimCorrect = ["BuildPyramidSuccess", "CodeLabAmazed", "CodeLabCelebrate", "CodeLabExcited", "CodeLabHappy", "CodeLabWhee1", "CodeLabYes"]
AnimWrong   = ["CantHandleTallStack", "CodeLabBored", "CodeLabDejected", "CodeLabLose", "CodeLabThinking", "CodeLabUnhappy", "CodeLabWondering", "GoToSleepGetIn"]

ProtocolName = "pepperQuizProtocol.txt"  # todo: Mit Parameter einstellbar
ProtocolHandle = None

# players = []
# for i in range (3):
	# players.append (CPlayer())
# print (players)

parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, default="127.0.0.1",
					help="Robot IP address.")
parser.add_argument("--port", type=int, default=9559,
					help="Robot port address. ")
parser.add_argument("-t", "--timeout", type=int, default=60,
					help="timeout in seconds, default = 60, ")
parser.add_argument("-q", "--quiz", type=str, default="quiz.json",
					help="json file with quiz questions. Default: quiz.json")
parser.add_argument("-m", "--max", type=int, default="1000",
					help="maximal number of questions to be asked")
parser.add_argument("-a", "--animate", type=int, default="1",
					help="0...pronounce nothing, 1..pronounce questions, 2...pronounce answer options, 3...both")

args = parser.parse_args()



# if (len(sys.argv) > 1):
	# DataFileName = sys.argv[1]
# else:
	# DataFileName = "quiz_questions.json"
# print ("opening file " + DataFileName)

DataFileName = args.quiz
print ("opening file " + DataFileName)
try:
	with open(DataFileName) as data_file:
		data = json.load(data_file)
except Exception as e:
	print (str(e))
	sys.exit()

questions = []
for quiz_question_json in data:
	question = quiz_question_json["question"]
	answer_options = quiz_question_json["answer_options"]
	if "info" in quiz_question_json:
		info = quiz_question_json["info"]
	else:
		info = ""
	questions.append(QuizQuestion(question, answer_options, info))
	
NumQuestions = len(questions)
Evaluate = False
Status = "NEXT_QUESTION"
print (str(NumQuestions) + " questions")
	
prepareProtocol (ProtocolName)


answer_index = 0
QuestionNr = 0



question = get_next_question()
NumCorrect = 0

setupJavascript(args.ip, args.port, args.animate, args.timeout)

if (introduction (args.animate) == 1000):
	sys.exit()

while True:			# all questions
	QuestionNr =  QuestionNr + 1
	print ("question " + str(QuestionNr))
	
	# clearGuesses()
	TimeRemaining = args.timeout # Brauchen wir das ueberhaupt?

	Answer = askQuestion(question, QuestionNr, args.animate)
	print ("got answer " + str(Answer))
	
	if (Answer == answer_index): 
		Correct = True
		NumCorrect = NumCorrect + 1
	else: 
		Correct = False
	
	protocolResult (question, QuestionNr, min(NumQuestions, args.max), Answer, answer_index, ProtocolName)
	showResult (question, QuestionNr, min(NumQuestions, args.max), Answer, answer_index, args.animate) 
	

	print ("QuestionNr=" + str(QuestionNr) + " args.max=" + str(args.max))
	
	question = get_next_question()
	if ((question == None) or (QuestionNr >= args.max)): 
		break
		
print ("finished!")
finish(NumCorrect, QuestionNr, args.animate)

#endJavascript()


