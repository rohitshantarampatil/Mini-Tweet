#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import *
from mininet.net import *
from mininet.util import *
from mininet.log import *
from time import sleep

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self, n=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)


class FatTree(Topo):
    def __init__(self,**opts):
        Topo.__init__(self, **opts)
        h1 = self.addHost('h1')
        s1 = self.addSwitch('s1')
        self.addLink(h1,s1,bw=40)
        
        #depth 1
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        self.addLink(s1,s2,bw=40)
        self.addLink(s1,s3,bw=40)

        #depth 2
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')

        self.addLink(s2,s4,bw=20)
        self.addLink(s2,s5,bw=20)
        self.addLink(s3,s6,bw=20)
        self.addLink(s3,s7,bw=20)

        #depth 3
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        h9 = self.addHost('h9')

        self.addLink(s4,h2,bw=10)
        self.addLink(s4,h3,bw=10)
        self.addLink(s5,h4,bw=10)
        self.addLink(s5,h5,bw=10)
        self.addLink(s6,h6,bw=10)
        self.addLink(s6,h7,bw=10)
        self.addLink(s7,h8,bw=10)
        self.addLink(s7,h9,bw=10)



def simpleTest():
    "Create and test a simple network"
    topo = FatTree()
    net = Mininet(topo)
    net.start()
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')
    h8 = net.get('h8')
    h9 = net.get('h9')
    hlist = []
    
    # h1.cmd('/home/rohit/anaconda3/bin/python ./exp.py <inp.txt  >out.txt')
    result = h1.cmd("mongod &")
    print(result)
    sleep(1)
    result2 = h1.cmd("/home/rohit/anaconda3/bin/python ../server.py 10.0.0.1 &")
    # print(result2)
    sleep(2)
    h2.cmd("/home/rohit/anaconda3/bin/python ../client.py 10.0.0.1 <./inputs/input1.txt >./outputs/output1.txt")
    h4.cmd("/home/rohit/anaconda3/bin/python ../client.py 10.0.0.1 <./inputs/input2.txt >./outputs/output2.txt")
    h6.cmd("/home/rohit/anaconda3/bin/python ../client.py 10.0.0.1 <./inputs/input3.txt >./outputs/output3.txt")
    h8.cmd("/home/rohit/anaconda3/bin/python ../client.py 10.0.0.1 <./inputs/input4.txt >./outputs/output4.txt")
    h9.cmd("/home/rohit/anaconda3/bin/python ../client.py 10.0.0.1 <./inputs/input5.txt >./outputs/output5.txt")
    
    sleep(5)
    

    # print("Dumping host connections")
    # dumpNodeConnections(net.hosts)
    # print("Testing network connectivity")
    # net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()

