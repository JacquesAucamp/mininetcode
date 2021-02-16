from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI
import sys

n = len(sys.argv)-1
print("Total arguments passed:", n)

#-----------------------------------------------------------------------------
# CLI STRING PROCESSING
#-----------------------------------------------------------------------------
str_arg2 = str(sys.argv[2])
final_arg2 = "'" + str_arg2 + "ms" + "'"

str_arg4 = str(sys.argv[4])
final_arg4 = "'" + str_arg4 + "ms" + "'"

str_arg6 = str(sys.argv[6])
final_arg6 = "'" + str_arg6 + "ms" + "'"

str_arg8 = str(sys.argv[8])
final_arg8 = "'" + str_arg8 + "ms" + "'"
#=============================================================================

#-----------------------------------------------------------------------------
# ROUTER DEFINITION
#-----------------------------------------------------------------------------
class Router(Node):
    "Node that will act as the router to send network traffic through"
    
    #Router configuration
    def config(self, **params):                      
        super( Router, self).config( **params )
        self.cmd('sysctl net.ipv4.ip_forward=1')      #enables port forwarding on the router node
        
    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super( Router, self ).terminate()
#------------------------------------------------------------------------------
# MININET TOPOLOGY SETUP
#------------------------------------------------------------------------------
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
        self.addLink(h1, s1, cls=TCLink, bw=int(sys.argv[1]), delay=final_arg2, loss=int(sys.argv[3]), jitter=final_arg4)
        #link with 100 Mbps BW, 50ms delay, 25% packet loss and 2ms jitter
        self.addLink(h2, s2, cls=TCLink, bw=int(sys.argv[5]), delay=final_arg6, loss=int(sys.argv[7]), jitter=final_arg8)
#==========================================================================================================================

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
