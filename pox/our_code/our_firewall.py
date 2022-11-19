from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.addresses import EthAddr
import pox.forwarding.l2_learning
import pox.lib.packet as pkt  #se puede definir el tipo de paquete, si es IPv4 y si es TCP o UDP
from pox.lib.util import dpid_to_str
from collections import namedtuple

from pox.our_code.topologia import gl_firewallPosition


log = core.getLogger()
class Firewall(EventMixin):

    #def ControllerRule (self, src, dst, value):
     #   if(src,dst) not in self.firewall:
      #      self.firewall[(src,dst)] = value
    
#    def DeleteRule (self, src, dst): #asumo si la llamas sabes que existe
#        del self.firewall[(src,dst)]

    def __init__(self, connection):
        log.info("------ENTRE AL FIREWALL CONSTRUCTOR")

        self.connection = connection
        connection.addListeners(self)

        #self.listenTo(core.openflow.addListenerByName("ConnectionUp",self._handle_ConnectionUp))
        self.match = of.ofp_match()
        #log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp(self,event): #o _handle_PacketIn() ???
        
        print(" Se llam'o a _handle_ConnectionUp")

        self.filter_port_dst_80(event)
        self.filter_host_1(event)
        self.uncommunicate_hosts(event,host_not_src="00:00:00:00:00:01",host_not_dst="00:00:00:00:00:04")

        #Add your logic here
        #log.debug("Switch %s has come up.", dpid_to_str(event.dpid))
        #if (event.connection.dpid == gl_firewallPosition):
        #    print(" Entre al if del _handle_ConnectionUp!! ")        
            #for fw_msg in self.firewallRules:
            #    event.connection.send(fw_msg) 
                
        
        #es el firewall, hay que verificar las reglas
        #self.filter_port_dst_80()

        #self.filter_host_1(event) ## chequear que si se dropea acá, no sigo filtrando
        
        #self.uncommunicate_hosts()


    def launch():
        log.info("------ENTRE AL FIREWALL launch")
        def start_switch(event):
            log.debug("Controlling %s" % (event.connection,))
            Firewall(event.connection)
        #core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
        core.openflow.addListenerByName("ConnectionUp", start_switch)
        #Starting the Firewall module
        #pox.forwarding.l2_learning.launch()
        #core.registerNew(Firewall)
    
    def send_message_none(self,message,event):
       #message.hard_timeout = 0
       #message.soft_timeout = 0
       #message.priority = 32768
       message.match = self.match
       message.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
       event.connection.send(message,event)

    def filter_port_dst_80(self,event):  #regla 1
        self.match.tp_dst = 80
        message = of.ofp_flow_mod()
        self.send_message_none(message,event)
        #falta lógica
        return 0

    def filter_host_1(self,event):  #regla 2
        self.match.src = EthAddr("00:00:00:00:00:01")
        self.match.nw_proto = pkt.ipv4.UDP_PROTOCOL
        self.match.nw_dst = 5001
        message = of.ofp_flow_mod()
        self.send_message_none(message,event)
        #falta lógica
        return 0

    def uncommunicate_hosts(self,event,host_not_src,host_not_dst):  #regla 3
        self.match.src = EthAddr(host_not_src)
        self.match.dst = EthAddr(host_not_dst)
        message = of.ofp_flow_mod()
        self.send_message_none(message,event)
        #falta lógica
        return 0
        