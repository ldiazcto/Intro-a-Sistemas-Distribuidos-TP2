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
BANNED_PORT_R1 = 80
BANNED_PORT_R2 = 5001



#RULE 1
def filter_port_dst_80(event):  
    log.debug("-- Starting to execute RULE 1 --")
    log.debug("- Filtering TCP messages... -")
    msg_tcp = of.ofp_flow_mod()
    msg_tcp.match.dl_type = IP
    msg_tcp.match.nw_proto = TCP
    msg_tcp.match.tp_dst = BANNED_PORT_R1
    event.connection.send(msg_tcp)
    
    log.debug("- Filtering UDP messages... -")
    msg_udp = of.ofp_flow_mod()
    msg_udp.match.dl_type = IP
    msg_udp.match.nw_proto = UDP
    msg_udp.match.tp_dst = BANNED_PORT_R1
    event.connection.send(msg_udp)

    log.debug("-- RULE 1 complete --")

#RULE 2
def filter_host_1(event):
    log.debug("-- Starting to execute RULE 2 --")
    msg = of.ofp_flow_mod()
    msg.match.dl_src = EthAddr("00:00:00:00:00:01")
    msg.match.dl_type = IP
    msg.match.nw_proto = UDP
    msg.match.tp_dst = BANNED_PORT_R2
    event.connection.send(msg)
    log.debug("-- RULE 2 complete --")
    
#RULE 3
def uncommunicate_hosts(event, host_not_src, host_not_dst): 
    log.debug("-- Starting to execute RULE 3 --")
    msg = of.ofp_flow_mod()
    msg.match.dl_src = EthAddr(host_not_src)
    msg.match.dl_dst= EthAddr(host_not_dst)
    event.connection.send(msg)
    log.debug("-- RULE 3 complete --")


def _handle_PacketInFirewall(event):
    log.info("Soy el handler del Firewall") #Esto se imprimirá muchas veces xd!
    filter_port_dst_80(event)
    filter_host_1(event)
    uncommunicate_hosts(event, host_not_src="00:00:00:00:00:01", host_not_dst="00:00:00:00:00:04") #VER COMO PARAMETRIZAR HOSTS
    

def _handle_ConnectionUp (event):
    log.info("-----_handle_ConnectionUp")
    if event.dpid ==  (global_vars.firewallPosition) :
        l2l.LearningSwitch(event.connection, False)
        log.info("--- SOY FIREWALL Switchh Number-----> %s", event.dpid)      
        log.info("Creating %s as Switch Firewall", event.connection)      
        event.connection.addListenerByName("PacketIn", _handle_PacketInFirewall)
    else:
        log.info("---NOOOOOOOO SOY FIREWALL Switchh Number-----> %s", event.dpid)      
        l2l.LearningSwitch(event.connection, False)
        #event.connection.addListenerByName("PacketIn", l2l._handle_PacketIn)

def launch (firewallPosition):
    global_vars.firewallPosition = (int)(firewallPosition)
    if( global_vars.firewallPosition <= 0):
        log.error("Firewall Postion incorrecto, debe ser mayor a 0")

    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    log.info("Mixed switches demo running.")
    log.info("Firewall position-------------> %s", global_vars.firewallPosition)
