#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots
import math
import random

class RobotControllerDefensorI(drobots.ControllerDefensor):
	def __init__(self):
        self.robot = None
        self.robotControllerContainer = None
        self.amigos = dict()
        self.location = 0
        self.energia = 100
        self.angulo = -1
        self.amplitud = 20
        self.angulosAmigos = []
        self.velocidad = 0
        self.coordenadaXEnemigo = -1
        self.coordenadaYEnemigo = -1
        self.contadorTurno = 0
    
    def setRobot(self,robot, jugador, robotControllerContainer, current = None):
        self.robot = robot
        self.jugador = jugador
        self.robotControllerContainer = robotControllerContainer
        
    def turn(self, current = None):
        print("Turno Defensor")
        print(self.contadorTurno)  
        self.energia = 100

        self.amigos = self.getAmigos()

        self.minas = self.getMinas()

        self.location = self.robot.location()
        print("Posicion Robot - "+str(self.location.x)+","+str(self.location.y))
        self.energia -= 1

        self.angulosAmigos = self.getAngulosAmigos()
        print("Angulos Amigos")
        print(self.angulosAmigos)

        self.angulo = random.randint(0, 359)
        
        self.comprobarMinas()
        self.accion()

        self.contadorTurno += 1

    def getMinas(self, current = None):
        print("Obteniendo Minas")
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

    def accion(self, current = None):
        print("ACCION DEFENSOR")
        if(self.energia > 10):
            self.escanear(self.angulo, self.amplitud)

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

    def escanear(self, angulo, amplitud, current = None):
        print("Escaneando: grados - "+str(angulo)+" amplitud - "+str(amplitud))
        self.coordenadaXEnemigo = -1
        self.coordenadaYEnemigo = -1
        encontrados = self.robot.scan(angulo, amplitud)
        if(encontrados > 0):
            for anguloAmigo in self.angulosAmigos:
                if(angulo > anguloAmigo + 10 and angulo < anguloAmigo - 10):
                    print("Enemigo Encontrado")
                    coordenadaEnemigoX = int((self.location.x + math.cos(angulo) * random.randint(1,4)*100)%1000)
                    self.coordenadaXEnemigo = coordenadaEnemigoX
                    coordenadaEnemigoY = int((self.location.y + math.sin(angulo) * random.randint(1,4)*100)%1000)
                    self.coordenadaYEnemigo = coordenadaEnemigoY
                else:
                    print("Amigo Encontrado")
                    self.angulo = -1
                    self.coordenadaXEnemigo = -1
                    self.coordenadaYEnemigo = -1
                    
            
    def getCoordenadaEnemigoX(self, current = None):
        coordenadaX = self.coordenadaXEnemigo
        return coordenadaX

    def getCoordenadaEnemigoY(self, current = None):
        coordenadaY = self.coordenadaYEnemigo
        return coordenadaY

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

                angulo = self.calcularAngulo(coordenadas)

                angulosAmigos.append(angulo)

            elif("def") in keys:
                defensor = drobots.ControllerDefensorPrx.checkedCast(self.amigos[keys])
                coordenadas = defensor.getPosicionAmiga()
                
                angulo = self.calcularAngulo(coordenadas)

                angulosAmigos.append(angulo)

            elif("compl") in keys:
                completo = drobots.ControllerCompletoPrx.checkedCast(self.amigos[keys])
                coordenadas = completo.getPosicionAmiga()
                
                angulo = self.calcularAngulo(coordenadas)
                
                angulosAmigos.append(angulo)

        return angulosAmigos

    def calcularAngulo(self, coordenadas, current = None):
        puntoX = math.fabs(coordenadas.x - self.location.x)
        puntoY = math.fabs(coordenadas.y - self.location.y)
        angulo=int(math.degrees(math.atan2(puntoY,puntoX)))
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