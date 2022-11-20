from pox.core import core
import pox.forwarding.l2_pairs as l2p
import pox.forwarding.l2_learning as l2l
from global_vars import global_vars
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.addresses import EthAddr
from pox.lib.util import dpid_to_str
from collections import namedtuple
import pox.lib.packet as pkt

log = core.getLogger()

TCP = 6
UDP = 17
IP = 0X800

def send_message_none(message, event):
       #message.hard_timeout = 0
       #message.soft_timeout = 0
       #message.priority = 32768
       #message.match = self.match ##?
       #message.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
       #message.actions = []
       event.connection.send(message)

def filter_port_dst_80(event):  #regla 1
    """
    msg = of.ofp_flow_mod()
    msg.match.tp_dst = 80
    #msg.match.in_port = 80 #??
    event.connection.send(msg)
    """
    msg_tcp = of.ofp_match()
    msg_tcp.dl_type=IP
    msg_tcp.nw_proto=TCP 
    msg_tcp.tp_src = 80
    msg_tcp.tp_dst = 80 #Para poder seleccionar que el puerto sea el 80, deben si o si especificarse las capas anteriores, es decir, IP y TCP
    openflow_packet = of.ofp_flow_mod()
    openflow_packet.match = msg_tcp
    #Nota: Al no especificar una accion a realizar tras el match, el paquete sera descartado
    event.connection.send(openflow_packet)

    # msg_udp = of.ofp_match()
    # msg_udp.dl_type=IP
    # msg_udp.nw_proto=UDP
    # msg_udp.tp_dst = 80
    # openflow_packet = of.ofp_flow_mod()
    # openflow_packet.match = msg_udp
    # event.connection.send(openflow_packet)
    #log.debug("Firewall rules 1 installed on %s", dpidToStr(event.dpid))


#def filter_host_1(event):  #regla 2
#    self.match.src = EthAddr("00:00:00:00:00:01")
#   self.match.nw_proto = pkt.ipv4.UDP_PROTOCOL
#    self.match.nw_dst = 5001
#    message = of.ofp_flow_mod()
#    self.send_message_none(message,event)

def uncommunicate_hosts(event, host_not_src, host_not_dst):  #regla 3
    msg = of.ofp_flow_mod()
    msg.match.dl_src = EthAddr(host_not_src) # not reversed this time!
    msg.match.dl_dst= EthAddr(host_not_dst)
    event.connection.send(msg)


def _handle_PacketInFirewall(event):
    log.info("Soy el handler del Firewall") #Esto se imprimirá muchas veces xd!
    #uncommunicate_hosts(event, host_not_src="00:00:00:00:00:01", host_not_dst="00:00:00:00:00:04") #VER COMO PARAMETRIZAR HOSTS
    #filter_port_dst_80(event)


def _handle_ConnectionUp (event):
    log.info("-----_handle_ConnectionUp")

    if event.dpid ==  (global_vars.firewallPosition) :
        l2l.LearningSwitch(event.connection, False)
        log.info("--- SOY FIREWALL Switchh Number-----> %s", event.dpid)      
        #log.info("Creating %s as Switch Firewall", event.connection)      
        #log.info("Treating %s as l2_pairs", event.connection)
        event.connection.addListenerByName("PacketIn", _handle_PacketInFirewall)
    else:
        log.info("---NOOOOOOOO SOY FIREWALL Switchh Number-----> %s", event.dpid)      
        #log.info("Treating %s as l2_learning", event.connection)
        l2l.LearningSwitch(event.connection, False)
        #event.connection.addListenerByName("PacketIn", l2l._handle_PacketIn)

def launch (firewallPosition):
    log.info("----- ENTREE LAUNCH DE MIXED")
    global_vars.firewallPosition = (int)(firewallPosition)
    if( global_vars.firewallPosition <= 0):
        log.error("Firewall Postion incorrecto, debe ser mayor a 0")

    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    log.info("Mixed switches demo running.")
    log.info("Firewall position-------------> %s", global_vars.firewallPosition)
