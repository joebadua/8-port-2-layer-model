class Host:
    def __init__(self, host, mac_addr, switch_pn): 
        self.host = host
        self.mac_addr = mac_addr
        self.switch_pn = switch_pn

    def asdict(self):
        return {'host':self.host, 'mac_addr': self.mac_addr, 'switch_pn': self.switch_pn }

class FWDTable:    
    def __init__(self):
        self.table = []

    def add(self, Host):
        self.table.append(Host)

    def getTable(self):
        return self.table

    def printTable(self): 
        count = 0
        if self.table == []:
            print("Nothing in forwarding table!")
        else:     
            print("FORWARD TABLE")
            for x in self.table:
                print(str(count) + ". Host: " + x.host + " | Mac Address: "+ str(x.mac_addr) +" | Switch Port #: "+ str(x.switch_pn))
                count+=1

class TMTable:
    def __init__(self, fwdtable):
        self.table = fwdtable.getTable()
        self.ports = 8
    
    def printFWDTable(self):
        if self.table == []:
            print("Nothing inside forwarding table!") 
        else:
            count = 0
            print("FORWARD TABLE")
            for x in self.table:
                print(str(count) + ". Host: " + x.host + " | Mac Address: "+ str(x.mac_addr) +" | Switch Port Number: "+ str(x.switch_pn))
                count+=1

    def Transmission(self, DA, SA):
        isFound = False # for when Host Name & Port Number match
        isFoundInvalid = False # for when Host Name match, but not port number
        SAMatch = False # for when there is a match for SA in FWD Table

        trans = SA.host + "->" + DA.host
        pkt = "{" + str(DA.mac_addr) + "," + str(SA.mac_addr) + "}"
        print("TRANS: " + trans + " | PACKET: " + pkt)
        
        for x in self.table:
            if x.host == SA.host:
                SAMatch = True
            elif x.host == DA.host:
                if x.switch_pn == DA.switch_pn:
                    isFound = True
                    print(DA.host + " is in FWD TABLE, and SWITCH PORT NUMBER matches. PACKET will only output at DA - " + pkt + " @P" + str(DA.switch_pn))
                else:
                    isFoundInvalid = True
                    print(DA.host + " is in FWD TABLE but does not have original SWITCH PORT NUMBER. ")
                    self.table.remove(x)
                    return
        
        if isFound == False:
            if SAMatch == False: # you only want to append to FWD table if SA is not found
                self.table.append(SA)
            
            print("DA was not found in FWD TABLE")
            count = 0
            while count < self.ports:
                if count == SA.switch_pn:
                    print("P" + str(SA.switch_pn) + ":  N/A") 
                    count += 1
                else: 
                    print("P" + str(count) + ": " + pkt)
                    count += 1   
        else:
            self.table.append(SA)
            count = 0
            while count < self.ports:
                if count == DA.switch_pn:
                    print("P" + str(DA.switch_pn) + ": "+ pkt)
                    count += 1
                else:
                    print("P" + str(count) + ":  N/A") 
                    count += 1

#a = Host('A', 50, 0)
#b = Host('B', 51, 1)
##c = Host('C', 52, 2)
#d = Host('D', 53, 3)
#d_2 = Host('D', 50, 0) # for testing if port changes for a Host

a = Host('A', 20, 3)
b = Host('B', 21, 7)
c = Host('C', 22, 5)

fwdtable = FWDTable()

tmtable = TMTable(fwdtable)

print("TIME 1")
#tmtable.Transmission(a, d) # D -> A
tmtable.Transmission(c, a)
print("--------")
tmtable.printFWDTable()

print("--------")
print("TIME 2")
#tmtable.Transmission(d, c) # C -> D
tmtable.Transmission(c, b)
print("--------")
tmtable.printFWDTable()


print("--------")
print("TIME 3")
#tmtable.Transmission(c, a) # A -> C
tmtable.Transmission(a, c)
print("--------")
tmtable.printFWDTable()

print("--------")
print("TIME 4")
#tmtable.Transmission(a, b) # B -> A
tmtable.Transmission(b, a)
print("--------")
tmtable.printFWDTable()

print("--------")
#tmtable.printFWDTable()