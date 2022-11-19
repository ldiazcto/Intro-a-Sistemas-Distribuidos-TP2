from pox.core import core
import pox.forwarding.l2_pairs as l2p
import pox.forwarding.l2_learning as l2l

log = core.getLogger()

def _handle_ConnectionUp (event):
    log.info("-----_handle_ConnectionUp")
    if event.dpid & 1 == 1:
        log.info("Treating %s as l2_pairs", event.connection)
        event.connection.addListenerByName("PacketIn", l2p._handle_PacketIn)
    else:
        log.info("Treating %s as l2_learning", event.connection)
        l2l.LearningSwitch(event.connection, False)

def launch ():
    log.info("----- ENTREE LAUNCH DE MIXED")
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    log.info("Mixed switches demo running.")
