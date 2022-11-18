from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.addresses import EthAddr, IpAddr
import pox.forwarding.l2_learning
import pox.lib.packet as pkt  #se puede definir el tipo de paquete, si es IPv4 y si es TCP o UDP
from collections import namedtuple

from topologia import gl_firewallPosition


log = core.getLogger()
class Firewall (EventMixin):

    #def ControllerRule (self, src, dst, value):
     #   if(src,dst) not in self.firewall:
      #      self.firewall[(src,dst)] = value
    
#    def DeleteRule (self, src, dst): #asumo si la llamas sabes que existe
#        del self.firewall[(src,dst)]

    def __init__(self):
        self.listenTo(core.openflow.addListenerByName("ConnectionUp",self._handle_ConnectionUp))
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self,event): #o _handle_PacketIn() ???
        #Add your logic here
        log.debug("Switch %s has come up.", dpid_to_str(event.dpid))
        if (event.connection.dpid == gl_firewallPosition):
            for fw_msg in self.firewallRules:
                event.connection.send(fw_msg) 
                
        
        #es el firewall, hay que verificar las reglas
        self.filter_port_dst_80()

        self.filter_host_1(event) ## chequear que si se dropea acá, no sigo filtrando
        
        self.uncommunicate_hosts()

        return 0

    def launch():
        #core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)

        #Starting the Firewall module
        pox.forwarding.l2_learning.launch()
        core.registerNew(Firewall)
        

    def obtain_match(self):
        match = of.ofp_match()
        return match
        

    def filter_port_dst_80(self):  #regla 1
        self.obtain_match().tp_dst = 80
        #falta lógica
        return 0

    def filter_host_1(self, event):  #regla 2
        self.obtain_match().src = EthAddr("00:00:00:00:00:01")
        self.obtain_match().nw_proto = pkt.ipv4.UDP_PROTOCOL
        self.obtain_match().nw_dst = 5001
        #falta lógica
        return 0

    def uncommunicate_hosts(self):  #regla 3

        #falta lógica
        return 0
        
        
#https://www.youtube.com/watch?v=fzqVR4-oeso&t=502s&ab_channel=WangRobbie 

#iperf --> para pruebas de rendimiento

#get_switch_desc  ---> gets switch details
#get_switches   ---> gets list of switches

# openflow.keepalive --> pra que el switch no piense que el controller murió

#https://noxrepo.github.io/pox-doc/html/#id120

#https://noxrepo.github.io/pox-doc/html/
#https://github.com/CPqD/RouteFlow/blob/master/pox/pox/openflow/libopenflow_01.py

#https://github.com/hip2b2/poxstuff/blob/master/of_firewall.py





#https://noxrepo.github.io/pox-doc/html/#openflow-actions

#https://noxrepo.github.io/pox-doc/html/#id78


# en nuestro comando necesitamos poner algo acerca de Layer 2 learning switch, porque nuestros switches tienen que ser de tipo learning