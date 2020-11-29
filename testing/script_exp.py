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

def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo(6)
    net = Mininet(topo)
    net.start()
    h1 = net.get('h1')
    h2 = net.get('h2')
    hlist = []
    
    # h1.cmd('/home/rohit/anaconda3/bin/python ./exp.py <inp.txt  >out.txt')
    result = h1.cmd("mongod &")
    print(result)
    sleep(1)
    result2 = h1.cmd("/home/rohit/anaconda3/bin/python ../server.py 10.0.0.1 &")
    print(result2)
    sleep(1)
    result3 = h2.cmd("/home/rohit/anaconda3/bin/python ../client.py 10.0.0.1 <./inputs/input.txt >./outputs/output.txt")
    print(result3)
    sleep(4)
    # print("Dumping host connections")
    # dumpNodeConnections(net.hosts)
    # print("Testing network connectivity")
    # net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()

