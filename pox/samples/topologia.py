#import global_vars.global_vars as global_vars
#from pox.core import core
#import pox.forwarding.l2_pairs as l2p
#import pox.forwarding.l2_learning as l2l
#log = core.getLogger()

from mininet.topo import Topo

#print("GLOBAL VARS %s", global_vars)
class MyTopo(Topo):

    def create_first_switch(self) :
        switch_outter_left = self.addSwitch("s1")
        h1_left = self.addHost("h1")
        h2_left = self.addHost("h2")

        self.addLink(switch_outter_left , h1_left)
        self.addLink(switch_outter_left , h2_left)

        return switch_outter_left

    def create_last_switch(self, switchNumber, previousSwitch) :
        switch_outter_right = self.addSwitch("s"+(str)(switchNumber))
        h1 = self.addHost("h3")
        h2 = self.addHost("h4")

        self.addLink(switch_outter_right , h1)
        self.addLink(switch_outter_right , h2)

        self.addLink(previousSwitch, switch_outter_right)

        # if (firewallPosition == switchNumber):
        #      print("Soy firewall! pos = ", switchNumber)

        return switch_outter_right



    def configure_structure(self, switchesAmount):
        firstSwtich = self.create_first_switch()
        
        previousSwitch = firstSwtich
        for i in range(2, switchesAmount): 
            newSwitch = self.addSwitch("s" + (str)(i))  
            self.addLink(previousSwitch, newSwitch)
            previousSwitch = newSwitch

        lastSwitch = self.create_last_switch(switchesAmount, previousSwitch)
    
    def __init__( self, switchesAmount=0):
        # Initialize topology
        Topo.__init__( self )
        print("Switched smount-->" , switchesAmount)


        #-----------Verificacion
        #log.info("Firewall Position actualizado a ---->>>>%s", global_vars.firewallPosition)
        #if (switchesAmount < global_vars.firewallPosition):
         #   print("sd")
            #log.error("FirewallPosition inalcanzable, debe ser menor o igual a la cantidad de swithces ingresados")
        self.configure_structure( (int) (switchesAmount))
    
        print("Termine de crear!")

topos = {'mytopo': MyTopo}

#---Levantar topologia parados en la carpeta pox/samples --- > EDIT : Ahora no se le pasa la posicion del firewall
#sudo mn --custom ./topologia.py --topo mytopo,5 --mac --controller=remote

#------Este comando se ejecuta si pox.py esta afuera de la carpeta pox
#python3 pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning samples.new_firewall --firewallPosition=2

#Sino va este
#pox/pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning samples.our_firewall


# asegurarse de estar en el branch helosaur
#->  git checkout halosaur


#sudo mn -c <-- para terminar de borrar cosas colgadas de mininet
'''
mininet> net // muestra informacion sobre la red
mininet> pingall //manda ping a todos y te dice cuantos dropeo
mininet> h1 ping c1 h2 // manda un ping desde el Host 1 (h1) al Host 2 (h2)
mininet> h1 ifconfig // muestra informacion sobre los interfaces de h1
mininet> exit // cierra la consola
'''