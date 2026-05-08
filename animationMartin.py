#! /usr/bin/python
# -*- encoding: UTF-8 -*-

import qi
from naoqi import ALProxy
import random
import time

global Debug
Debug = 1
if (Debug):
	print "initialising Martins code"
AnimPos     = ['animations/Stand/Gestures/Yes_1','animations/Stand/Gestures/Yes_2','animations/Stand/Gestures/Yes_3',]
AnimNeg     = ['animations/Stand/Gestures/No_1', 'animations/Stand/Gestures/No_2', 'animations/Stand/Gestures/No_8',]
AnimBye     = ['animations/Stand/Gestures/Hey_1','animations/Stand/Gestures/Hey_3','animations/Stand/Gestures/Hey_4','animations/Stand/Gestures/Hey_6']
AnimNeutral = ['animations/Stand/Gestures/Explain_1']

animatedSpeech = None

#------------------------------------------------------------------
def umlaut (text):
	text = text.replace ("&auml;","ae")
	text = text.replace ("&ouml;","oe")
	text = text.replace ("&uuml;","ue")
	text = text.replace ("&Auml;","Ae")
	text = text.replace ("&Ouml;","Oe")
	text = text.replace ("&Uuml;","Ue")
	text = text.replace ("&szlig;","ss")
	text = text.replace ("<sup>2</sup>","Quadrat")
	return (text)



#------------------------------------------------------------------
def initEmotion (Ip, Port, MySession):
	global animatedSpeech

	# try:
		# MySession.connect("tcp://" + Ip + ":" + str(Port))
	# except RuntimeError:
		# print ("Can't connect to Naoqi at ip \"" + Ip + "\" on port " + str(Port) +".\n"
			   # "Please check your script arguments. Run with -h option for help.")
		# # sys.exit(1)


	
	try:
		animatedSpeech = ALProxy("ALAnimatedSpeech", Ip, Port)
	except:
		print ("cannot get ALProxy - ALAnimatedSpeech")

	tts = ALProxy("ALTextToSpeech", Ip, Port)
	tts.setLanguage("German")

	alMotion = ALProxy("ALMotion", Ip, Port)
	#alMotion = session.service("ALMotion")
	alMotion.wakeUp()


#-----------------sayTextWithEmotion-------------------------------------
def sayTextWithEmotion (Ip, Port, Mood, Text=""):
	"makes Pepper say some text and execute some movement according to mood. parameters: mood=pos/neg/neutral,bye[, text]"	
	global animatedSpeech
	
	Text = umlaut (Text)
		
	if (Mood == "pos"):
		Anim = AnimPos
	elif (Mood == "neg"):
		Anim = AnimNeg
	elif (Mood == "neutral"):
		Anim = AnimNeutral
	elif (Mood == "bye"):
		Anim = AnimBye
	else:		
		return ("Error: No valid mood given")
		
	Index = random.randint(0, (len(Anim)-1))
	AnimatedText = "^start(" + Anim[Index] + ")" + Text + "^wait(" + Anim[Index] + ")"
	#print (AnimatedText)
	
	ErrorText1 = ""
	ErrorText2 = ""
	MaxTries = 5	
	Tries = 0
	Fail = 1
	while ((Tries <= MaxTries) and (Fail == 1)):
		Tries = Tries + 1		
		Fail = 0		
		try:
			#animatedSpeech = ALProxy("ALAnimatedSpeech")
			animatedSpeech.say (AnimatedText)
		except BaseException, err:
		  ErrorText1 = str(err)		  
		  if (Debug):	  
		    print ("tried to say >>>" + AnimatedText + "<<<")	  
		    print str(err)
		  Fail = 1
		  time.sleep (0.5)
		  
	#set head horizontal again		
	Tries = 0
	Fail = 1
	while ((Tries <= MaxTries) and (Fail == 1)):
		Tries = Tries + 1		
		Fail = 0		
		try:
			motion = ALProxy("ALMotion", Ip, Port)
			motion.setAngles(["HeadPitch"], [0], 0.1)
		except BaseException, err:
		   ErrorText2 = str(err)			
		   if (Debug):	  
		   	print ("tried to set head horizontal again")
			Fail = 1
		  
	return (ErrorText1 + ErrorText2);
	