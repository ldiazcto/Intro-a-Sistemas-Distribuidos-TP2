from mininet.net import Mininet
from mininet.topo import Topo

class MyTopo(Topo):
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )
        
        # Create switch
        s1 = self.addSwitch("switch_1")
        #s2 = self.addSwitch('switch_2')
        # Create hosts
        h1 = self.addHost("host_1")
        h2 = self.addHost("host_2")
        
        # Add links between switches and hosts self . addLink (s1 , s2)
        self.addLink(s1 , h1)
        self.addLink(s1 , h2)

#topos = { 'customTopo ': Topo }
topos = {'mytopo': MyTopo}
#

#sudo mn --custom ./topologia.py --topo mytopo --mac --switch ovsk
'''
mininet> net // muestra información sobre la red
mininet> h1 ping –c1 h2 // manda un ping desde el Host 1 (h1) al Host 2 (h2)
mininet> h1 ifconfig // muestra información sobre los interfaces de h1
mininet> exit // cierra la consola
'''