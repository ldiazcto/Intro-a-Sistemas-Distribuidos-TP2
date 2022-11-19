from pox.core import core
import pox.forwarding.l2_pairs as l2p
import pox.forwarding.l2_learning as l2l

log = core.getLogger()


def _handle_PacketInFirewall(event):
    log.info("Soy el handler del Firewall")
    l2p._handle_PacketIn(event)

def _handle_ConnectionUp (event):
    log.info("-----_handle_ConnectionUp")
    if event.dpid == 1:
        l2l.LearningSwitch(event.connection, False)
        log.info("Creating %s as Switch Firewall", event.connection)      
        log.info("Treating %s as l2_pairs", event.connection)
        event.connection.addListenerByName("PacketIn", _handle_PacketInFirewall)
    else:
        log.info("Treating %s as l2_learning", event.connection)
        l2l.LearningSwitch(event.connection, False)
        #event.connection.addListenerByName("PacketIn", l2l._handle_PacketIn)


def launch ():
    log.info("----- ENTREE LAUNCH DE MIXED")
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    log.info("Mixed switches demo running.")
