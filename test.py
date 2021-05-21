import USBPro as up

def main():
######## Set EU3 region if supported ########
    supRegions = up.supportedRegions()
    if 'EU3' in supRegions:
        up.setRegion("EU3")
        print('Region "EU3" successfully set')
    else:
        print("Error: EU3 is not supported")


    tagsFound = up.read(2000)

    for i in tagsFound:
        up.write(i.epc+1, i.epc) 
    
if __name__ == "__main__":
    main()