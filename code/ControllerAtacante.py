#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots
import math
import random

class RobotControllerAtacanteI(drobots.ControllerAtacante):
	def __init__(self):
		self.robot = None
		self.robotControllerContainer = None
		self.amigos = dict()
		self.location = 0
		self.energia = 100
		self.angulo = -1
		self.angulosAmigos = []
		self.angulosEnemigos = []
		self.velocidad = 0
		self.contadorTurno = 0
	
	def setRobot(self,robot, jugador, robotControllerContainer, current = None):
		self.robot = robot
		self.jugador = jugador
		self.robotControllerContainer = robotControllerContainer
		
	def turn(self, current = None): 
		print("Turno Atacante")
		print(self.contadorTurno)
		self.energia = 100

		self.minas = self.getMinas()

		self.amigos = self.getAmigos()

		self.location = self.robot.location()
		print("Posicion Robot - "+str(self.location.x)+","+str(self.location.y))
		self.energia -= 1
		
		self.angulosAmigos = self.getAngulosAmigos()
		print("Angulos Amigos")
		print(self.angulosAmigos)

		self.angulosEnemigos = self.getAngulosEnemigos()
		print("Angulos Enemigos")
		print(self.angulosEnemigos)

		self.angulo = self.selectAngulo()

		self.comprobarMinas()
		self.accion()

		self.contadorTurno += 1

	def getMinas(self, current = None):
        print("Obtener Minas")
        minas = dict()
        lista = self.robotControllerContainer.listMinas()
        for i in range(0, len(lista)):
            keys = lista.keys()[i]
            values = lista.values()[i]
            if(self.jugador) in keys:
                minas[keys] = values

        return minas

    def comprobarMinas(self, current = None):
    	print("Comprobando posicion minas")
    	for mina in self.minas.values():
    		for i in range(4,8):
	    		if(mina.x + i == self.location.x or mina.y + i == self.location):
	    			if(mina.x - i == self.location.x or mina.y - i == self.location):
			    		print("Mina en la ruta del robot")
			    		self.robot.drive(random.randint(0,360),100)


	def selectAngulo(self, current = None):
		for anguloEnemigo in self.angulosEnemigos:
			for angulo in self.angulosAmigos:
				if(angulo < anguloEnemigo + 10 and angulo > anguloEnemigo - 10):
					angulo = -1
				else:
					angulo = anguloEnemigo
		return angulo
				
	def accion(self, current = None):
		print("ACCION ATACANTE")
		if(self.energia > 50 and self.angulo > -1):
            distancia = random.randint(1,10)*100
            self.disparar(self.angulo, distancia)
            self.energia -= 50

		if(self.energia > 60):
			self.moverRobot(self.location)
			self.energia -= 60
        
	def moverRobot(self, current = None):
		print("Mover")
		if(self.contadorTurno == 0):
			self.robot.drive(random.randint(0,360),100)
			self.velocidad = 100
		elif(self.location.x > 390):
			self.robot.drive(225, 100)
			self.velocidad = 100
		elif(self.location.x < 100):
			self.robot.drive(45, 100)
			self.velocidad = 100
		elif(self.location.y > 390):
			self.robot.drive(315, 100)
			self.velocidad = 100
		elif(self.location.y < 100):
			self.robot.drive(135, 100)
			self.velocidad = 100


	def getAmigos(self, current = None):
		print("Obteniendo Amigos")
		amigos = dict()
		lista = self.robotControllerContainer.listController()
		for i in range(0, len(lista)):
			keys = lista.keys()[i]
			values = lista.values()[i]
			if(self.jugador) in keys:
				amigos[keys] = values

		return amigos

	def getAngulosAmigos(self, current = None):
		print("Obteniendo los angulos Amigos")
		angulosAmigos=[]
		for keys in self.amigos.keys():
			if("atac") in keys:
				atacante = drobots.ControllerAtacantePrx.checkedCast(self.amigos[keys])
				coordenadas = atacante.getPosicionAmiga()

				angulo = self.calcularAngulo(coordenadas.x, coordenadas.y)

				angulosAmigos.append(angulo)

			elif("def") in keys:
				defensor = drobots.ControllerDefensorPrx.checkedCast(self.amigos[keys])
				coordenadas = defensor.getPosicionAmiga()

				angulo = self.calcularAngulo(coordenadas.x, coordenadas.y)

				angulosAmigos.append(angulo)

			elif("compl") in keys:
				completo = drobots.ControllerCompletoPrx.checkedCast(self.amigos[keys])
				coordenadas = completo.getPosicionAmiga()
				
				angulo = self.calcularAngulo(coordenadas.x, coordenadas.y)
				
				angulosAmigos.append(angulo)

		return angulosAmigos

	def getAngulosEnemigos(self, current = None):
		print("Obteniendo las coordenadas Enemigas")
		angulosEnemigos=[]
		for keys in self.amigos.keys():
			if("def") in keys:
				defensor = drobots.ControllerDefensorPrx.checkedCast(self.amigos[keys])
				
				coordenadaXEnemigo = defensor.getCoordenadaEnemigoX()
				coordenadaYEnemigo = defensor.getCoordenadaEnemigoY()

				angulo = self.calcularAngulo(coordenadaXEnemigo, coordenadaYEnemigo)

				angulosEnemigos.append(angulo)

			if("compl") in keys:
				completo = drobots.ControllerCompletoPrx.checkedCast(self.amigos[keys])
				
				coordenadaXEnemigo = completo.getCoordenadaEnemigoX()
				coordenadaYEnemigo = completo.getCoordenadaEnemigoY()

				angulo = self.calcularAngulo(coordenadaXEnemigo, coordenadaYEnemigo)

				angulosEnemigos.append(angulo)

			if("detector") in keys:
				detector = drobots.ControllerDetectorPrx.checkedCast(self.amigos[keys])
				
				posicion = detector.getEnemigo()

				angulo = self.calcularAngulo(posicion.x, posicion.y)

				angulosEnemigos.append(angulo)

		return angulosEnemigos

	def disparar(self, angulo, distancia, current = None):
		print("Disparando: grados - "+str(angulo)+" distancia - "+str(distancia))
        self.robot.cannon(angulo, distancia)
        self.angulo = -1

	def calcularAngulo(self, coordenadaX, coordenadaY, current = None):
		puntoX = math.fabs(coordenadaX - self.location.x)
		puntoY = math.fabs(coordenadaY - self.location.y)
		angulo = int(math.degrees(math.atan2(puntoY,puntoX)))
		if(angulo < 0):
			angulo = angulo + 360
		elif(angulo >= 360):
			angulo = 0
		return angulo

	def getPosicionAmiga(self, current = None):
		location = self.robot.location()
		return location

	def robotDestroyed(self, current = None):
		print("Robot Destruido")