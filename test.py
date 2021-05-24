import USBPro as up
from time import sleep
def main():
######## Init USBPro device ########

######## Set EU3 region if supported ########
    supRegions = up.supportedRegions()
    if 'EU3' in supRegions:
        up.setRegion("EU3")
        print('Region "EU3" successfully set')
    else:
        print("Error: EU3 is not supported")

######## Read temperature ########
    print('Temperature is: {}C'.format(up.getTemperature()))

# Button/LED            GPIO pin
# Button 1 (Red)        1 if configured as input
# Button 2 (Yellow)     2 if configured as input
# LED 1 (Yellow)        1 if configured as output
# LED 2 (Red)           2 if configured as output

######## Configure GPIO pin 1 and 2 as outputs and turn them off ########
    up.setGpioOutputs([2])

######## Configure GPIO pin 1 as input (Button) and 2 as output (LED) ########
    #up.setGpioOutputs([2])
    up.setGpioInputs([1])

######## Turn on LED 2 (Red) ########
    up.gpoSet(2, True)
    #up.gpoSet(1, False)
        
    while (up.gpiGet(1) == True):
        pass
    print("Button 1 pressed")
    
    #while (up.gpiGet(1) == ):
    #    pass
        

    #agsFound = up.read(2000)

    #for i in tagsFound:
     #   up.write(i.epc+1, i.epc) 
    
if __name__ == "__main__":
    main()