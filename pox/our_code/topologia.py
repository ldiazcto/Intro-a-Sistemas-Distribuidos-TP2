# coding=utf-8
from mininet.topo import Topo
import sys;
import getopt

gl_firewallPosition = 1

class MyTopo(Topo):

    def create_first_switch(self, firewallPosition) :
        switch_outter_left = self.addSwitch("s1")
        h1_left = self.addHost("h1")
        h2_left = self.addHost("h2")

        self.addLink(switch_outter_left , h1_left)
        self.addLink(switch_outter_left , h2_left)

        # if (firewallPosition == 1):
        #     print("Soy firewall! pos = ", 1)

        return switch_outter_left

    def create_last_switch(self, switchNumber, previousSwitch, firewallPosition) :
        switch_outter_right = self.addSwitch("s"+(str)(switchNumber))
        h1 = self.addHost("h3")
        h2 = self.addHost("h4")

        self.addLink(switch_outter_right , h1)
        self.addLink(switch_outter_right , h2)

        self.addLink(previousSwitch, switch_outter_right)

        # if (firewallPosition == switchNumber):
        #     print("Soy firewall! pos = ", switchNumber)

        return switch_outter_right



    def configure_structure(self, switchesAmount, firewallPosition):
        firstSwtich = self.create_first_switch(firewallPosition)
        
        previousSwitch = firstSwtich
        for i in range(2, switchesAmount):
            # if (i == firewallPosition):
            #     print("Soy firewall! pos = ", i)
                
            newSwitch = self.addSwitch("s" + (str)(i))  
            self.addLink(previousSwitch, newSwitch)
            previousSwitch = newSwitch

        lastSwitch = self.create_last_switch(switchesAmount, previousSwitch, firewallPosition)
    
    def __init__( self, switchesAmount=3, firewallPosition=1):
        # Initialize topology
        Topo.__init__( self )
        print("Switched smount-->" , switchesAmount)
        print("firewallPosition--->" , firewallPosition)
        
        gl_firewallPosition = firewallPosition
        
        self.configure_structure( (int) (switchesAmount),(int) (firewallPosition))
    
        print("Terminé de crear!")

topos = {'mytopo': MyTopo}


#sudo mn --custom ./topologia.py --topo mytopo,5,1 --mac --controller=remote
# asegurarse de estar en el branch helosaur
#->  git checkout halosaur


#sudo mn -c <-- para terminar de borrar cosas colgadas de mininet
'''
mininet> net // muestra información sobre la red
mininet> pingall //manda ping a todos y te dice cuántos dropeo
mininet> h1 ping –c1 h2 // manda un ping desde el Host 1 (h1) al Host 2 (h2)
mininet> h1 ifconfig // muestra información sobre los interfaces de h1
mininet> exit // cierra la consola
'''