#!/usr/bin/python -u
# -*- coding:utf-8; tab-width:4; mode:python -*-

#fuente: repositorio ice-hello de la asignatura
import sys
import Ice

Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all drobotsAux.ice')

import drobots

class ContainerI(drobots.Container):
    def __init__(self):
        self.proxies = dict()
        self.factorias = dict()
        self.controller = dict()
        self.minas = dict()

    def link(self, key, proxy, current=None):
        if(key) in self.proxies:
            raise drobots.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def linkFactorias(self, key, proxy, current=None):
        if(key) in self.factorias:
            raise drobots.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.factorias[key] = proxy

    def linkController(self, key, proxy, current=None):
        if(key) in self.controller:
            raise drobots.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.controller[key] = proxy

    def linkMinas(self, key, proxy, current=None):
        if(key) in self.minas:
            raise drobots.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.minas[key] = proxy

    def unlink(self, key, current=None):
        if not (key) in self.proxies:
            raise drobots.NoSuchKey(key)

        print("unlink: {0}".format(key))
        del self.proxies[key]

    def list(self, current=None):
        return self.proxies

    def listFactorias(self, current=None):
        return self.factorias

    def listController(self, current=None):
        return self.controller

    def listMinas(self, current=None):
        return self.minas

    def get(self, key, current=None):
        return self.proxies[key]

    def keys(self, current=None):
        return self.proxies.keys()

    def items(self, current=None):
        return self.proxies.items()

    def getValueFactorias(self, index, current=None):
        return self.factorias.values()[index]

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ContainerI()

        adapter = broker.createObjectAdapter("ContainerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("container"))

        print("Container: " + str(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))
