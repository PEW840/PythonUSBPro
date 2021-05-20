import mercury
rfid = mercury.Reader("tmr:///dev/ttyACM0")

def init():
    rfid.set_region("EU3")

#antenna: 1 for internal and 2 for external antenna
#timeout: Reading time in ms.
def read(antenna, timeout):
    rfid.set_read_plan([antenna], "GEN2")
    return rfid.read(timeout)

#Perfoms a synchronous write. Return 1 upon success, or 0 i no tag was found.
def write(newEpc, oldEpc):
    if rfid.write(epc_code=newEpc, epc_target=oldEpc):
        print('Rewrited "{}" with "{}"'.format(oldEpc, newEpc))
        return 1
    else:
        print('No tag found')
        return 0
    
#Provide reader stats during asynchronous tag reads
#This function must be called before 'read()'
def enableStats:
    pass


def supportedRegions():
    return rfid.get_supported_regions()

def supportedFreq():
    return rfid.get_hop_table()

def availableAntennas():
    return rfid.get_antennas()

def main():
    init()
    print(supportedRegions())
    print(supportedFreq())
    print(availableAntennas())
    print(read(3000))

if __name__ == "__main__":
    main()
