# from mininet.net import Mininet
# from firewall import Firewall
# from topologia import MyTopo
# from mininet.log import setLogLevel, info


# --controller firewall 


#HACE FALTA CLASE NETWORK??
# localhost = '127.0.0.1'
# port_nmbr = 6633


# def myNetwork():
#     info('*** Creating net\n')
#     myTopo = MyTopo()
#     net = Mininet(topo=MyTopo, build=False, ipBase='10.0.0.0/8')

#     info('*** Adding controller\n')
#     c0 = net.addController(name='c0', controller=Firewall, ip=localhost, protocol='tcp', port=port_nmbr)
    
#     info('*** Starting network\n')
#     net.build()

#     info('*** Starting controllers\n')
#     for controller in net.controllers:
#         controller.start()

#     info('*** Starting switches\n')
#     switches = net.topo.Topo.switches() #o sin el segundo Topo?
#     for s in switches:
#         net.get("s" + s.defaultDpid()).start([c0]) #iniciamos cada switch
    
#     info('*** Post configure switches and hosts\n')
#     net.pingAll()
#     #y cualquier otra cosa que quiera hacer con mis hosts

#     info('*** Gracefull exit\n')
#     #stops the controllers, switches and hosts
#     net.stop()


# if __name__ == '__main__':
#     setLogLevel('info')
#     myNetwork()