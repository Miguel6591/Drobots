#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

# COMPONENTES DEL GRUPO: ALBERTO LOPEZ HURTADO Y MIGUEL RODRIGUEZ LORENTE
# GRUPO DE PRACTICAS: B2

import sys
import Ice
import random
import math

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots

class Cliente(Ice.Application):
    def run(self, argv):   
        jugador = "P" + str(random.randint(0,999))+"LAYR"
        print("Jugador: " + jugador)
        broker = self.communicator()

        proxyContainer = broker.stringToProxy("container")
        container = drobots.ContainerPrx.checkedCast(proxyContainer)
        
        adapter = broker.createObjectAdapter("PlayerAdapter")
        servantPlayer = PlayerI(jugador,container)
        proxyPlayer = adapter.addWithUUID(servantPlayer)
        directProxyPlayer = adapter.createDirectProxy(proxyPlayer.ice_getIdentity())
        player = drobots.PlayerPrx.uncheckedCast(directProxyPlayer)

        adapter.activate()

        # Se usa drobots
        proxyGame = broker.propertyToProxy("Cliente")
        game = drobots.GamePrx.checkedCast(proxyGame)
        
        # Se usa la factoria de juego
        #proxyGame = broker.propertyToProxy("Factoria")
        #gameFactory = drobots.GameFactoryPrx.checkedCast(proxyGame)
        #game = gameFactory.makeGame("nombre210", 2)

        try:
            print('Haciendo login')
            game.login(player, jugador)
            print('Esperando robots')
        except drobots.GameInProgress:
            print("Partida en curso.")
        except drobots.InvalidProxy:
            print("Proxy inválido")
        except drobots.InvalidName as e:
            print("Nombre inválido")
            print(str(e.reason))
        except drobots.BadNumberOfPlayers:
            print("Número de jugadores no válidos")

        self.shutdownOnInterrupt()
        broker.waitForShutdown()
 
        return 0

class PlayerI(drobots.Player):
    def __init__(self, jugador, container):
        self.jugador = jugador
        self.container = container
        self.contador = 0
        self.contadorDetectores = 0
        self.contadorMinas = 0
        
    def makeController(self, robot, current=None):
        print("Make Controller, indice: " +str(self.contador))
        lista = self.container.listFactorias()

        if(robot.ice_ids() == ['::Ice::Object', '::drobots::Attacker', '::drobots::RobotBase']):
            print("Robot Atacante, usando la factoria: " + str(self.contador))
            factoria = drobots.ControllerFactoryPrx.checkedCast(lista.values()[self.contador])
            controller = factoria.make(robot, "atac", self.jugador, self.container, self.contador)
            self.contador = self.contador + 1
            print("Controller de Atacante: "+str(controller))

        elif(robot.ice_ids() == ['::Ice::Object', '::drobots::Attacker', '::drobots::Defender', '::drobots::Robot', '::drobots::RobotBase']):
            print("Robot Completo, usando la factoria: " + str(self.contador))
            factoria = drobots.ControllerFactoryPrx.checkedCast(lista.values()[self.contador])
            controller = factoria.make(robot, "compl", self.jugador, self.container, self.contador)
            self.contador = self.contador + 1
            print("Controller de Completo: "+str(controller))

        elif(robot.ice_ids() == ['::Ice::Object', '::drobots::Defender', '::drobots::RobotBase']):
            print("Robot Defensor, usando la factoria: " + str(self.contador))
            factoria = drobots.ControllerFactoryPrx.checkedCast(lista.values()[self.contador])
            controller = factoria.make(robot, "def", self.jugador, self.container, self.contador)
            self.contador = self.contador + 1
            print("Controller de Defensor: "+str(controller))

        return controller

    def makeDetectorController(self, current=None):
        print("Make Controller del Detector")
        print("Indice 1: " +str(self.contadorDetectores))
        print("Detector, usando la factoria: " + str(self.contadorDetectores))
        factoria = drobots.ControllerFactoryPrx.checkedCast(self.container.listFactorias().values()[self.contadorDetectores])
        controller = factoria.makeDetector("detector", self.jugador, self.container, self.contadorDetectores)
        self.contadorDetectores = self.contadorDetectores + 1
        print("Indice 2: " +str(self.contadorDetectores))
        print("ControllerDetector: "+str(controller))
        return controller

    def lose(self, current=None):
        print("You lose :-(")
        current.adapter.getCommunicator().shutdown()

    def win(self, current=None):
        print("You win")
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print("The game was aborted")
        current.adapter.getCommunicator().shutdown()

    def getMinePosition(self, current):
        x = random.randint(0,399)
        y = random.randint(0,399)
        mina = drobots.Point(x=x, y=y)
        clave = "Mina"+"-"+str(self.contadorMinas)+"-"+self.jugador
        self.container.linkMinas(clave,mina)
        self.contadorMinas += 1
        return mina
    
sys.exit(Cliente().main(sys.argv))
