from pox.core import core
import pox.forwarding.l2_pairs as l2p
import pox.forwarding.l2_learning as l2l
from global_vars import global_vars

log = core.getLogger()

def _handle_PacketInFirewall(event):
    log.info("Soy el handler del Firewall") #Esto se imprimirá muchas veces xd!
    l2p._handle_PacketIn(event)

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
