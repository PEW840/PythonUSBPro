import mercury
tagObj  = mercury.TagReadData

x=0
while True:
    if x < 32:
        try:
            rfid = mercury.Reader("tmr:///dev/ttyACM{}".format(x))
        except:
            x += 1
            continue
        else:
            print("Device found at ttyACM{}".format(x))
            break
    else:
        print("Error, could not connect to USB Pro device :( ")
        print("If device was recently connected, wait 30 seconds before retry")
        exit()
#TagReadData Object - Represents a read of an RFID tag:
#
#   epc - corresponds to the Electronic Product Code
#   phase-  of the tag response
#   antenna - indicates where the tag was read
#   read_count - indicates how many times was the tag read during interrogation
#   rssi - is the strength of the signal recieved from the tag
#   frequency - the tag was read with
#   timestamp - of the read, in floating-point seconds for datetime.fromtimestamp
#   epc_mem_data - contains the EPC bank data bytes
#   tid_mem_data contains the TID bank data bytes
#   user_mem_data contains the User bank data bytes
#   reserved_mem_data contains the Reserved bank data bytes

#Please note that the bank data bytes need to be requested via the bank parameter of the 
#setReadPlan function. Data not requested will not be read.
#
#The friendly string representation (str) of the tag data is its EPC.
#e.g. print(tag) results in: b'E2000087071401930700D206'
#
#However, to avoid ambiguity, the string representation (repr) includes a prefix.
#e.g. print(repr(tag)) results in: EPC(b'E2000087071401930700D206')
#------------------------------------------------------------------------------------------------------
def TagReadDataObject():
    return tagObj

#------------------------------------------------------------------------------------------------------
#antenna: 1 for internal and 2 for external antenna
#timeout: Reading time in ms.
def read(timeout):
    return rfid.read(timeout)

#------------------------------------------------------------------------------------------------------
#Perfoms a synchronous write. Return 1 upon success, or 0 i no tag was found.
def write(newEpc, oldEpc):
    if rfid.write(newEpc, oldEpc):
        print('Rewrited "{}" with "{}"'.format(oldEpc, newEpc))
        return 1
    else:
        print('No tag found!')
        return 0

def setReadPlan(antenna=1, protocol="GEN2", epcTarget=None, bank=[], readPower=0):
    rfid.set_read_plan([antenna], protocol, epcTarget, bank, readPower)
#------------------------------------------------------------------------------------------------------    
#Callback routine for enableStats, this subroutine prints read stats
def statsReceived(stats):
    print({"temp" : stats.temperature})
    print({"antenna" : stats.antenna})
    print({"protocol" : stats.protocol})
    print({"frequency" : stats.frequency})

#Provide reader stats during asynchronous tag reads
#This function must be called before 'startReading()'
def enableStats():
    rfid.enable_stats(statsReceived)

#------------------------------------------------------------------------------------------------------
#Callback routine for enableExceptionHandler, this routine prints exception
def exceptionHandle(e):
    print('Exception: {}'.format(e))

#Provide reader exception handling.
#The function must be called before 'startReading()'
def enableExceptionHandler():
    rfid.enable_exception_handler(exceptionHandle)


#------------------------------------------------------------------------------------------------------
#Starts asynchronous reading. It returns immediatly and begins a sequence of reads or a continous read.
#The results are passed the the 'callback'. The reads are repeated until the stopReading() is called.
#Callback - Will be invoked for every tag detected
#onTime   - Sets the duration, in ms, for the reader to be quiet while querying
def startReading(callback, onTime, offTime):
    rfid.start_reading(callback, onTime, offTime)

#------------------------------------------------------------------------------------------------------
#Stops the asynchronous reading started by 'startReading()'
def stopReading():
    rfid.stopReading()

#------------------------------------------------------------------------------------------------------
#Reads byte from the memory bank of a tag. Returns bytearray or None if no tag was found.
#Upon failure an exception is raised
def readTagMem(bank, address, count, epcTarget):
    return rfid.read_tag_mem(bank, address, count, epc_target=epcTarget)

#------------------------------------------------------------------------------------------------------
#Writes byte to the memory bank of a tag. Returns 1 upon success, or 0 if no tag was found.
#Upon failure an exception is raised
def writeTagMem(bank, address, data, epcTarget):
    if rfid.write_tag_mem(bank, address, data, epc_target=epcTarget):
        print('Wrote "{}" at bank "{}" and address "{}" successfully!'.format(data, bank, address))
        return 1
    else:
        print('No tag found!')
        return 0

#------------------------------------------------------------------------------------------------------
#Returns value of GPIO pin, or None if the pin is not configured as input (see getGpioInputs)
def gpiGet(pin):
    return rfid.gpi_get(pin)

#------------------------------------------------------------------------------------------------------
#Sets value of a GPIO pin configured as output (see getGpioOutputs)
#pin   - GPIO pin
#value - 0 or 1
def gpoSet(pin, value):
    rfid.gpo_set(pin, value)

#------------------------------------------------------------------------------------------------------
#Returns a model identifier for the connected reader hardware (e.g "M6e Nano" or "M6e Micro USBPro")
def getModel():
    return rfid.get_model()

#------------------------------------------------------------------------------------------------------
#Returns the software version of the reader hardware
def getSoftwareVersion():
    return rfid.get_software_version()

#------------------------------------------------------------------------------------------------------
#Returns a serial number of the reader, the same number printed on the barcode label
def getSerial():
    return rfid.get_serial()

#------------------------------------------------------------------------------------------------------
#Controls the Region of Operation for the connected device
#region - e.g "EU3"
def setRegion(region):
    rfid.set_region(region)

#------------------------------------------------------------------------------------------------------
#Lists supported regions for the connected device
def supportedRegions():
    return rfid.get_supported_regions()

#------------------------------------------------------------------------------------------------------
#Gets the frequencies for the reader to use, in kHz
def getHopTable():
    return rfid.get_hop_table()

#------------------------------------------------------------------------------------------------------
#Sets the frequencies for the reader to use, in kHz
#table - a list with frequencies
def setHopTable(table):
    rfid.set_hop_table()

#------------------------------------------------------------------------------------------------------
#Gets the frequency hop time, in ms
def getHopTime():
    return rfid.get_hop_time()

#------------------------------------------------------------------------------------------------------
#sets the frequency hop time, in ms
def setHopTime(num):
    rfid.set_hop_time(num)

#------------------------------------------------------------------------------------------------------
#Lists available antennas, e.g. [1,2]
def getAntennas():
    return rfid.get_antennas()

#------------------------------------------------------------------------------------------------------
#Returns number of the antenna ports where the reader has detected antennas
def getConnectedPorts():
    return rfid.get_connected_ports()

#------------------------------------------------------------------------------------------------------
#Lists supported radio power range, in centidBm
def getPowerRange():
    return rfid.get_power_range()

#------------------------------------------------------------------------------------------------------
#Lists configured read powers for each antenna. [(antenna, power)]. 
#The list does not include antennas with default power setting, so the list may be empty.
def getReadPowers():
    return rfid.get_read_powers()

#------------------------------------------------------------------------------------------------------
#Lists configured write powers for each antenna [(antenna, power)]
def getWritePowers():
    return rfid.get_write_powers()

#------------------------------------------------------------------------------------------------------
#sets the read power for each listed antenna and return the read setted values.
#Setted values may differ from those passed due to reader rounding.
#powers - List of 2-tuples that include:
#           *which antenna (or virtual antenna numbers) is going to be setted
#           *required power, in centidBm, for the antenna, overriding the value from setReadPlan or
#            reader specific default. The value must be withing the allowed power range
#   e.g. setReadPowers( [(1, 1533), (2, 1912)] )
def setReadPowers(powers):
    return rfid.set_read_powers(powers)

#------------------------------------------------------------------------------------------------------
#Set the write power for each listed antenna and return the read setted value
def setWritePowers(powers):
    return rfid.set_write_powers(powers)

#------------------------------------------------------------------------------------------------------
#Get numbers of the GPIO pins available as input pins on the device.
def getGpioInputs():
    return rfid.get_gpio_inputs()

#------------------------------------------------------------------------------------------------------
#Set numbers of the GPIO pins available as input pins on the device.
def setGpioInputs(inputs):
    rfid.set_gpio_inputs(inputs)

#------------------------------------------------------------------------------------------------------
#Get numbers of the GPIO pins available as output pins on the device.
def getGpioOutputs():
    return rfid.get_gpio_outputs()

#------------------------------------------------------------------------------------------------------
#Set numbers of the GPIO pins available as output pins on the device.
#On some devices this parameter is not writeable. Thus, instead of calling setGpioOutputs with the a 
#set you may need to call set_gpio_inputs with the pin omitted.
def setGpioOutputs(outputs):
    rfid.set_gpio_outputs(outputs)

#------------------------------------------------------------------------------------------------------
#Returns the current Gen2 BLF setting.
def getGen2Blf():
    return rfid.get_gen2_blf()

#------------------------------------------------------------------------------------------------------
#Sets the Gen2 BLF. Supported values include:
#   * 250 (250KHz)
#   * 320 (320KHz)
#   * 640 (640KHz)
#Not all values may be supported by a particular reader. If successful the input value will be returned
def setGen2Blf(blf):
    return rfid.set_gen2_blf(blf)

#------------------------------------------------------------------------------------------------------
#Returns the current Gen2 Tari setting.
def getGen2Tari():
    return rfid.get_gen2_tari()

#------------------------------------------------------------------------------------------------------
#Sets the Gen2 Tari. Supported values include:
#   * 0 (25 us)
#   * 1 (12.5 us)
#   * 2 (6.25 us)
#If successful the input value will be returned
def setGen2Tari(tari):
    return rfid.set_gen2_tari()

#------------------------------------------------------------------------------------------------------
#Returns the current Gen2 TagEncoding setting.
def getGen2Tagencoding():
    return rfid.get_gen2_tagencoding()

#------------------------------------------------------------------------------------------------------
#Sets the Gen2 TagEncoding. Supported values include:
#   * 0 (FM0)
#   * 1 (M = 2)
#   * 2 (M = 4)
#   * 3 (M = 8)
#If successful the input value will be returned
def setGen2Tagencoding(tagencoding):
    return rfid.set_gen2_tagencoding(tagencoding)

#------------------------------------------------------------------------------------------------------
#Returns the current Gen2 Session setting
def getGen2Session():
    return rfid.get_gen2_session()

#------------------------------------------------------------------------------------------------------
#Sets the Gen2 TagEncoding. Supported values include:
#   * 0 (FM0)
#   * 1 (M = 2)
#   * 2 (M = 4)
#   * 3 (M = 8)
#If successful the input value will be returned. For example:
def setGen2Session(session):
    return rfid.set_gen2_session(session)

#------------------------------------------------------------------------------------------------------
#Returns the current Gen2 Target setting
def getGen2Target():
    return rfid.get_gen2_target()

#------------------------------------------------------------------------------------------------------
#Sets the Gen2 Target. Supported values include:
#   * 0 (A)
#   * 1 (B)
#   * 2 (AB)
#   * 3 (BA)
#If successful the input value will be returned
def setGen2Targer(target):
    return rfid.set_gen_target(target)


#------------------------------------------------------------------------------------------------------
#Returns the current Gen2 Q setting as a tuple containing the current Q type, and initial Q value
def getGen2Q():
    return rfid.get_gen2_q()

#------------------------------------------------------------------------------------------------------
#Sets the Gen2 Q.
#   * qtype defines Dynamic vs Static Q value where:
#       - 0 (Dynamic)
#       - 1 (Static)
#   * initialq defines 2^initialq time slots to be used initially for tag communication.
#If Dynamic Q is used then the input initialq value is ignored as the reader will choose this on its own. 
#It is then likely for initialq on a get to be different than the value used on a set.
#If successful the input value will be returned
def setGen2Q(qtype, initialq):
    return rfid.set_gen2_q(qtype, initialq)

#------------------------------------------------------------------------------------------------------
#Returns the chip temperature in degrees of Celsius
def getTemperature():
    return rfid.get_temperature()

#------------------------------------------------------------------------------------------------------
#Example routine. This routine will run if this file is executed by itself
def main():
######## Set EU3 region if supported ########
    supRegions = supportedRegions()
    if 'EU3' in supRegions:
        setRegion("EU3")
    else:
        print("Error: EU3 is not supported")
    
######## Set read plan ########
    setReadPlan() #Using default values
    
    #print(supportedRegions())
    #print(getHopTable())
    #print(getAntennas())
    #print(read(1,3000))
    #x = TagReadDataObject()

if __name__ == "__main__":
    main()
#------------------------------------------------------------------------------------------------------