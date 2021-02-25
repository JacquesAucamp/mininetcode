from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI
import sys
import random
import time
import numpy as np


n = len(sys.argv)-1
print("Total arguments passed:", n)


#===========================================================================
#--------------------------------------------------------------------------
# CLI STRING PROCESSING                                                    |
#--------------------------------------------------------------------------
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
#----------------------------------------------------------------------------
# Link Performance Randomizer                                                |
#----------------------------------------------------------------------------

### List of potential performance parameters for the links ###
bws_list = [10, 20, 40, 80, 100, 200, 400, 500, 1000]
delays_list = ['1ms', '2ms', '5ms', '10ms', '20ms', '50ms']
losses_list = [5, 10, 20, 50, 75, 90]
jitter_list = ['1ms', '2ms', '3ms', '4ms', '5ms']

### Retrieve Random Parameter Values ###
random_bw = random.sample(bws_list,6)
random_delay = random.sample(delays_list,6)
random_loss = random.sample(losses_list,6)
random_jitter = random.sample(jitter_list,6)

print("The Link Bandwidths are: %d, %d, %d, %d, %d, %d" %(random_bw[0],random_bw[1],random_bw[2],random_bw[3],random_bw[4],random_bw[5]))
print("The Link Delays are: %s, %s, %s, %s, %s, %s" %(random_delay[0],random_delay[1],random_delay[2],random_delay[3],random_delay[4],random_delay[5]))
print("The Link Losses are: %d, %d, %d, %d, %d, %d" %(random_loss[0],random_loss[1],random_loss[2],random_loss[3],random_loss[4],random_loss[5]))
print("The Link Jitters are: %s, %s, %s, %s, %s, %s" %(random_jitter[0],random_jitter[1],random_jitter[2],random_jitter[3],random_jitter[4],random_jitter[5]))

#=============================================================================

#=============================================================================
#----------------------------------------------------------------------------
# TRAFFIC DEFAULTS                                                           |
#----------------------------------------------------------------------------
### Level 4 Protocols ###
protocol_list = ['--udp', '']  # udp / tcp
port_min = 1025
port_max = 65536

### IPERF SETTINGS ###
sampling_interval = '1'  # seconds

### ELEPHANT FLOW PARAMS ###
elephant_bandwidth_list = ['10M', '20M', '30M', '40M', '50M', '60M', '70M', '80M', '90M', '100M',
                           '200M', '300M', '400M', '500M', '600M', '700M', '800M', '900M', '1000M']
#=============================================================================

#=============================================================================
#----------------------------------------------------------------------------
# ROUTER DEFINITION                                                          |
#----------------------------------------------------------------------------
class Router(Node):
    "Node that will act as the router to send network traffic through"
    
    #Router configuration
    def config(self, **params):                      
        super( Router, self).config( **params )
        self.cmd('sysctl net.ipv4.ip_forward=1')      #enables port forwarding on the router node
        
    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super( Router, self ).terminate()
#-----------------------------------------------------------------------------
# MININET TOPOLOGY SETUP                                                      |
#-----------------------------------------------------------------------------
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
            
        #self.addLink(h1, s1, cls=TCLink, bw=int(sys.argv[1]), delay=final_arg2, loss=int(sys.argv[3]), jitter=final_arg4)
        #self.addLink(h1_2, s1, cls=TCLink, bw=int(sys.argv[5]), delay=final_arg6, loss=int(sys.argv[1]), jitter=final_arg8)
        #self.addLink(h1_3, s1, cls=TCLink, bw=int(sys.argv[9]), delay=final_arg10, loss=int(sys.argv[11]), jitter=final_arg12)
        #self.addLink(h2, s2, cls=TCLink, bw=int(sys.argv[13]), delay=final_arg14, loss=int(sys.argv[15]), jitter=final_arg16)
        #self.addLink(h2_2, s2, cls=TCLink, bw=int(sys.argv[17]), delay=final_arg18, loss=int(sys.argv[19]), jitter=final_arg20)
        #self.addLink(h2_3, s2, cls=TCLink, bw=int(sys.argv[21]), delay=final_arg22, loss=int(sys.argv[23]), jitter=final_arg24)
        
        self.addLink(h1, s1, cls=TCLink, bw=random_bw[0], delay=random_delay[0], loss=random_loss[0], jitter=random_jitter[0])
        self.addLink(h1_2, s1, cls=TCLink, bw=random_bw[1], delay=random_delay[1], loss=random_loss[1], jitter=random_jitter[1])
        self.addLink(h1_3, s1, cls=TCLink, bw=random_bw[2], delay=random_delay[2], loss=random_loss[2], jitter=random_jitter[2])
        self.addLink(h2, s2, cls=TCLink, bw=random_bw[3], delay=random_delay[3], loss=random_loss[3], jitter=random_jitter[3])
        self.addLink(h2_2, s2, cls=TCLink, bw=random_bw[4], delay=random_delay[4], loss=random_loss[4], jitter=random_jitter[4])
        self.addLink(h2_3, s2, cls=TCLink, bw=random_bw[5], delay=random_delay[5], loss=random_loss[5], jitter=random_jitter[5])
        
        #self.addLink(h1_3, h2_3, cls=TCLink, bw=int(sys.argv[25]), delay=final_arg26, loss=int(sys.argv[27]), jitter=final_arg28)
#==========================================================================================================================

#==================================================================================================
#-----------------------------------------------------------------------------------------
#Generate Traffic                                                                         |
#-----------------------------------------------------------------------------------------
def random_normal_number(low, high):
    range = high - low
    mean = int(float(range) * float(75) / float(100)) + low
    sd = int(float(range) / float(4))
    num = np.random.normal(mean, sd)
    return int(num)

def generate_traf_flows(id,duration,net):

    hosts_1 = [net['h1'],net['h1_2'],net['h1_3']]
    hosts_2 = [net['h2'],net['h2_2'],net['h2_3']]
    
    ### Select a random source and destination ###
    src1_end_points = random.sample(hosts_1,2)
    src2_end_points = random.sample(hosts_2,2)
    src1 = net.get(str(src1_end_points[0]))
    dst = net['r0']
    
    ### Select Connection Parameters ###
    protocol = random.choice(protocol_list)                     #Choose random protocol from above list
    port_argument = str(random.randint(port_min, port_max))     #Choose random port interval
    bandwidth_argument = random.choice(elephant_bandwidth_list) #Choose random bw from list
    
    ### Create a server cmd ###
    server_cmd = "iperf -s "
    server_cmd += protocol
    server_cmd += " -p "
    server_cmd += port_argument
    server_cmd += " -i "
    server_cmd += sampling_interval
    server_cmd += " > "
    server_cmd += "server_log.txt 2>&1"
    server_cmd += " & "
    
    ### Create a client cmd ###
    client_cmd = "iperf -c "
    client_cmd += dst.IP() + " "
    client_cmd += protocol
    client_cmd += " -p "
    client_cmd += port_argument
    if protocol == "--udp":
        client_cmd += " -b "
        client_cmd += bandwidth_argument
    client_cmd += " -t "
    client_cmd += str(duration)
    client_cmd += " & "
    
    ### send the cmd ###
    dst.cmdPrint(server_cmd)
    src1.cmdPrint(client_cmd)
    
def generate_flows(n_elephant_flows, duration, net):
    interval = duration / n_elephant_flows
    
    ### setting random flow types (only one type for now)
    flow_type = []
    for i in range(n_elephant_flows):
        flow_type.append('E')
    random.shuffle(flow_type)
    
    ### Set random flow start time ###
    flow_start_time = []
    for i in range(n_elephant_flows):
        n = random.randint(1, interval)
        if i == 0:
            flow_start_time.append(0)
        else:
            flow_start_time.append(flow_start_time[i - 1] + n)
            
    ### Set random flow end time
    flow_end_time = []
    for i in range(n_elephant_flows):
        s = flow_start_time[i]
        e = int(float(95) / float(100) * float(duration))  # 95% of the duration
        end_time = random_normal_number(s, e)
        while end_time > e:
            end_time = random_normal_number(s, e)
        flow_end_time.append(end_time)
        
    ### Calculate flow duration from above values ###
    flow_duration = []
    for i in range(n_elephant_flows):
        flow_duration.append(flow_end_time[i] - flow_start_time[i])
        
    print(flow_start_time)
    print(flow_end_time)
    print(flow_duration)
    print("Remaining duration :" + str(duration - flow_start_time[-1]))
    
    ### Generate flows based on above times ###
    count = 0
    for i in range(n_elephant_flows):
        if count == 0:
            count += 1
            if i == 0:
                time.sleep(flow_start_time[i])
            else:
                time.sleep(flow_start_time[i] - flow_start_time[i-1])
            if flow_type[i] == 'E':
                generate_traf_flows(i, flow_duration[i], net)
        elif count != 0:
            break

        
    ### Sleep for rest of duration ###
    remaining_duration = duration - flow_start_time[-1]
    info("Traffic started, going to sleep for %s seconds...\n " % remaining_duration)
    time.sleep(remaining_duration)
    
    info("Stopping traffic...\n")
    info("Killing active iperf sessions...\n")

    ### killing iperf in all the hosts ###
    for host in net.hosts:
        host.cmdPrint('killall -9 iperf')
#==================================================================================================

#==================================================================================================
#-------------------------------------------------------------------------------------------------
# Reading performance test outputs                                                                |
#-------------------------------------------------------------------------------------------------
def performance_reader():
    with open("test_output.txt", "r") as outFile:     #Read from results
            link_num = 0
            while True:
                current_line = outFile.readline()         #Read line
                if not current_line:                      #Break if no lines are left
                    break
                elif current_line.startswith('-'):        #Look for specific line
                    link_num += 1
                    print('Found info!')

                    ### LOSS FINDING ###
                    packet_line = outFile.readline()      #Packet info line read
                    print(packet_line)                    #Print Packet info line
                    #Find the number of packets received
                    for n in range(len(packet_line)-1):
                        if packet_line[n] == ',' and packet_line[n+5] == 'r': 
                            received_pack = packet_line[n+2] + packet_line[n+3]
                            int_received_pack = int(received_pack)
                            print('Number of received packets: %d' %int_received_pack)
                        elif packet_line[n] == ',' and packet_line[n+4] == 'r':
                            received_pack = packet_line[n+2]
                            int_received_pack = int(received_pack)
                            print('Number of received packets: %d' %int_received_pack)
                        elif packet_line[n] == ',' and packet_line[n+6] == 'p':
                            received_pack_perc = packet_line[n+2] + packet_line[n+3]
                            int_received_pack_perc = int(received_pack_perc)
                            print('The percentage packet loss is: %d' %int_received_pack_perc)
                            break
                        elif packet_line[n] == ',' and packet_line[n+5] == 'p':
                            received_pack_perc = packet_line[n+2]
                            int_received_pack_perc = int(received_pack_perc)
                            print('The percentage packet loss is: %d' %int_received_pack_perc)
                            break
                        else:
                            print('Looking for received packet amount...')

                    ### RTT FINDING ###
                    rtt_line = outFile.readline()                       #RTT info line read
                    print(rtt_line)                                     #Print RTT info line
                    #Find the average rtt from the rtt_line
                    slash_count = 0
                    avg_rtt = ''
                    for n in range(len(rtt_line)-1):        
                        if rtt_line[n] == '/' and slash_count < 3:      #Find the first 3 slashes
                            slash_count += 1
                            print('Looking for average RTT value...')
                        elif rtt_line[n] == '/' and slash_count == 3:   #Already past first 3
                            k=n+1
                            while rtt_line[k] != '/':                   #Read the number between 2 slashes
                                avg_rtt += rtt_line[k]
                                k += 1
                            int_avg_rtt = float(avg_rtt)
                            print('The average RTT is: %.3f ms' %int_avg_rtt)
                            slash_count = 0
                            break
                        else:
                            print('Looking for average RTT value...')

                    ### Link performance values assignment ###
                    if link_num == 1:
                        link1_int_received_pack = int_received_pack
                        link1_int_received_pack_perc = int_received_pack_perc
                        link1_int_avg_rtt = int_avg_rtt
                    elif link_num == 2:
                        link2_int_received_pack = int_received_pack
                        link2_int_received_pack_perc = int_received_pack_perc
                        link2_int_avg_rtt = int_avg_rtt
                    elif link_num == 3:
                        link3_int_received_pack = int_received_pack
                        link3_int_received_pack_perc = int_received_pack_perc
                        link3_int_avg_rtt = int_avg_rtt
                    elif link_num == 4:
                        link4_int_received_pack = int_received_pack
                        link4_int_received_pack_perc = int_received_pack_perc
                        link4_int_avg_rtt = int_avg_rtt
                    elif link_num == 5:
                        link5_int_received_pack = int_received_pack
                        link5_int_received_pack_perc = int_received_pack_perc
                        link5_int_avg_rtt = int_avg_rtt
                    elif link_num == 6:
                        link6_int_received_pack = int_received_pack
                        link6_int_received_pack_perc = int_received_pack_perc
                        link6_int_avg_rtt = int_avg_rtt
                        link_num = 0
                else:
                    print('searching...')
    #---------------------------------------------------------------------------------------------
    # GOOD OR BAD NETWORK                                                                         |
    #---------------------------------------------------------------------------------------------
    print('\n')
    print('PERFORMANCE SUMMARY')
    print('Link 1:')
    print('   The percentage packet loss is: %d' %link1_int_received_pack_perc)
    print('   The average RTT is: %.3f ms' %link1_int_avg_rtt)
    if link1_int_received_pack_perc <= 25 and link1_int_avg_rtt < 25:
        print('   Link 1 is above average and is performing effectively \n')
    elif link1_int_received_pack_perc <= 25 and link1_int_avg_rtt >= 25 and link1_int_avg_rtt < 200:
        print('   Link 1 is average and will perform sufficiently. Consider network improvement \n')
    elif link1_int_received_pack_perc <= 25 and link1_int_avg_rtt >= 25 and link1_int_avg_rtt >= 200:
        print('   Link 1 is below average and serious improvements need to be made \n')
    elif link1_int_received_pack_perc < 50 and link1_int_received_pack_perc > 25 and link1_int_avg_rtt < 100:
        print('   Link 1 is average and will perform sufficiently. Consider network improvement \n')
    elif link1_int_received_pack_perc < 50 and link1_int_received_pack_perc > 25 and link1_int_avg_rtt >= 100 and link1_int_avg_rtt <200:
        print('   Link 1 is average and will perform sufficiently. Consider network improvement \n')
    elif link1_int_received_pack_perc < 75 and link1_int_received_pack_perc >= 50 and link1_int_avg_rtt < 100:
        print('   Link 1 is below average and serious improvements need to be made \n')
    elif link1_int_received_pack_perc >= 75 and link1_int_avg_rtt < 100:
        print('   Link 1 is below average and serious improvements need to be made \n')
    else:
        print('   Link 1 is below average and serious improvements need to be made \n')

    print('Link 2:')
    print('   The percentage packet loss is: %d' %link2_int_received_pack_perc)
    print('   The average RTT is: %.3f ms' %link2_int_avg_rtt)
    if link2_int_received_pack_perc <= 25 and link2_int_avg_rtt < 25:
        print('   Link 2 is above average and is performing effectively \n')
    elif link2_int_received_pack_perc <= 25 and link2_int_avg_rtt >= 25 and link2_int_avg_rtt < 200:
        print('   Link 2 is average and will perform sufficiently. Consider network improvement \n')
    elif link2_int_received_pack_perc <= 25 and link2_int_avg_rtt >= 25 and link2_int_avg_rtt >= 200:
        print('   Link 2 is below average and serious improvements need to be made \n')
    elif link2_int_received_pack_perc < 50 and link2_int_received_pack_perc > 25 and link2_int_avg_rtt < 100:
        print('   Link 2 is average and will perform sufficiently. Consider network improvement \n')
    elif link2_int_received_pack_perc < 50 and link2_int_received_pack_perc > 25 and link2_int_avg_rtt >= 100 and link1_int_avg_rtt <200:
        print('   Link 2 is average and will perform sufficiently. Consider network improvement \n')
    elif link2_int_received_pack_perc < 75 and link2_int_received_pack_perc >= 50 and link2_int_avg_rtt < 100:
        print('   Link 2 is below average and serious improvements need to be made \n')
    elif link2_int_received_pack_perc >= 75 and link2_int_avg_rtt < 100:
        print('   Link 2 is below average and serious improvements need to be made \n')
    else:
        print('   Link 2 is below average and serious improvements need to be made \n')

    print('Link 3:')
    print('   The percentage packet loss is: %d' %link3_int_received_pack_perc)
    print('   The average RTT is: %.3f ms' %link3_int_avg_rtt)
    if link3_int_received_pack_perc <= 25 and link3_int_avg_rtt < 25:
        print('   Link 3 is above average and is performing effectively \n')
    elif link3_int_received_pack_perc <= 25 and link3_int_avg_rtt >= 25 and link3_int_avg_rtt < 200:
        print('   Link 3 is average and will perform sufficiently. Consider network improvement \n')
    elif link3_int_received_pack_perc <= 25 and link3_int_avg_rtt >= 25 and link3_int_avg_rtt >= 200:
        print('   Link 3 is below average and serious improvements need to be made \n')
    elif link3_int_received_pack_perc < 50 and link3_int_received_pack_perc > 25 and link3_int_avg_rtt < 100:
        print('   Link 3 is average and will perform sufficiently. Consider network improvement \n')
    elif link3_int_received_pack_perc < 50 and link3_int_received_pack_perc > 25 and link3_int_avg_rtt >= 100 and link1_int_avg_rtt <200:
        print('   Link 3 is average and will perform sufficiently. Consider network improvement \n')
    elif link3_int_received_pack_perc < 75 and link3_int_received_pack_perc >= 50 and link3_int_avg_rtt < 100:
        print('   Link 3 is below average and serious improvements need to be made \n')
    elif link3_int_received_pack_perc >= 75 and link3_int_avg_rtt < 100:
        print('   Link 3 is below average and serious improvements need to be made \n')
    else:
        print('   Link 3 is below average and serious improvements need to be made \n')

    print('Link 4:')
    print('   The percentage packet loss is: %d' %link4_int_received_pack_perc)
    print('   The average RTT is: %.3f ms' %link4_int_avg_rtt)
    if link4_int_received_pack_perc <= 25 and link4_int_avg_rtt < 25:
        print('   Link 4 is above average and is performing effectively \n')
    elif link4_int_received_pack_perc <= 25 and link4_int_avg_rtt >= 25 and link4_int_avg_rtt < 200:
        print('   Link 4 is average and will perform sufficiently. Consider network improvement \n')
    elif link4_int_received_pack_perc <= 25 and link4_int_avg_rtt >= 25 and link4_int_avg_rtt >= 200:
        print('   Link 4 is below average and serious improvements need to be made \n')
    elif link4_int_received_pack_perc < 50 and link4_int_received_pack_perc > 25 and link4_int_avg_rtt < 100:
        print('   Link 4 is average and will perform sufficiently. Consider network improvement \n')
    elif link4_int_received_pack_perc < 50 and link4_int_received_pack_perc > 25 and link4_int_avg_rtt >= 100 and link1_int_avg_rtt <200:
        print('   Link 4 is average and will perform sufficiently. Consider network improvement \n')
    elif link4_int_received_pack_perc < 75 and link4_int_received_pack_perc >= 50 and link4_int_avg_rtt < 100:
        print('   Link 4 is below average and serious improvements need to be made \n')
    elif link4_int_received_pack_perc >= 75 and link4_int_avg_rtt < 100:
        print('   Link 4 is below average and serious improvements need to be made \n')
    else:
        print('   Link 4 is below average and serious improvements need to be made \n')

    print('Link 5:')
    print('   The percentage packet loss is: %d' %link5_int_received_pack_perc)
    print('   The average RTT is: %.3f ms' %link5_int_avg_rtt)
    if link5_int_received_pack_perc <= 25 and link5_int_avg_rtt < 25:
        print('   Link 5 is above average and is performing effectively \n')
    elif link5_int_received_pack_perc <= 25 and link5_int_avg_rtt >= 25 and link5_int_avg_rtt < 200:
        print('   Link 5 is average and will perform sufficiently. Consider network improvement \n')
    elif link5_int_received_pack_perc <= 25 and link5_int_avg_rtt >= 25 and link5_int_avg_rtt >= 200:
        print('   Link 5 is below average and serious improvements need to be made \n')
    elif link5_int_received_pack_perc < 50 and link5_int_received_pack_perc > 25 and link5_int_avg_rtt < 100:
        print('   Link 5 is average and will perform sufficiently. Consider network improvement \n')
    elif link5_int_received_pack_perc < 50 and link5_int_received_pack_perc > 25 and link5_int_avg_rtt >= 100 and link1_int_avg_rtt <200:
        print('   Link 5 is average and will perform sufficiently. Consider network improvement \n')
    elif link5_int_received_pack_perc < 75 and link5_int_received_pack_perc >= 50 and link5_int_avg_rtt < 100:
        print('   Link 5 is below average and serious improvements need to be made \n')
    elif link5_int_received_pack_perc >= 75 and link5_int_avg_rtt < 100:
        print('   Link 5 is below average and serious improvements need to be made \n')
    else:
        print('   Link 5 is below average and serious improvements need to be made \n')

    print('Link 6:')
    print('   The percentage packet loss is: %d' %link6_int_received_pack_perc)
    print('   The average RTT is: %.3f ms' %link6_int_avg_rtt)
    if link6_int_received_pack_perc <= 25 and link6_int_avg_rtt < 25:
        print('   Link 6 is above average and is performing effectively \n')
    elif link6_int_received_pack_perc <= 25 and link6_int_avg_rtt >= 25 and link6_int_avg_rtt < 200:
        print('   Link 6 is average and will perform sufficiently. Consider network improvement \n')
    elif link6_int_received_pack_perc <= 25 and link6_int_avg_rtt >= 25 and link6_int_avg_rtt >= 200:
        print('   Link 6 is below average and serious improvements need to be made \n')
    elif link6_int_received_pack_perc < 50 and link6_int_received_pack_perc > 25 and link6_int_avg_rtt < 100:
        print('   Link 6 is average and will perform sufficiently. Consider network improvement \n')
    elif link6_int_received_pack_perc < 50 and link6_int_received_pack_perc > 25 and link6_int_avg_rtt >= 100 and link1_int_avg_rtt <200:
        print('   Link 6 is average and will perform sufficiently. Consider network improvement \n')
    elif link6_int_received_pack_perc < 75 and link6_int_received_pack_perc >= 50 and link6_int_avg_rtt < 100:
        print('   Link 6 is below average and serious improvements need to be made \n')
    elif link6_int_received_pack_perc >= 75 and link6_int_avg_rtt < 100:
        print('   Link 6 is below average and serious improvements need to be made \n')
    else:
        print('   Link 6 is below average and serious improvements need to be made \n')
#==================================================================================================

#==================================================================================================
#-------------------------------------------------------------------------------------------------
# Main Program                                                                                    | 
#-------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    setLogLevel( 'info' )
    #----------------------------------------------------------------------------------------------
    "Test router"
    topo = Net_Topology()
    net = Mininet( topo=topo,
                   waitConnected=True )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r0' ].cmd( 'route' ) )
    
    #----------------------------------------------------------------------------------------------
    #Performance Tests
    #----------------------------------------------------------------------------------------------
    ### Test Losses and Delays ###
    info(net['h1'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee test_output.txt'))
    info(net['h1_2'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    info(net['h1_3'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    info(net['h2'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    info(net['h2_2'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    info(net['h2_3'].cmd('ping -c 10 %s' %net['r0'].IP() + '| tee -a test_output.txt'))
    
    ### Generate Network Traffic ###
    generate_flows(40, 400, net)
    
    ### Read Performance Test Outputs ###
    performance_reader()
    #----------------------------------------------------------------------------------------------
    
    ### Start the mininet CLI ###
    CLI( net )
    net.stop()
#==============================================================================================
