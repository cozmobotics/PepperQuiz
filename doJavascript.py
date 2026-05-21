# routines for the quiz on pepper's tablet 

import time
import qi
import sys
from naoqi import ALProxy
from animationMartin import sayTextWithEmotion
from animationMartin import initEmotion

EventGlob = ""
tabletService = ""

# Don't forget to disconnect the signal at the end
signalID = 0

#----------------------------------------------------------------------------------
style = """
document.clear ();
document.writeln ('<style> ');
document.writeln ('.button { ');
document.writeln ('  color: white; ');
document.writeln ('  padding: 10px 20px; ');
document.writeln ('  text-align: center; ');
document.writeln ('  text-decoration: none; ');
document.writeln ('  display: inline-block; ');
document.writeln ('  font-size: 15px; ');
document.writeln ('  border-radius: 10px; ');
document.writeln ('  margin: 4px 2px; ');
document.writeln ('  cursor: pointer; ');
document.writeln ('  background-color: #006599 /* TU-blau */ ');
document.writeln ('} ');
document.writeln ('.button1 { font-size: 10px; } ');
document.writeln ('.button2 { font-size: 25px; } ');
document.writeln ('</style> ');
"""

# call like "<button style=button button2 onclick=..."


#----------------------------------------------------------------------------------
def introduction (Animate):
	global tabletService
	global EventGlob	
	global session	# this is essential! Without this statement I get "Error 1 was:  Socket is not connected"
	
	global Ip
	global Port
	global Timeout


	script = """
		var Name="";
		function myFunctionIntro()
		{
			//document.write("Button 1 clicked  ");
			Name = "0";
			ALTabletBinding.raiseEvent(Name);
		}
		
		document.clear();
		document.write ("<font size=+2>");
		document.write("<h1>Hallo!</h1><b>Machen wir ein Quiz!</b><br><br>") 
		document.write('<button class=button onclick="myFunctionIntro()">OK</button><br><br>');
		document.write ("</font>");
		"""

	# print (script)
	
	EventGlob = "1000"

	tabletService.hideWebview()
	time.sleep(0.5)
	tabletService.showWebview("") # this necessary for clearing the screen. cleanWebview() and document.clear() don't do the job. 

	try:
		tabletService.executeJS(style + script)
	except Exception as e:
		print ("Error 1 was: ", e)

	if (Animate):
		sayTextWithEmotion (Ip, Port, "neutral", "Hallo! Machen wir ein Quiz!")	# don't know why I need str() here. 

	TimeRemaining = 10 * Timeout
	while (('1000' in EventGlob) and (TimeRemaining > 0)):
		TimeRemaining = TimeRemaining - 1
		time.sleep(1)
		
	tabletService.hideWebview() # this necessary for clearing the screen. cleanWebview() and document.clear() don't do the job. 

	return (int(EventGlob))

#----------------------------------------------------------------------------------
def askQuestion (Question, Nr, Animate):
	global tabletService
	global EventGlob	
	global session	# this is essential! Without this statement I get "Error 1 was:  Socket is not connected"
	
	global Ip
	global Port

	print (str(Question.question))
	print (str(Question.answer_options[0]))


	script = """
		var Name="";
		function myFunction1()
		{
			//document.write("Button 1 clicked  ");
			Name = "0";
			ALTabletBinding.raiseEvent(Name);
		}
		function myFunction2()
		{
			//document.write("Button 2 clicked  ");
			Name = "1";
			ALTabletBinding.raiseEvent(Name);
		}
		
		function myFunction3()
		{
			//document.write("Button 3 clicked  ");
			Name = "2";
			ALTabletBinding.raiseEvent(Name);
		}
		
		function myFunction4()
		{
			//document.write("Button 4 clicked  ");
			Name = "3";
			ALTabletBinding.raiseEvent(Name);
		}
		
		function myFunction100()
		{
			//document.write("Button 4 clicked  ");
			Name = "100";
			ALTabletBinding.raiseEvent(Name);
		}
		
		document.clear();
		document.write ("<font size=+1>");
		document.write("<h1>Frage """ + str(Nr) + """</h1>""" + \
		"""<b>""" + Question.question + """</b><br><br>""" + \
		"""<button class=button onclick=myFunction1()>a</button> """+ Question.answer_options[0] + """<br><br>""" + \
		"""<button class=button onclick=myFunction2()>b</button> """+ Question.answer_options[1] + """<br><br>""" + \
		"""<button class=button onclick=myFunction3()>c</button> """+ Question.answer_options[2] + """<br><br>""" + \
		"""<button class=button onclick=myFunction4()>d</button> """+ Question.answer_options[3] + """<br><br>""" + \
		"""<button class=button onclick=myFunction100()>?</button> Ich weiss es nicht <br><br>""" + \
		"""");
		document.write ("</font>");
		"""

	# print (script)
	
	EventGlob = "1000"

	tabletService.hideWebview()
	time.sleep(0.5)
	tabletService.showWebview("") # this necessary for clearing the screen. cleanWebview() and document.clear() don't do the job. 

	try:
		tabletService.executeJS(style + script)
	except Exception as e:
		print ("Error 1 was: ", e)

	if (Animate & 1):
		sayTextWithEmotion (Ip, Port, "neutral", str(Question.question))	# don't know why I need str() here. 
		
		# read quiz answer options
	if (Animate & 2):
		for count in range (4):
			time.sleep (1)
			letter = chr (ord('a') + count) + ": "
			sayTextWithEmotion (Ip, Port, "neutral", str(letter + Question.answer_options[count]))	# don't know why I need str() here. 
		 		

	TimeRemaining = Timeout
	while (('1000' in EventGlob) and (TimeRemaining > 0)):
		TimeRemaining = TimeRemaining - 1
		time.sleep(1)
	#tabletService.hideWebview() # this necessary for clearing the screen. cleanWebview() and document.clear() don't do the job. 

	return (int(EventGlob))

#----------------------------------------------------------------------------------------------------
def getColor(Index, Answer, answer_index):
	Color = "black"
	
	if (Index == answer_index): 
		Color = "green"
		
	if (Index == Answer) and (Answer != answer_index):
		Color = "red"
	
	return (Color)

#----------------------------------------------------------------------------------------------------
def showResult (Question, QuestionNr, NumQuestions, Answer, answer_index, Animate):
	global tabletService
	global EventGlob	
	global Ip
	global Port

	if (Answer == 1000):
		Heading = "Das hat mir zu lange gedauert."
		Mood = "neg"
	elif (Answer == 100):
		Heading = "Danke fuer deine Ehrlichkeit!"
		Mood = "neutral"
	else:
		if (Answer == answer_index):
			Heading = "Das ist richtig!"
			Mood = "pos"
			# info = ""  # when you know it, I do not need to tell you
		else:
			# Heading = "Das ist leider falsch!"
			Heading = "Jetzt kannst du etwas Neues lernen!"
			Mood = "neutral"
			

	script = """
		document.write ("<font size=+2>");
		var Name="";
		function myFunction5()
		{
			//document.write("Button OK clicked  ");
			Name = "100";
			ALTabletBinding.raiseEvent(Name);
		}
		
		document.clear();
		document.write("<h1>Frage """ + str(QuestionNr) + """ von """ + str(NumQuestions) + """</h1>""" + \
		Heading + """ <br><br> """ + \
		"""<b>""" + Question.question + """</b><br><br>""" + \
		"""<font color = """ + getColor(0, Answer, answer_index) + """> a) """+ Question.answer_options[0] + """</font><br>""" + \
		"""<font color = """ + getColor(1, Answer, answer_index) + """> b) """+ Question.answer_options[1] + """</font><br>""" + \
		"""<font color = """ + getColor(2, Answer, answer_index) + """> c) """+ Question.answer_options[2] + """</font><br>""" + \
		"""<font color = """ + getColor(3, Answer, answer_index) + """> d) """+ Question.answer_options[3] + """</font><br>""" + \
		"<br>" + Question.info + "<br>" + \
		"""<button class=button onclick=myFunction5()>OK</button> <br><br>""" + \
		"""");
		document.write ("</font>");
		"""

	# print (script)

	EventGlob = "1000"

	# try:
		# tabletService.cleanWebview()
	# except Exception, e:
		# print "Error 0 was: ", e

	tabletService.hideWebview()
	time.sleep(0.5)
	tabletService.showWebview("")


	try:
		tabletService.executeJS(style + script)
	except Exception as e:
		print ("Error 2 was: ", e)

	if (Animate):
		# Mood = "neutral"                                     #### UnboundLocalError: local variable 'Mood' referenced before assignment
		
		sayTextWithEmotion (Ip, Port, Mood, Heading)
		if (Animate & 2):
			sayTextWithEmotion (Ip, Port, "pos", str(Question.question))
			sayTextWithEmotion (Ip, Port, "pos", str(Question.answer_options[answer_index]))
		
		if Question.info != "":
			sayTextWithEmotion (Ip, Port, Mood, str(Question.info))

	TimeRemaining = Timeout
	while (('1000' in EventGlob) and (TimeRemaining > 0)):
		TimeRemaining = TimeRemaining - 1
		time.sleep(1)
		
	return (EventGlob)


#----------------------------------------------------------------------------------------------------
def callback(event):
	global EventGlob
	EventGlob = event
	print ("Event: <<", EventGlob, ">>")

#----------------------------------------------------------------------------------------------------
def setupJavascript(ip, port, Animate, timeout):
	global tabletService
	global session
	global Ip
	global Port
	global signalID
	global Timeout

	Ip = ip 	#	for passing to sayTextWithEmotion
	Port = port
	Timeout = timeout
		
	session = qi.Session()
	try:
		session.connect("tcp://" + ip + ":" + str(port))
	except RuntimeError:
		print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + str(port) +".\n"
			   "Please check your script arguments. Run with -h option for help.")
		sys.exit(1)

	if (Animate):
		initEmotion (ip, port, session)
		
	try:
		# Get the service ALTabletService.
		tabletService = session.service("ALTabletService")
	except Exception as e:
		print ("Error 3 was: ", e)

	try:
		# Display a local web page located in boot-config/html folder
		# The ip of the robot from the tablet is 198.18.0.1
		# tabletService.showWebview("http://198.18.0.1/apps/boot-config/preloading_dialog.html")
		tabletService.showWebview("")
	except Exception as e:
		print ("Error 4 was: ", e)

		time.sleep(3)

	try:
		# attach the callback function to onJSEvent signal
		signalID = tabletService.onJSEvent.connect(callback)
	except Exception as e:
		print ("Error 6 was: ", e)

#-------------------------------------------------------------------------------------------------
def finish (NumCorrect, NumTotal, Animate):
	global EventGlob
	
	greeting = "Ich hoffe, es war interessant und hat Spa&szlig; gemacht. Danke f&uuml;r's Mitmachen"
	EventGlob = "1000"

	tabletService.hideWebview()
	time.sleep(0.5)
	tabletService.showWebview("")

	
	script = """
		document.clear();
		document.write ("<font size=+3>");
		document.write("<h1>Fertig! </h1>");
		"""
	
	try:
		tabletService.executeJS(script)
	except Exception as e:
		print ("Error 8 was: ", e)

	if (Animate):
		sayTextWithEmotion (Ip, Port, "pos", "Fertig!")
		
		
	time.sleep (2)

	script = """
		var Name="";
		function myFunction6()
		{
			//document.write("Button OK clicked  ");
			Name = "100";
			ALTabletBinding.raiseEvent(Name);
		}
		
		document.write("<br>""" + \
		"""<b>""" + str(NumCorrect) + """ Fragen von """  + str(NumTotal) + """ richtig! </b><br><br>""" + \
		"""<b>""" + str(NumTotal - NumCorrect) + """ mal etwas Neues gelernt! </b><br><br>""" + \
		"""<button class=button onclick=myFunction6()>OK</button> <br><br>""" + \
		"""");
		document.write ("</font>");
		"""

	EventGlob = "1000"

	try:
		tabletService.executeJS(style + script)
	except Exception as e:
		print ("Error 8 was: ", e)

		
	if (Animate):
		if (NumCorrect >= (NumTotal / 2)):
			Mood = "pos"
		else:
			Mood = "neg"
		
		sayTextWithEmotion (Ip, Port, Mood, str(NumCorrect) + " Fragen von " + str(NumTotal) + " richtig!")
		sayTextWithEmotion (Ip, Port, Mood, str(NumTotal - NumCorrect) + " mal etwas Neues gelernt!")
		
		
	TimeRemaining = Timeout
	while (('1000' in EventGlob) and (TimeRemaining > 0)):
		TimeRemaining = TimeRemaining - 1
		time.sleep(1)

	sayTextWithEmotion (Ip, Port, "bye", greeting)
	tabletService.hideWebview()
	
	if (Animate):
		postureService = ALProxy("ALRobotPosture", Ip, Port)
		postureService.goToPosture("StandInit", 0.5)
		
#-------------------------------------------------------------------------------------------------
def endJavascript():
	global tabletService
	global signalID


	try:
		tabletService.onJSEvent.disconnect(signalID)
	except Exception as e:
		print ("Error 7 was: ", e)

