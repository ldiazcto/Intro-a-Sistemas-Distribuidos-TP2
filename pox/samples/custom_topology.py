from mininet.topo import Topo

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

        return switch_outter_right

    def configure_structure(self, switchesAmount ):
        firstSwtich = self.create_first_switch()
        
        previousSwitch = firstSwtich
        for i in range(1, switchesAmount): 
            newSwitch = self.addSwitch("s" + (str)(i+1))  
            self.addLink(previousSwitch, newSwitch)
            previousSwitch = newSwitch

        lastSwitch = self.create_last_switch(switchesAmount+2, previousSwitch)
    
    def __init__( self, switchesAmount=0):
        # Initialize topology
        Topo.__init__( self )
        self.configure_structure( (int) (switchesAmount))

topos = {'mytopo': MyTopo}