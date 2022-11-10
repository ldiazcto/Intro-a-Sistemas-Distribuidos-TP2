from mininet.net import Mininet
from mininet.topo import Topo

class Topo():
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )
        
        # Create switch
        s1 = self.addSwitch('switch_1')
        s2 = self.addSwitch('switch_2')
        # Create hosts
        h1 = self.addHost('host_1 ')
        h2 = self.addHost('host_2')
        
        # Add links between switches and hosts self . addLink (s1 , s2)
        self.addLink(s1 , h1)
        self.addLink(s1 , h2)

topos = { 'customTopo ': Topo }