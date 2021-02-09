'''
using TCIntf options to manipulate an interface with
intf.config() to test performance metrics such as delay,
jitter, loss, bandwidth etc.

NOTE: Struggled to implement with the simple_mininet_router.py
code. Kept running into compile errors.
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI

def intfOptions():

    "run various traffic control commands on a single interface"
    net = Mininet( autoStaticArp=True, waitConnected=True )
    
  #=====================================================================    
  #SETUP
    net.addController( 'c0' )
    h1 = net.addHost( 'h1' )
    h2 = net.addHost( 'h2' )
    
    #add switch nodes
    s1, s2 = [net.addSwitch(s) for s in ('s1','s2')]
    
    #add links
    link1 = net.addLink( h1, s1, cls=TCLink )
    net.addLink( h2, s1 )
    
    net.start()

    # flush out latency from reactive forwarding delay
    net.pingAll()

  #=========================================================
  #Different configurations for testing network performance    

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
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    intfOptions()
