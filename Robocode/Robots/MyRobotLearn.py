import math
import socket

from robot import Robot


class MyRobotLearn(Robot):

	global client_socket

	host = "localhost"  # as both code is running on same pc
	port = 1000  # socket server port number

	client_socket = socket.socket()  # instantiate
	try:
		client_socket.connect((host, port))  # connect to the server
	except Exception as e:
		print("Cannot connect to the server:", e)

	def init(self):

		# Set the bot color in RGB
		self.setColor(200, 200, 100)
		self.setGunColor(200, 200, 0)
		self.setRadarColor(255, 60, 0)
		self.setBulletsColor(0, 200, 100)

		# get the map size
		size = self.getMapSize()  # get the map size
		self.radarVisible(True)  # show the radarField

		self.lockRadar("gun")
		self.setRadarField("round")

		self.enemies = {}

	def run(self):  # NECESARY FOR THE GAME  main loop to command the bot
		self.setRadarField("large")
		
		self.gunTurn(100)
		self.turn(90)
		self.move(90)
		self.gunTurn(100)
		self.turn(-90)
		self.move(90)
		self.gunTurn(100)
		self.move(-90)
		self.turn(90)
		self.move(90)
		self.move(-90)
		self.turn(90)
		self.stop()

	def sensors(self):  # NECESARY FOR THE GAME
		pass


	def onHitByRobot(self, robotId, robotName):
		pass

	def onRobotHit(self, robotId, robotName):
		pass

	def onHitWall(self):
		pass

	def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower):  # NECESARY FOR THE GAME
		pass

	def onBulletHit(self, botId, bulletId):  # NECESARY FOR THE GAME
		pass

	def onBulletMiss(self, bulletId):
		pass

	def onRobotDeath(self):  # NECESARY FOR THE GAME
		pass

	def onTargetSpotted(self, botId, botName, botPos):  # NECESARY FOR THE GAME

		if botId not in self.enemies:
			self.enemies[botId] = {}
			self.enemies[botId]["x"] = botPos.x()
			self.enemies[botId]["y"] = botPos.y()
			self.enemies[botId]["velx"] = 0
			self.enemies[botId]["vely"] = 0
			self.enemies[botId]["lastX"] = botPos.x()
			self.enemies[botId]["lastY"] = botPos.y()
		else:
			# Velocity calculation
			velx = self.enemies[botId]["x"] - self.enemies[botId]["lastX"] 
			vely = self.enemies[botId]["y"] - self.enemies[botId]["lastY"] 
			# If enemy did not move more than 10 units
			if abs(velx) > 10 or abs(vely) > 10:
				# Update of velocity
				self.enemies[botId]["velx"] = 0
				self.enemies[botId]["vely"] = 0
			else:
				self.enemies[botId]["velx"] = velx
				self.enemies[botId]["vely"] = vely
				
			self.enemies[botId]["lastX"] = self.enemies[botId]["x"] 
			self.enemies[botId]["lastY"] = self.enemies[botId]["y"] 
			self.enemies[botId]["x"] = botPos.x()
			self.enemies[botId]["y"] = botPos.y()

		pos = self.getPosition()
		dx = botPos.x() - pos.x()
		dy = botPos.y() - pos.y()

		my_gun_angle = self.getGunHeading() % 360

		sendData = ";".join([f'{x:.2f}' for x in [dx, dy, my_gun_angle, self.enemies[botId]["velx"], self.enemies[botId]["vely"]]])
		client_socket.send(sendData.encode())

		data = client_socket.recv(1024).decode()

		if data == "shoot\n":
			self.fire(1)
		elif data == "do not shoot\n":
			return
