from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI

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
        
        #define router node
        router = self.addNode('r0', cls=Router, ip = '192.168.1.1/24')
        
        #add switch nodes
        s1, s2 = [self.addSwitch(s) for s in ('s1','s2')]
        
        #add routes
        self.addLink(s1, router, intfName2 = 'ro-eth0', params2 = {'ip' : '192.168.1.1/24'})
        self.addLink(s2, router, intfName2 = 'ro-eth1', params2 = {'ip' : '10.0.0.1/8'})
        
        #add hosts
        h1 = self.addHost('h1', ip = '192.168.1.50/24', defaultRoute = 'via 192.168.1.1')
        h2 = self.addHost('h2', ip = '10.0.0.50/8', defaultRoute = 'via 10.0.0.1')
        
        #add links between hosts and switches
        #for h, s in [ (h1, s1), (h2, s2) ]:
            #self.addLink( h, s )
        #link with 10 Mbps BW, 10ms delay, 10% packet loss and 1ms jitter
        l1 = self.addLink( h1, s1, cls=TCLink )
        l1.intf1.config(bw=10, delay='10ms', loss=10, jitter='1ms')
        #link with 100 Mbps BW, 50ms delay, 25% packet loss and 2ms jitter
        l2 = self.addLink( h2, s2, cls=TCLink )
        l2.intf1.config(bw=100, delay='50ms', loss=25, jitter='2ms')
            
def run():
    "Test router"
    topo = Net_Topology()
    net = Mininet( topo=topo,
                   waitConnected=True )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r0' ].cmd( 'route' ) )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
