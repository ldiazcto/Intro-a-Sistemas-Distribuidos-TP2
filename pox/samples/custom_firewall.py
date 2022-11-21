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
HOST1_ADDR = "00:00:00:00:00:01"

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
    msg.match.dl_src = EthAddr(HOST1_ADDR)
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
    log.debug("Firewall handler starting...")
    filter_port_dst_80(event)
    filter_host_1(event)
    uncommunicate_hosts(event, host_not_src=global_vars.host_not_src, host_not_dst=global_vars.host_not_dst)
    log.debug("Firewall handler completed")

def _handle_ConnectionUp (event):
    if event.dpid ==  (global_vars.firewallPosition) :
        l2l.LearningSwitch(event.connection, False)
        log.info("--- Creating %s as Switch Firewall", event.connection)      
        event.connection.addListenerByName("PacketIn", _handle_PacketInFirewall)
    else:
        log.info("--- Creating %s as L2 learning Switch", event.connection)
        l2l.LearningSwitch(event.connection, False)


def launch (firewallPosition, host_not_src=1, host_not_dst=4):
    log.debug("Firewall launch starting...")
    global_vars.firewallPosition = (int)(firewallPosition)
    
    if ((int)(host_not_src) <= 0 or (int)(host_not_src) > 4) or ((int)(host_not_dst) <= 0 or (int)(host_not_dst) >= 5):
        log.error("Incorrect hosts entered. Both must be 1, 2, 3 or 4")

    global_vars.host_not_src = "00:00:00:00:00:0" + (str)(host_not_src)
    global_vars.host_not_dst = "00:00:00:00:00:0" + (str)(host_not_dst)

    if (global_vars.firewallPosition <= 0):
        log.error("Incorrect Firewall Postion, must be > 0")
    
    if (global_vars.host_not_src == global_vars.host_not_dst):
        log.error("Incorrect hosts entered. Must be different hosts")

    log.debug("Firewall position received ---> %s", global_vars.firewallPosition)
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    log.debug("Firewall launch completed")
    