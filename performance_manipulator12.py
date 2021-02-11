  
'''
using TCIntf options to manipulate an interface with
intf.config() to test performance metrics such as delay,
jitter, loss, bandwidth etc.
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

class Router(Node):
    "Node that will act as the router to send network traffic through"
    
    #Router configuration
    def config(self, **params):                      
        super( Router, self).config( **params )
        self.cmd('sysctl net.ipv4.ip_forward=1')      #enables port forwarding on the router node
        
    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super( Router, self ).terminate()
        
class Net_Topology(Topo):
    "Router connects to 2 subnets (hosts) "
    
    def build(self, k = 2):
        
        net = Mininet( autoStaticArp=True, waitConnected=True )
        
        #define router node
        router = net.addNode('r0', cls=Router, ip = '192.168.1.1/24')
        
        #add switch nodes
        s1, s2 = [net.addSwitch(s) for s in ('s1','s2')]
        
        #add routes
        net.addLink(s1, router, intfName2 = 'ro-eth0', params2 = {'ip' : '192.168.1.1/24'})
        net.addLink(s2, router, intfName2 = 'ro-eth1', params2 = {'ip' : '10.0.0.1/8'})
        
        #add hosts
        h1 = net.addHost('h1', ip = '192.168.1.50/24', defaultRoute = 'via 192.168.1.1')
        h2 = net.addHost('h2', ip = '10.0.0.50/8', defaultRoute = 'via 10.0.0.1')
        
        #add links between hosts and switches
        #add adjustable performance link
        link1 = net.addLink(h1, s1, cls = TCLink)
        #add normal link
        net.addLink(h2, s1)
        

        "Test router"
        net.start()
        info( '*** Routing Table on Router:\n' )
        info( net[ 'r0' ].cmd( 'route' ) )


        # flush out latency from reactive forwarding delay
        net.pingAll()

        info('\n***Configure one intf with 10Mb/s bandwidth')
        link1.intf1.config( bw=10 )
        info( '\n*** Running iperf to test\n' )
        net.iperf( seconds=10 )

        info( '\n*** Configuring one intf with delay of 15ms\n' )
        link1.intf1.config( delay='15ms' )
        info( '\n*** Run a ping to confirm delay of 15ms\n' )
        net.pingPairFull()

        info( '\n*** Configuring one intf with jitter of 1ms\n' )
        link1.intf1.config( jitter='1ms' )
        info( '\n*** Run iperf to confirm 1ms jitter\n' )
        net.iperf( ( h1, h2 ), l4Type='UDP' )

        info( '\n*** Configuring one intf with loss of 50%\n' )
        link1.intf1.config( loss=50 )
        info( '\n' )
        net.iperf( ( h1, h2 ), l4Type='UDP' )

        info( '\n*** Done testing\n' )

        CLI( net )
        net.stop()
    
    self = build.self
    if __name__ == '__main__':
        setLogLevel( 'info' )
        build(self)  
