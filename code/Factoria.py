#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice
import os

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots
import math
import random
import ControllerCompleto
import ControllerDefensor
import ControllerAtacante
import ControllerDetector

class FactoriaI(drobots.ControllerFactory):

	def make(self, robot, tipo, jugador, container, contador, current=None):
		print("Make Factoria")

		if(tipo == "def"):
			print("Defensor Factoria")
			servantController = ControllerDefensor.RobotControllerDefensorI()
			proxyController = current.adapter.addWithUUID(servantController)
			directProxyController = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
			controller = drobots.ControllerDefensorPrx.checkedCast(directProxyController)
			
			clave = tipo+"-"+str(contador)+"-"+jugador

			container.linkController(clave,controller)

			print(container.listController())
			print("container " + clave)

			controller.setRobot(robot, jugador, container)

		if(tipo == "atac"):
			print("Atacante Factoria")
			servantController = ControllerAtacante.RobotControllerAtacanteI()
			proxyController = current.adapter.addWithUUID(servantController)
			directProxyController = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
			controller = drobots.ControllerAtacantePrx.checkedCast(directProxyController)
			clave = tipo+"-"+str(contador)+"-"+jugador
			container.linkController(clave,controller)
			
			print(container.listController())
			print("container " + clave)

			controller.setRobot(robot, jugador,container)

		if(tipo == "compl"):
			print("Completo Factoria")
			servantController = ControllerCompleto.RobotControllerCompletoI()
			proxyController = current.adapter.addWithUUID(servantController)
			directProxyController = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
			controller = drobots.ControllerCompletoPrx.checkedCast(directProxyController)
			clave = tipo+"-"+str(contador)+"-"+jugador
			container.linkController(clave,controller)
			
			print(container.listController())
			print("container " + clave)

			controller.setRobot(robot, jugador,container)

		return controller

	def makeDetector(self, tipo, jugador, container, contador, current=None):
		print("Make Factoria")
		print("Detector Factoria")
		servantController = ControllerDetector.RobotControllerDetectorI()
		print("servantController "+str(servantController))
		proxyController = current.adapter.addWithUUID(servantController)
		print("proxyController "+str(proxyController))
		directProxyController = current.adapter.createDirectProxy(proxyController.ice_getIdentity())
		print("directProxyController "+str(directProxyController))
		controller = drobots.ControllerDetectorPrx.checkedCast(directProxyController)
		print("controller "+str(controller))
		clave = tipo+"-"+str(contador)+"-"+jugador
		print("clave "+str(clave))
		container.linkController(clave,controller)
			
		print(container.listController())
		print("container " + clave)

		return controller


class Server(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		servant = FactoriaI()

		adapter = broker.createObjectAdapter("FactoryAdapter")

		proxy = adapter.add(servant, broker.stringToIdentity("factoria"))

		print("Factoria: " + str(proxy))

		proxyContainer = broker.stringToProxy("container")
		factoriasContainer = drobots.ContainerPrx.checkedCast(proxyContainer)

		factoriasContainer.linkFactorias("Factoria"+"-"+str(os.getpid()), proxy)

		adapter.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()
 
		return 0

if __name__ == '__main__':
	sys.exit(Server().main(sys.argv))	
