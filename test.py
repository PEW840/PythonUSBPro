import mercury
rfid = mercury.Reader("tmr:///dev/ttyUSB0")

def init():
    rfid.set_region("EU")
    
def read():
    rfid.set_read_plan([1], "GEN2")
    return rfid.read()



def main():
    init()
    read()

if __name__ == __main__:
    main()
