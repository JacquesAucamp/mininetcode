from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI
import sys

n = len(sys.argv)-1
print("Total arguments passed:", n)



#=============================================================================
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

str_arg10 = str(sys.argv[10])
final_arg10 = "'" + str_arg10 + "ms" + "'"

str_arg12 = str(sys.argv[12])
final_arg12 = "'" + str_arg12 + "ms" + "'"

str_arg14 = str(sys.argv[14])
final_arg14 = "'" + str_arg14 + "ms" + "'"

str_arg16 = str(sys.argv[16])
final_arg16 = "'" + str_arg16 + "ms" + "'"

str_arg18 = str(sys.argv[18])
final_arg18 = "'" + str_arg18 + "ms" + "'"

str_arg20 = str(sys.argv[20])
final_arg20 = "'" + str_arg20 + "ms" + "'"

str_arg22 = str(sys.argv[22])
final_arg22 = "'" + str_arg22 + "ms" + "'"

str_arg24 = str(sys.argv[24])
final_arg24 = "'" + str_arg24 + "ms" + "'"

str_arg26 = str(sys.argv[26])
final_arg26 = "'" + str_arg26 + "ms" + "'"

str_arg28 = str(sys.argv[28])
final_arg28 = "'" + str_arg28 + "ms" + "'"
#=============================================================================



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
        h1_2 = self.addHost('h1_2', ip = '192.168.1.51/24', defaultRoute = 'via 192.168.1.1')
        h1_3 = self.addHost('h1_3', ip = '192.168.1.52/24', defaultRoute = 'via 192.168.1.1')
        
        h2 = self.addHost('h2', ip = '10.0.0.50/8', defaultRoute = 'via 10.0.0.1')
        h2_2 = self.addHost('h2_2', ip = '10.0.0.51/8', defaultRoute = 'via 10.0.0.1')
        h2_3 = self.addHost('h2_3', ip = '10.0.0.52/8', defaultRoute = 'via 10.0.0.1')
        
        #add links between hosts and switches
            
        self.addLink(h1, s1, cls=TCLink, bw=int(sys.argv[1]), delay=final_arg2, loss=int(sys.argv[3]), jitter=final_arg4)
        self.addLink(h1_2, s1, cls=TCLink, bw=int(sys.argv[5]), delay=final_arg6, loss=int(sys.argv[1]), jitter=final_arg8)
        self.addLink(h1_3, s1, cls=TCLink, bw=int(sys.argv[9]), delay=final_arg10, loss=int(sys.argv[11]), jitter=final_arg12)
        self.addLink(h2, s2, cls=TCLink, bw=int(sys.argv[13]), delay=final_arg14, loss=int(sys.argv[15]), jitter=final_arg16)
        self.addLink(h2_2, s2, cls=TCLink, bw=int(sys.argv[17]), delay=final_arg18, loss=int(sys.argv[19]), jitter=final_arg20)
        self.addLink(h2_3, s2, cls=TCLink, bw=int(sys.argv[21]), delay=final_arg22, loss=int(sys.argv[23]), jitter=final_arg24)
        
        self.addLink(h1_3, h2_3, cls=TCLink, bw=int(sys.argv[25]), delay=final_arg26, loss=int(sys.argv[27]), jitter=final_arg28)
#==========================================================================================================================



#==============================================================================================
def run():
    "Test router"
    topo = Net_Topology()
    net = Mininet( topo=topo,
                   waitConnected=True )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r0' ].cmd( 'route' ) )
    
    #------------------------------------------------------------------------------------------
    #Performance Tests
    #------------------------------------------------------------------------------------------
    ###Test Losses and Delays###
    info(net['h1'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee test_output.txt'))
    info(net['h1_2'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    info(net['h1_3'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    info(net['h2'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    info(net['h2_2'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    info(net['h2_3'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    
    ###Test Link Bandwidths between hosts and router###
    #info(net['h1'].cmd('iperf -t 10 -c %s | tee -a test_output.txt' %net['r0'].IP()))
    #info(net['h1_2'].cmd('iperf -t 10 -c %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    #info(net['h1_3'].cmd('iperf -t 10 -c %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    #info(net['h2'].cmd('iperf -t 10 -c %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    #info(net['h2_2'].cmd('iperf -t 10 -c %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    #info(net['h2_3'].cmd('iperf -t 10 -c %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    
    #------------------------------------------------------------------------------------------
    #Reading performance test outputs
    #------------------------------------------------------------------------------------------
    with open("test_output.txt", "r") as outFile:     #Read from results
        while True:
            current_line = outFile.readline()         #Read line
            if not current_line:                      #Break if no lines are left
                break
            elif current_line.startswith('-'):        #Look for specific line
                print('Found info!')
                packet_line = outFile.readline()      #Packet info line read
                print(packet_line)                    #Print Packet info line
                
                #Find the number of packets received
                for n in range(len(packet_line)-1):
                    if packet_line[n] == ',' and packet_line[n+5] == 'r':
                        received_pack = packet_line[n+2] + packet_line[n+3]
                        int_received_pack = int(received_pack)
                        print('Number of received packets: '+ int_received_pack)
                        break
                    elif packet_line[n] == ',' and packet_line[n+4] == 'r':
                        received_pack = packet_line[n+2]
                        int_received_pack = int(received_pack)
                        print('Number of received packets: '+ int_received_pack)
                        break
                    else:
                        print('Looking for received packet amount...')
                    
                rtt_line = outFile.readline()         #RTT info line read
                print(rtt_line)                       #Print RTT info line
            else:
                print('searching...')
    
    CLI( net )
    net.stop()
#==============================================================================================

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
