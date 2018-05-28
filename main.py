import qi
import time
import sys

import Queue
import socket
import requests
from threading import Thread

import math



class Winston(object):
	def __init__(self, app):
		app.start()
		self.session = app.session
		self.reacting = False
		self.ppService = self.session.service("ALPeoplePerception")
		self.gazeAnalysisService = self.session.service("ALGazeAnalysis")
		self.wavingDetection = self.session.service("ALWavingDetection")
		self.tts = self.session.service("ALTextToSpeech")
		self.memory = self.session.service("ALMemory")
		self.navigationService = self.session.service("ALNavigation")
		self.motionService = self.session.service("ALMotion")
		self.tabletService = self.session.service("ALTabletService")
		self.engagementZoneService = self.session.service("ALEngagementZones")
		self.runApp = True
		self.tableCallQueue = Queue.Queue()

		print "start localization"
		self.motionService.wakeUp()
		self.navigationService.stopLocalization()
		exploration_file = '/home/nao/.local/share/Explorer/2018-05-19T154733.970Z.explo'
		self.navigationService.loadExploration(exploration_file)
		guess = [0., 0.]
		self.navigationService.relocalizeInMap(guess)
		self.navigationService.startLocalization()

		
		self.gazeAnalysisService.setFaceAnalysisEnabled(True)

		self.subscriber2 = self.memory.subscriber("EngagementZones/PersonMovedAway")
		self.subscriber2.signal.connect(self.onEnteredZone1)

		self.engagementZoneService.subscribe("Winston")

	def onEnteredZone1(self, id):
		posWorld =  self.memory.getData("PeoplePerception/Person/"+str(id)+"/PositionInWorldFrame", 1)
		posTorso =  self.memory.getData("PeoplePerception/Person/"+str(id)+"/PositionInTorsoFrame", 1)
		posRobot =  self.memory.getData("PeoplePerception/Person/"+str(id)+"/PositionInRobotFrame", 1)

		if posWorld[0] > 8.9:
			self.tts.say("Goodbye")
		elif posWorld[0] < 8.8:
			self.tts.say("Hello dear customer")


		print posWorld, posRobot, posTorso 

	def handleCall(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(None) 
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			s.bind(('0.0.0.0', 10000))
			s.listen(1)
			while self.runApp:
				time.sleep(0.5)
				print "wait for connection"
				conn, addr = s.accept()

				print 'Connection address:', addr
				
				tableNr = conn.recv(1)
				print tableNr
				conn.close()
				if tableNr == 3:
					self.runApp = False
				else:
					self.tableCallQueue.put(tableNr)

				
		except socket.error as msg:

			print "error"
			print  str(msg)
		
	def goToTable(self, tableId):
		
		#get table position
		r = requests.get("http://192.168.1.104:8080/position/" + str(tableId) + "/json")
		tablePos = r.json()

		xPos = tablePos[0]['x']
		yPos = tablePos[0]['y']
		orientationCor = tablePos[0]['orientation']

		print "going to table " + str(tableId) + " at " + str(xPos) + ", " + str(yPos)

		self.navigationService.navigateToInMap([xPos, yPos, 0.])
		curPos = self.navigationService.getRobotPositionInMap()[0]
		print "I reached: " + str(curPos)

		cur_orientation = curPos[2]

		if cur_orientation > math.pi:
			cur_orientation = -math.pi + ( curPos[2]- math.pi)
	
		self.motionService.moveTo(0,0, -math.pi/2 - cur_orientation  )

		self.showMenuCart(tableId)
		print "going back"
		self.goBackToStartPoint()
		pass

	def showMenuCart(self, tableId):
		try:
			# Ensure that the tablet wifi is enabled
			self.tabletService.enableWifi()

			# Display webpage where menu is
			self.tabletService.loadUrl("http://192.168.1.104:8080/position/"+str(tableId))
			self.tabletService.showWebview()

			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket.setdefaulttimeout(None)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind(('0.0.0.0', 5000))
			s.listen(1)
			conn, addr = s.accept()
			status = conn.recv(1)
			conn.close()
			print str(status)
			if str(status) == '1':
				self.tts.say("Thank you for your order")
			else:
				self.tts.say("Something went wrong. Someone will be here in second")

			# Hide the web view
			self.tabletService.hideWebview()
		except Exception, e:
			print "Error showing menu: ", e		
		pass
		
	def goBackToStartPoint(self):
		self.navigationService.navigateToInMap([0., 0., 0.])
		curPos = self.navigationService.getRobotPositionInMap()[0]
		self.motionService.moveTo(0,0, -curPos[2])
		print "I reached: " + str(self.navigationService.getRobotPositionInMap()[0])


	def run(self):
		t = Thread(target=self.handleCall)
		t.start()
		while self.runApp:
			tableNr = self.tableCallQueue.get()
			print "handling table call"
			if tableNr != 3:
				self.goToTable(tableNr)

			time.sleep(1)
		self.navigationService.stopLocalization()
		t.join()
		print "finished everything."
		time.sleep(2)
		
		
if __name__ == "__main__":
	connection_url = "192.168.1.102:9559"
	try:
		app = qi.Application(["Example", "--qi-url="+connection_url])
	except RuntimeError:
		print("Cant connect to NAOqi")
		sys.exit(1)
	WinstonApp = Winston(app)
	WinstonApp.run()